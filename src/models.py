"""
Modelos de datos y lógica de procesamiento.
"""

from dataclasses import dataclass
from datetime import datetime, date
from typing import List, Dict, Any


@dataclass
class PricePoint:
    """Representa un punto de precio PVPC."""
    fecha: date
    hora: int
    precio: float  # €/MWh
    tramo: str = None  # 'verde', 'amarillo', 'rojo'
    
    def __str__(self) -> str:
        emoji = {'verde': '🟢', 'amarillo': '🟡', 'rojo': '🔴'}.get(self.tramo, '⚪')
        return f"{self.hora:02d}-{self.hora+1:02d} │ {self.precio:8.5f} │ {emoji} {self.tramo or 'N/A'}"


def parse_esios_response(data: Dict[str, Any], geo_id: int = 8741) -> List[PricePoint]:
    """
    Parsea la respuesta JSON de ESIOS y extrae los precios.
    
    Args:
        data: Respuesta JSON de la API de ESIOS
        geo_id: ID de geografía (8741=Península, 8742=Canarias, 8743=Baleares, 8744=Ceuta, 8745=Melilla)
        
    Returns:
        Lista de PricePoint
    """
    prices = []
    
    # La estructura de ESIOS es: indicator -> values -> [{datetime, value, geo_id}]
    if 'indicator' not in data:
        return prices
    
    indicator = data['indicator']
    if 'values' not in indicator:
        return prices
    
    for entry in indicator['values']:
        # Filtrar solo por geografía deseada (por defecto Península)
        if entry.get('geo_id') != geo_id:
            continue
        
        # Parsear datetime (formato ISO: "2026-02-19T00:00:00.000+01:00")
        dt_str = entry['datetime']
        # Manejar diferentes formatos de zona horaria
        dt_str = dt_str.replace('+01:00', '+0100').replace('+02:00', '+0200')
        dt = datetime.fromisoformat(dt_str)
        
        # Extraer valor (viene en €/MWh)
        # Para PVPC viene en €/MWh, convertir a €/kWh
        value = float(entry['value']) / 1000
        
        # Crear PricePoint
        prices.append(PricePoint(
            fecha=dt.date(),
            hora=dt.hour,
            precio=value
        ))
    
    return prices


def calculate_tramos(prices: List[PricePoint]) -> List[PricePoint]:
    """
    Calcula los tramos (verde/amarillo/rojo) basándose en los precios del día.
    
    Divide las 24 horas en 3 tramos:
    - Verde: tercio inferior (8 horas más baratas)
    - Amarillo: tercio medio (8 horas intermedias)
    - Rojo: tercio superior (8 horas más caras)
    
    Args:
        prices: Lista de PricePoint sin tramos asignados
        
    Returns:
        Lista de PricePoint con tramos asignados
    """
    if not prices:
        return prices
    
    # Ordenar por precio
    sorted_prices = sorted(prices, key=lambda p: p.precio)
    
    # Calcular índices de corte (tercios)
    n = len(sorted_prices)
    tercio = n // 3
    
    # Asignar tramos
    for i, price in enumerate(sorted_prices):
        if i < tercio:
            price.tramo = 'verde'
        elif i < 2 * tercio:
            price.tramo = 'amarillo'
        else:
            price.tramo = 'rojo'
    
    # Devolver en orden original (por hora)
    return sorted(prices, key=lambda p: p.hora)


def format_price_table(prices: List[PricePoint], fecha: date) -> str:
    """
    Formatea una tabla bonita con los precios del día.
    
    Args:
        prices: Lista de PricePoint con tramos
        fecha: Fecha de los precios
        
    Returns:
        String con la tabla formateada
    """
    if not prices:
        return f"No hay datos para {fecha.strftime('%d/%m/%Y')}"
    
    lines = []
    lines.append(f"\nPrecios PVPC - {fecha.strftime('%d/%m/%Y')}")
    lines.append("═" * 50)
    lines.append("Hora  │ Precio (€/kWh) │ Tramo")
    lines.append("──────┼────────────────┼───────────")
    
    for price in prices:
        lines.append(str(price))
    
    lines.append("═" * 50)
    
    # Estadísticas
    precios_valores = [p.precio for p in prices]
    min_precio = min(prices, key=lambda p: p.precio)
    max_precio = max(prices, key=lambda p: p.precio)
    media = sum(precios_valores) / len(precios_valores)
    
    lines.append(f"💚 Hora más barata: {min_precio.hora:02d}-{min_precio.hora+1:02d} → {min_precio.precio:.5f} €/kWh")
    lines.append(f"🔴 Hora más cara:   {max_precio.hora:02d}-{max_precio.hora+1:02d} → {max_precio.precio:.5f} €/kWh")
    lines.append(f"📊 Precio medio:    {media:.5f} €/kWh")
    lines.append("")
    
    return "\n".join(lines)
