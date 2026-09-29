# ☕ Pipeline de Ingesta, Limpieza y Transformación (ETL) - Ventas Starbucks

**Curso:** Data Science II  
**Entregable:** Pre-Entrega 5 - Construcción de un Pipeline de Ingesta y Limpieza  
**Nivel del Entregable:** Principiante Inicial (Nivel 2)  
**Repositorio GitHub:** [https://github.com/nacho1907/etl-pipeline](https://github.com/nacho1907/etl-pipeline)

---

## 📌 Descripción del Proyecto

Este proyecto consiste en la implementación de un **Pipeline ETL (Extracción, Transformación y Carga)** modular en Python para procesar datos de ventas de Starbucks.

El objetivo principal es demostrar las buenas prácticas en la estructuración de proyectos de ciencia de datos:
- **Modularización**: Separación del código en funciones y módulos reutilizables (`src/`).
- **Eficiencia y Limpieza**: Manejo explícito de valores nulos, eliminación de filas duplicadas y normalización de nombres de columnas.
- **Exportación en Parquet**: Uso del formato binario columnar Parquet optimizado para Machine Learning.

---

## 📁 Estructura del Repositorio

```text
etl-pipeline/
├── data/
│   ├── raw/                      # Archivo CSV de origen (dataset no procesado)
│   │   └── ventas_starbucks.csv
│   └── output/                   # Archivo Parquet generado por el pipeline
│       └── ventas_starbucks_limpio.parquet
├── src/                          # Módulos de lógica ETL modular
│   ├── __init__.py
│   ├── extract.py                # Extracción desde fuente CSV
│   ├── transformations.py        # Limpieza, deduplicación y tratamiento de nulos
│   ├── load.py                   # Carga e inmunización en formato Parquet
│   └── etl_pipeline.py           # Orquestador del pipeline completo
├── main.py                       # Script principal de ejecución
├── pipeline_colab.py             # Versión para Google Colab con descarga automática (Kaggle)
├── requirements.txt              # Dependencias del proyecto
├── .gitignore                    # Archivos y datos excluidos del repositorio
└── README.md                     # Documentación técnica del proyecto
```

---

## ⚙️ Descripción Detallada de las Etapas del Pipeline

### 1. Extracción (`src/extract.py`)
- Carga el dataset original en formato CSV mediante **Pandas**.
- Incluye validaciones de existencia del archivo y reporta el consumo de memoria RAM.

### 2. Transformación (`src/transformations.py`)
- **Normalización de Nombres de Columnas**: Convierte todos los encabezados a formato `snake_case`, minúsculas, sin espacios extras ni acentos (ejemplo: `Categoría_Producto` ➡️ `categoria_producto`).
- **Eliminación de Duplicados**: Detecta y remueve filas idénticas redundantes mediante `drop_duplicates()`.
- **Tratamiento Justificado de Valores Nulos**:
  - Imputación calculada: En registros donde falta `total_venta`, se calcula como `precio_unitario * cantidad`.
  - Imputación categórica: Variables como `categoria_producto` o `metodo_de_pago` con valores faltantes se imputan como `'No Especificado'`.
  - Conversión de tipos de datos: Se castea la columna `fecha` a `datetime`.

### 3. Carga (`src/load.py`)
- Exporta el DataFrame procesado a un archivo `.parquet` ubicado en `data/output/ventas_starbucks_limpio.parquet`.

---

## 💡 Justificación del Formato Parquet para Machine Learning

El uso de **Parquet** ofrece importantes ventajas sobre el tradicional **CSV** en proyectos de Machine Learning:

1. **Almacenamiento Columnar**: Permite leer únicamente las características (*features*) necesarias para el modelo de ML, reduciendo drásticamente el uso de memoria RAM e I/O de disco.
2. **Preservación de Esquema y Tipos de Datos**: Mantiene los tipos exactos de datos (enteros, flotantes, fechas, texto) sin necesidad de volver a inferirlos al recargar los datos.
3. **Alta Compresión**: Reduce el peso de los datos en un 70% a 80% utilizando compresión columnar (ej. Snappy).
4. **Compatibilidad con Big Data**: Es el estándar de la industria soportado por Pandas, PyArrow, Dask, Polars y PySpark.

---

## 🛠️ Requisitos e Instalación de Dependencias

### Requisitos previos
- Python 3.8 o superior.

### Pasos de instalación
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/nacho1907/etl-pipeline.git
   cd etl-pipeline
   ```
2. Instalar las librerías necesarias:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Instrucciones de Ejecución Paso a Paso

Para ejecutar el pipeline ETL completo, basta con correr el archivo `main.py` desde la raíz del repositorio:

```bash
python main.py
```

### Salida esperada en consola:
```text
==================================================
 ☕ PIPELINE ETL - PROCESAMIENTO DE VENTAS STARBUCKS
==================================================

============================================================
 INICIANDO EJECUCIÓN DEL PIPELINE ETL (VENTAS STARBUCKS)
============================================================
[EXTRACCIÓN] Leyendo datos desde el origen CSV: '.../data/raw/ventas_starbucks.csv'...
[EXTRACCIÓN] ✓ Ingesta exitosa: 5000 filas y 21 columnas leídas.

--- INICIO DE ETAPA DE TRANSFORMACIÓN ---
[TRANSFORMACIÓN] Columnas normalizadas a snake_case.
[TRANSFORMACIÓN] ✓ Registros duplicados eliminados.
  ✓ Imputados valores nulos en 'total_venta' calculando (precio_unitario * cantidad).
  ✓ Imputados valores nulos en categóricas como 'No Especificado'.
  ✓ Columna 'fecha' parseada correctamente a formato datetime.
--- FIN DE ETAPA DE TRANSFORMACIÓN ---

[CARGA] Exportando datos procesados a Parquet en: '.../data/output/ventas_starbucks_limpio.parquet'...
[CARGA] ✓ Carga exitosa. Archivo Parquet generado.
==================================================
 ¡Pipeline finalizado con éxito!
 Registros totales limpios y guardados: 5000
==================================================
```
