# 🌳 TreeBench: Benchmark de Estructuras Arbóreas

## 📖 Descripción General

**TreeBench** es un sistema de evaluación comparativa que analiza el rendimiento de cuatro estructuras de datos arbóreas:

- **Árbol AVL** (balanceado por altura)
- **Árbol B** (estructura multiway)
- **Árbol B+** (variante optimizada para discos)
- **Árbol B*** (versión con redistribución mejorada)

El sistema mide científicamente el tiempo de ejecución de tres operaciones fundamentales:
1. **Inserción** de pares (ID, nombre)
2. **Búsqueda** por ID
3. **Eliminación** de nodos

## 🔬 Métricas de Análisis

| Métrica               | Descripción                                  |
|-----------------------|--------------------------------------------|
| ⏱️ Tiempos por operación | Registro individual con precisión de microsegundos |
| 📊 Promedios          | Cálculo por tipo de operación y estructura |
| 🏆 Top 10             | Operaciones más rápidas y más lentas       |
| 📝 Logs detallados    | Traza completa con timestamps y resultados |

## 📂 Flujo de Trabajo

```mermaid
graph TD
    A[Archivo de operaciones] --> B{Procesamiento}
    B --> C[AVL]
    B --> D[Árbol B]
    B --> E[Árbol B+]
    B --> F[Árbol B*]
    C --> G[Generar logs]
    D --> G
    E --> G
    F --> G
    G --> H[Reporte comparativo]
