# Sistema de Precios PVPC - ESIOS

Sistema completo para consultar, almacenar y visualizar precios del Precio Voluntario para el Pequeño Consumidor (PVPC) de España usando la API de ESIOS (Red Eléctrica de España).

## Qué resuelve

Obtener histórico de precios de electricidad españoles mediante la API ESIOS, almacenarlos localmente y generar gráficos para análisis de patrones y previsión de costos de energía.

## Para quién

Consumidores españoles de electricidad interesados en entender y analizar patrones de precios, especialmente bajo el sistema PVPC.

## Requisitos

- Python 3.7+
- SQLite (incluido en Python)

## Cómo instalar

```bash
git clone <repo>
cd PrecioElectricidadPVPC
pip install -r requirements.txt
cp .env.example .env
```

## Cómo correr

Los scripts principales son:

```bash
# Consultar precios actuales
python consultar.py

# Llenar histórico desde el inicio (puede tomar tiempo)
python backfill.py

# Generar gráficos
python graficar.py

# Script principal (ejecuta consulta periódica)
python main.py
```

## Cómo probar

No hay tests automáticos. Se prueba manualmente ejecutando los scripts contra la API de ESIOS.

## Estructura

```
src/               # Módulos principales
consultar.py       # CLI para consultar precios actuales
backfill.py        # Script para llenar histórico
graficar.py        # Generación de gráficos
main.py            # Ejecución periódica
requirements.txt   # Dependencias (mínimas)
.env.example       # Plantilla de configuración
```

## Stack

Python, SQLite, API ESIOS

## Estado

Archivado (última actividad: 2026-02-19)

Última actividad: 2026-02-19

## Configuración

Editar `.env`:
```
ESIOS_API_KEY=tu_key_aqui
DB_PATH=./precios.db
```

## Notas

Proyecto educativo de 2015. Mantiene histórico de precios españoles del PVPC. La API ESIOS requiere clave de acceso.

## Relacionado con

Red Eléctrica de España (REE), ESIOS API
