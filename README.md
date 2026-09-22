# Pipeline de Ingesta, Limpieza y Transformación (ETL) - Ventas Starbucks

**Curso:** Data Science II  
**Entregable:** Pre-Entrega 5 - Construcción de un Pipeline de Ingesta y Limpieza  
**Nivel:** Principiante Inicial  

---

## 📌 Descripción del Proyecto

Este proyecto consiste en el diseño e implementación de un **Pipeline de Datos ETL automatizado** en Python utilizando **Pandas** y **PyArrow**. El pipeline procesa transacciones de ventas de Starbucks mediante módulos desacoplados para:
1. **Extracción**: Lectura modular de archivos CSV de origen.
2. **Transformación**:
   - Normalización de encabezados a formato `snake_case`.
   - Remoción de registros duplicados.
   - Imputación justificada de valores nulos.
3. **Carga**: Exportación optimizada en formato **Parquet**.

---

## 📁 Estructura Modular del Repositorio

```text
├── main.py                     # Script principal de ejecución del pipeline
├── src/                        # Módulos de lógica modular del pipeline
│   ├── __init__.py             # Inicializador de paquete Python
│   ├── extract.py              # Módulo de Extracción (Ingesta desde CSV)
│   ├── transformations.py      # Módulo de Transformaciones (Limpieza, nulos y duplicados)
│   ├── load.py                 # Módulo de Carga (Exportación a Parquet con justificación ML)
│   └── etl_pipeline.py         # Orquestador del flujo ETL
├── data/                       # Gestión de datos (Raw y Output)
│   ├── raw/
│   │   └── ventas_starbucks.csv # Dataset original con nulos y duplicados
│   └── output/                 # Salida procesada en formato Parquet
├── Objetivos de la pre-entrega.md
├── requirements.txt            # Dependencias del proyecto (pandas, pyarrow)
├── .gitignore                  # Reglas de exclusión de Git
└── README.md                   # Documentación técnica del proyecto
```

---

## 💡 ¿Por qué Parquet es más eficiente para Machine Learning?

El formato **Parquet** ofrece ventajas críticas sobre formatos tradicionales orientados a texto como CSV o JSON cuando se preparan datos para modelos de **Machine Learning**:

1. **Almacenamiento Orientado a Columnas (Columnar Storage)**:
   - CSV guarda los datos fila por fila. Si un modelo de ML requiere entrenar solo con 5 características (*features*) de una tabla de 100 columnas, un CSV obliga a leer las 100 columnas del disco.
   - Parquet permite realizar *projection pushdown*, leyendo del disco **únicamente las columnas necesarias**, reduciendo radicalmente el uso de memoria RAM y el tiempo de lectura (I/O).

2. **Preservación del Esquema y Tipos de Datos**:
   - Guarda el esquema en metadatos binarios (tipos `datetime`, `int64`, `float64`).
   - Evita la necesidad de re-inferir tipos o castear cadenas a números cada vez que se carga el dataset en Pandas, Scikit-Learn o PyTorch, previniendo errores de precisión.

3. **Alta Compresión por Columna**:
   - Al agrupar valores del mismo tipo de dato en bloques contiguos, Parquet logra tasas de compresión de hasta un 75%-80% mediante algoritmos como Snappy o Gzip.
   - Esto reduce drásticamente el costo de almacenamiento en la nube (ej. AWS S3) y acelera las transferencias por red.

4. **Compatibilidad con Marcos de Computación Distribuida**:
   - Es el estándar nativo para herramientas de alto rendimiento y Big Data como **Apache Spark**, **Dask**, **Polars** y **DuckDB**, permitiendo entrenamiento distribuido y procesamiento en paralelo sin cuellos de botella.

---

## 🛠️ Instalación de Dependencias

Para instalar las dependencias requeridas en tu entorno virtual:

```bash
pip install -r requirements.txt
```

---

## 🚀 Instrucciones de Ejecución

Ejecuta el script principal desde la raíz del repositorio:

```bash
python main.py
```

Al finalizar la ejecución, el script mostrará en consola el reporte de ingesta, transformación y la justificación de carga, generando el archivo Parquet en `data/output/ventas_starbucks_limpio.parquet`.
