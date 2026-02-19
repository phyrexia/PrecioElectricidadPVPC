#!/usr/bin/env python3
"""
Script para consultar precios históricos de la base de datos.
"""

import sys
from datetime import datetime, date
from src.database import Database
from src.models import PricePoint, format_price_table


def consultar_fecha(fecha: date):
    """
    Consulta y muestra los precios de una fecha específica.
    
    Args:
        fecha: Fecha a consultar
    """
    with Database() as db:
        # Obtener precios de la BD
        rows = db.get_prices_by_date(fecha)
        
        if not rows:
            print(f"⚠️  No hay datos para {fecha.strftime('%d/%m/%Y')}")
            print(f"\n💡 Tip: Usa backfill.py para obtener datos históricos:")
            print(f"   python backfill.py --start {fecha.strftime('%Y-%m-%d')} --end {fecha.strftime('%Y-%m-%d')}")
            return
        
        # Convertir a PricePoint
        prices = [
            PricePoint(
                fecha=date.fromisoformat(row['fecha']),
                hora=row['hora'],
                precio=row['precio'],
                tramo=row['tramo']
            )
            for row in rows
        ]
        
        # Mostrar tabla
        table = format_price_table(prices, fecha)
        print(table)
        
        # Información adicional
        fecha_min, fecha_max = db.get_date_range()
        if fecha_min and fecha_max:
            print(f"📊 Datos disponibles en BD: {fecha_min.strftime('%d/%m/%Y')} - {fecha_max.strftime('%d/%m/%Y')}")


def main():
    """Función principal con argumentos de línea de comandos."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Consulta precios PVPC históricos de la base de datos'
    )
    parser.add_argument(
        'fecha',
        type=str,
        nargs='?',
        help='Fecha a consultar (formato: YYYY-MM-DD, ej: 2025-11-01). Por defecto: hoy',
        default=None
    )
    
    args = parser.parse_args()
    
    # Parsear fecha
    if args.fecha:
        try:
            fecha = datetime.strptime(args.fecha, '%Y-%m-%d').date()
        except ValueError as e:
            print(f"❌ Error al parsear fecha: {e}")
            print("   Usa el formato YYYY-MM-DD (ej: 2025-11-01)")
            sys.exit(1)
    else:
        fecha = datetime.now().date()
    
    # Consultar
    consultar_fecha(fecha)


if __name__ == "__main__":
    main()
