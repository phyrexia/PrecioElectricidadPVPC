#!/usr/bin/env python3
"""
Script principal para obtener precios PVPC del día actual.
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

from src.client import ESIOSClient
from src.database import Database
from src.indicators import PVPC_PRECIO
from src.models import parse_esios_response, calculate_tramos, format_price_table


def main():
    """Función principal."""
    # Cargar variables de entorno
    load_dotenv()
    api_key = os.getenv('ESIOS_API_KEY')
    
    if not api_key:
        print("❌ Error: No se encontró ESIOS_API_KEY en el archivo .env")
        sys.exit(1)
    
    # Fecha de hoy
    today = datetime.now().date()
    
    print(f"🔌 Conectando con API de ESIOS...")
    print(f"📅 Obteniendo precios para {today.strftime('%d/%m/%Y')}\n")
    
    try:
        # Crear cliente y base de datos
        with ESIOSClient(api_key) as client, Database() as db:
            # Obtener datos de la API
            print("⏳ Consultando API...")
            response = client.get_indicator(PVPC_PRECIO, today, today)
            
            # Parsear respuesta
            prices = parse_esios_response(response)
            
            if not prices:
                print("⚠️  No se encontraron datos para hoy")
                sys.exit(0)
            
            print(f"✅ Recibidos {len(prices)} precios")
            
            # Calcular tramos
            prices = calculate_tramos(prices)
            
            # Guardar en base de datos
            print("💾 Guardando en base de datos...")
            prices_tuples = [
                (p.fecha, p.hora, p.precio, p.tramo) 
                for p in prices
            ]
            count = db.insert_prices_batch(prices_tuples)
            print(f"✅ Guardados {count} registros")
            
            # Mostrar tabla
            table = format_price_table(prices, today)
            print(table)
            
            # Información de la base de datos
            fecha_min, fecha_max = db.get_date_range()
            if fecha_min and fecha_max:
                print(f"📊 Base de datos: {fecha_min.strftime('%d/%m/%Y')} - {fecha_max.strftime('%d/%m/%Y')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
