#!/usr/bin/env python3
"""
Script para rellenar datos históricos de precios PVPC.
"""

import os
import sys
from datetime import datetime, date, timedelta
from dotenv import load_dotenv
import time

from src.client import ESIOSClient
from src.database import Database
from src.indicators import PVPC_PRECIO
from src.models import parse_esios_response, calculate_tramos


def backfill(start_date: date, end_date: date, skip_existing: bool = True):
    """
    Rellena datos históricos desde start_date hasta end_date.
    
    Args:
        start_date: Fecha de inicio
        end_date: Fecha de fin
        skip_existing: Si es True, salta fechas que ya están en la BD
    """
    # Cargar variables de entorno
    load_dotenv()
    api_key = os.getenv('ESIOS_API_KEY')
    
    if not api_key:
        print("❌ Error: No se encontró ESIOS_API_KEY en el archivo .env")
        sys.exit(1)
    
    print(f"📅 Rellenando datos históricos")
    print(f"   Desde: {start_date.strftime('%d/%m/%Y')}")
    print(f"   Hasta: {end_date.strftime('%d/%m/%Y')}")
    print()
    
    try:
        with ESIOSClient(api_key) as client, Database() as db:
            # Calcular número total de días
            total_days = (end_date - start_date).days + 1
            current_date = start_date
            processed = 0
            skipped = 0
            errors = 0
            
            while current_date <= end_date:
                try:
                    # Verificar si ya existe
                    if skip_existing and db.has_date(current_date):
                        print(f"⏭️  {current_date.strftime('%d/%m/%Y')} - ya existe (saltando)")
                        skipped += 1
                        current_date += timedelta(days=1)
                        continue
                    
                    # Obtener datos de la API
                    print(f"⏳ {current_date.strftime('%d/%m/%Y')} - consultando API...", end=" ")
                    response = client.get_indicator(PVPC_PRECIO, current_date, current_date)
                    
                    # Parsear y calcular tramos
                    prices = parse_esios_response(response)
                    
                    if not prices:
                        print("⚠️  sin datos")
                        errors += 1
                        current_date += timedelta(days=1)
                        continue
                    
                    prices = calculate_tramos(prices)
                    
                    # Guardar en BD
                    prices_tuples = [
                        (p.fecha, p.hora, p.precio, p.tramo) 
                        for p in prices
                    ]
                    count = db.insert_prices_batch(prices_tuples)
                    
                    print(f"✅ guardados {count} registros")
                    processed += 1
                    
                    # Pausa para no sobrecargar la API
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"❌ error: {e}")
                    errors += 1
                
                current_date += timedelta(days=1)
            
            # Resumen
            print()
            print("═" * 50)
            print("Resumen del backfill:")
            print(f"  Total de días:      {total_days}")
            print(f"  ✅ Procesados:      {processed}")
            print(f"  ⏭️  Saltados:        {skipped}")
            print(f"  ❌ Errores:         {errors}")
            print("═" * 50)
            
            # Información de la base de datos
            fecha_min, fecha_max = db.get_date_range()
            if fecha_min and fecha_max:
                print(f"\n📊 Base de datos actualizada:")
                print(f"   {fecha_min.strftime('%d/%m/%Y')} - {fecha_max.strftime('%d/%m/%Y')}")
            
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        sys.exit(1)


def main():
    """Función principal con argumentos de línea de comandos."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Rellena datos históricos de precios PVPC'
    )
    parser.add_argument(
        '--start',
        type=str,
        help='Fecha de inicio (formato: YYYY-MM-DD, ej: 2024-01-01)',
        required=True
    )
    parser.add_argument(
        '--end',
        type=str,
        help='Fecha de fin (formato: YYYY-MM-DD). Por defecto: hoy',
        default=None
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Forzar actualización de fechas existentes'
    )
    
    args = parser.parse_args()
    
    # Parsear fechas
    try:
        start_date = datetime.strptime(args.start, '%Y-%m-%d').date()
        
        if args.end:
            end_date = datetime.strptime(args.end, '%Y-%m-%d').date()
        else:
            end_date = datetime.now().date()
        
        if start_date > end_date:
            print("❌ Error: La fecha de inicio debe ser anterior a la fecha de fin")
            sys.exit(1)
        
    except ValueError as e:
        print(f"❌ Error al parsear fechas: {e}")
        print("   Usa el formato YYYY-MM-DD (ej: 2024-01-01)")
        sys.exit(1)
    
    # Ejecutar backfill
    backfill(start_date, end_date, skip_existing=not args.force)


if __name__ == "__main__":
    main()
