#!/usr/bin/env python3
"""
Script para graficar la evolución de precios PVPC.
"""

import sys
from datetime import datetime, date, timedelta
from typing import List, Tuple
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from src.database import Database
from src.models import PricePoint


def obtener_datos_grafico(dias: int = 30) -> Tuple[List[datetime], List[float], List[str]]:
    """
    Obtiene datos para graficar de los últimos N días.
    
    Args:
        dias: Número de días hacia atrás
        
    Returns:
        Tupla de (fechas, precios, tramos)
    """
    fecha_fin = datetime.now().date()
    fecha_inicio = fecha_fin - timedelta(days=dias)
    
    fechas = []
    precios = []
    tramos = []
    
    with Database() as db:
        current_date = fecha_inicio
        while current_date <= fecha_fin:
            rows = db.get_prices_by_date(current_date)
            
            for row in rows:
                dt = datetime.combine(
                    date.fromisoformat(row['fecha']),
                    datetime.min.time()
                ) + timedelta(hours=row['hora'])
                
                fechas.append(dt)
                precios.append(row['precio'])
                tramos.append(row['tramo'])
            
            current_date += timedelta(days=1)
    
    return fechas, precios, tramos


def graficar_evolucion(dias: int = 30, guardar: str = None):
    """
    Genera un gráfico de la evolución de precios.
    
    Args:
        dias: Número de días hacia atrás
        guardar: Ruta donde guardar la imagen (opcional)
    """
    print(f"📊 Generando gráfico de los últimos {dias} días...")
    
    fechas, precios, tramos = obtener_datos_grafico(dias)
    
    if not fechas:
        print("⚠️  No hay datos suficientes para graficar")
        print(f"💡 Usa backfill.py para descargar datos históricos")
        return
    
    # Configurar figura
    plt.figure(figsize=(14, 7))
    
    # Colores por tramo
    colores = []
    for tramo in tramos:
        if tramo == 'verde':
            colores.append('#4CAF50')
        elif tramo == 'amarillo':
            colores.append('#FFC107')
        elif tramo == 'rojo':
            colores.append('#F44336')
        else:
            colores.append('#9E9E9E')
    
    # Gráfico de línea con puntos coloreados
    plt.plot(fechas, precios, linewidth=1, color='#2196F3', alpha=0.6, zorder=1)
    plt.scatter(fechas, precios, c=colores, s=10, alpha=0.8, zorder=2)
    
    # Configuración de ejes
    plt.xlabel('Fecha', fontsize=12, fontweight='bold')
    plt.ylabel('Precio (€/kWh)', fontsize=12, fontweight='bold')
    plt.title(f'Evolución Precio PVPC - Últimos {dias} días', 
              fontsize=14, fontweight='bold', pad=20)
    
    # Formato del eje X
    ax = plt.gca()
    if dias <= 7:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m %H:%M'))
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=12))
    elif dias <= 30:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    else:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    
    plt.xticks(rotation=45, ha='right')
    
    # Grid
    plt.grid(True, alpha=0.3, linestyle='--')
    
    # Leyenda personalizada
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#4CAF50', label='🟢 Verde (más barato)'),
        Patch(facecolor='#FFC107', label='🟡 Amarillo (intermedio)'),
        Patch(facecolor='#F44336', label='🔴 Rojo (más caro)')
    ]
    plt.legend(handles=legend_elements, loc='upper right', framealpha=0.9)
    
    # Estadísticas
    precio_medio = sum(precios) / len(precios)
    precio_min = min(precios)
    precio_max = max(precios)
    
    stats_text = f'Media: {precio_medio:.5f} €/kWh\nMín: {precio_min:.5f} €/kWh\nMáx: {precio_max:.5f} €/kWh'
    plt.text(0.02, 0.98, stats_text, transform=ax.transAxes,
             verticalalignment='top', bbox=dict(boxstyle='round', 
             facecolor='white', alpha=0.8), fontsize=9)
    
    plt.tight_layout()
    
    # Guardar o mostrar
    if guardar:
        plt.savefig(guardar, dpi=150, bbox_inches='tight')
        print(f"✅ Gráfico guardado en: {guardar}")
    else:
        print("📈 Mostrando gráfico...")
        plt.show()


def graficar_comparacion_diaria(fecha: date = None, guardar: str = None):
    """
    Genera un gráfico de barras para un día específico.
    
    Args:
        fecha: Fecha a graficar (por defecto hoy)
        guardar: Ruta donde guardar la imagen (opcional)
    """
    if fecha is None:
        fecha = datetime.now().date()
    
    print(f"📊 Generando gráfico del día {fecha.strftime('%d/%m/%Y')}...")
    
    with Database() as db:
        rows = db.get_prices_by_date(fecha)
        
        if not rows:
            print(f"⚠️  No hay datos para {fecha.strftime('%d/%m/%Y')}")
            return
        
        horas = [f"{row['hora']:02d}h" for row in rows]
        precios = [row['precio'] for row in rows]
        tramos = [row['tramo'] for row in rows]
    
    # Colores
    colores = ['#4CAF50' if t == 'verde' else '#FFC107' if t == 'amarillo' else '#F44336' for t in tramos]
    
    # Gráfico de barras
    plt.figure(figsize=(14, 6))
    bars = plt.bar(horas, precios, color=colores, alpha=0.8, edgecolor='black', linewidth=0.5)
    
    # Línea de precio medio
    precio_medio = sum(precios) / len(precios)
    plt.axhline(y=precio_medio, color='blue', linestyle='--', 
                linewidth=2, label=f'Precio medio: {precio_medio:.5f} €/kWh', alpha=0.7)
    
    plt.xlabel('Hora', fontsize=12, fontweight='bold')
    plt.ylabel('Precio (€/kWh)', fontsize=12, fontweight='bold')
    plt.title(f'Precios PVPC por Hora - {fecha.strftime("%d/%m/%Y")}', 
              fontsize=14, fontweight='bold', pad=20)
    
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, alpha=0.3, axis='y', linestyle='--')
    
    # Leyenda
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#4CAF50', label='🟢 Verde'),
        Patch(facecolor='#FFC107', label='🟡 Amarillo'),
        Patch(facecolor='#F44336', label='🔴 Rojo'),
        plt.Line2D([0], [0], color='blue', linewidth=2, linestyle='--', 
                   label=f'Media: {precio_medio:.5f} €/kWh')
    ]
    plt.legend(handles=legend_elements, loc='upper right', framealpha=0.9)
    
    plt.tight_layout()
    
    # Guardar o mostrar
    if guardar:
        plt.savefig(guardar, dpi=150, bbox_inches='tight')
        print(f"✅ Gráfico guardado en: {guardar}")
    else:
        print("📈 Mostrando gráfico...")
        plt.show()


def main():
    """Función principal con argumentos de línea de comandos."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Genera gráficos de evolución de precios PVPC'
    )
    parser.add_argument(
        '--tipo',
        choices=['evolucion', 'dia'],
        default='evolucion',
        help='Tipo de gráfico: "evolucion" (30 días) o "dia" (por hora)'
    )
    parser.add_argument(
        '--dias',
        type=int,
        default=30,
        help='Número de días para gráfico de evolución (default: 30)'
    )
    parser.add_argument(
        '--fecha',
        type=str,
        help='Fecha para gráfico diario (formato: YYYY-MM-DD, default: hoy)'
    )
    parser.add_argument(
        '--guardar',
        type=str,
        help='Guardar gráfico en archivo (ej: grafico.png)'
    )
    
    args = parser.parse_args()
    
    if args.tipo == 'evolucion':
        graficar_evolucion(dias=args.dias, guardar=args.guardar)
    else:
        if args.fecha:
            try:
                fecha = datetime.strptime(args.fecha, '%Y-%m-%d').date()
            except ValueError as e:
                print(f"❌ Error al parsear fecha: {e}")
                sys.exit(1)
        else:
            fecha = datetime.now().date()
        
        graficar_comparacion_diaria(fecha=fecha, guardar=args.guardar)


if __name__ == "__main__":
    main()
