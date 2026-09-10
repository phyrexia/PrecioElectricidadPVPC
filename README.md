<div align="center">
  <img src=".github/quantum-hero.png" alt="Quantum AI Foundry" width="100%"/>
</div>

<!-- ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ -->

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:120024,50:4c1d95,100:7c3aed&height=210&section=header&text=PrecioElectricidadPVPC&fontSize=52&fontColor=ffffff&fontAlignY=38&desc=Consulta%2C%20almacena%20y%20visualiza%20precios%20PVPC%20de%20la%20luz%20%28ESIOS%29&descSize=20&descAlignY=60" alt="PrecioElectricidadPVPC" width="100%"/>

### Python · ESIOS · gráficos · backfill

<br/>

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/ESIOS-7c3aed?style=for-the-badge"/>
<img src="https://img.shields.io/badge/open-source-16a34a?style=for-the-badge"/>

<a href="#precioelectricidadpvpc">
<img src="https://img.shields.io/badge/⚡%20Powered%20by-QUANTUM-7c3aed?style=for-the-badge&labelColor=120024"/>
</a>

<br/><br/>

<img src="https://skillicons.dev/icons?i=py,github,git,md&theme=dark" alt="stack"/>

</div>

<!-- ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ -->

---

## ⚡ Mantenido y evolucionado por **Quantum**

> **PrecioElectricidadPVPC** es un sistema completo para consultar, almacenar y visualizar los precios PVPC de la electricidad (ESIOS) en España.

<div align="center">

`ESIOS &nbsp;→&nbsp; consulta &nbsp;→&nbsp; almacenamiento &nbsp;→&nbsp; **gráficos**` ⚡

</div>

---

## 🚕 ¿Qué es?

**PrecioElectricidadPVPC** (repo `PrecioElectricidadPVPC`) consulta los precios PVPC de la luz desde ESIOS, los almacena y genera visualizaciones. Es un proyecto open-source (Python) popular.

## ✨ ¿Qué hace?

| | Área | Qué resuelve |
|:--:|------|--------------|
| 🔌 | **Consulta** | Precios PVPC desde ESIOS. |
| 💾 | **Almacenamiento** | Persistencia de precios. |
| 📈 | **Gráficos** | Visualización de precios. |
| ⏪ | **Backfill** | `backfill.py` rellena histórico. |

## 🏗️ Cómo está construido

ESIOS → consulta → almacenamiento → gráficos:

```mermaid
flowchart LR
    ESIOS["🔌 ESIOS"] --> CONS["consultar.py"]
    CONS --> STORE[("💾 datos")]
    STORE --> GRAF["📈 graficar.py"]
    BACK["⏪ backfill.py"] --> STORE
    classDef q fill:#4c1d95,stroke:#7c3aed,color:#fff;
    classDef d fill:#120024,stroke:#7c3aed,color:#fff;
    classDef g fill:#16a34a,stroke:#065f46,color:#fff;
    class CONS q; class STORE d; class ESIOS,GRAF,BACK g;
```

**Stack**

- **Lenguaje** — Python.
- **Fuente** — ESIOS (PVPC).

## 📂 Estructura del repositorio

| Ruta | Contenido |
|------|-----------|
| `consultar.py · backfill.py · graficar.py · main.py` | CLI principal. |
| `src/` | Lógica. |
| `docs/` | Documentación. |

## 🔗 Integraciones

- **ESIOS** — API de precios PVPC.

## 🚀 Entornos y despliegue

- Local / cron para consultas y backfill.

## 💜 Lo que Quantum ha aportado

<div align="center">

| | | |
|:--:|:--:|:--:|
| 🔌 **Consulta** | 📈 **Visualización** |
| ESIOS PVPC,<br/>backfill | Gráficos |

</div>

## 🌟 Hacia dónde va

```mermaid
flowchart LR
    A["🔌 Consulta"] --> B["📈 Visualización"]
    B --> C["✨ Sistema<br/>completo"]
    classDef done fill:#16a34a,stroke:#065f46,color:#fff;
    classDef now fill:#7c3aed,stroke:#4c1d95,color:#fff;
    classDef next fill:#120024,stroke:#7c3aed,color:#fff;
    class A done; class B now; class C next;
```

- Dashboard web.

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:7c3aed,50:4c1d95,100:120024&height=120&section=footer&text=Cuidado%20y%20llevado%20al%20siguiente%20nivel%20por%20Quantum&fontSize=20&fontColor=ffffff&fontAlignY=70" alt="Quantum" width="100%"/>

**PrecioElectricidadPVPC** — precios de la luz, hechos crecer por **Quantum** ⚡

</div>
