# ☕ Pipeline de Ingesta, Limpieza y Transformación (ETL) - Ventas Starbucks

**Curso:** Data Science II  
**Entregable:** Pre-Entrega 5 - Construcción de un Pipeline de Ingesta y Limpieza  
**Nivel del Entregable:** Principiante Inicial (Nivel 2)  

---

## 📋 Tabla de Contenidos
- [📌 Descripción del Proyecto](#-descripción-del-proyecto)
- [📁 Estructura del Repositorio](#-estructura-del-repositorio)
- [⚙️ Descripción Detallada de las Etapas del Pipeline](#️-descripción-detallada-de-las-etapas-del-pipeline)
  - [1. Extracción (`src/extract.py`)](#1-extracción-srcextractpy)
  - [2. Transformación (`src/transformations.py`)](#2-transformación-srctransformationspy)
  - [3. Carga (`src/load.py`)](#3-carga-srcloadpy)
- [💡 Justificación del Formato Parquet para Machine Learning](#-justificación-del-formato-parquet-para-machine-learning)
- [🛠️ Requisitos e Instalación de Dependencias](#️-requisitos-e-instalación-de-dependencias)
- [🚀 Instrucciones de Ejecución Paso a Paso](#-instrucciones-de-ejecución-paso-a-paso)

---

## 📌 Descripción del Proyecto

El objetivo de esta actividad es diseñar e implementar un **pipeline de datos automatizado (ETL)** aplicando librerías de alto rendimiento como **Pandas** y **PyArrow**. El pipeline procesa un conjunto de datos de transacciones de ventas de Starbucks, aplicando conceptos de **modularización**, **eficiencia en el manejo de volúmenes de datos crecientes** y **buenas prácticas de código**.

---

## 📁 Estructura del Repositorio

El proyecto cumple estrictamente con el principio de modularización, separando el script principal de ejecución de los módulos de lógica interna:

```text
Pre-Entrega 5- Construcción de un Pipeline de Ingesta y Limpieza/
├── main.py                     # Script principal para la ejecución del pipeline
├── src/                        # Paquete con los módulos de lógica modular
│   ├── __init__.py             # Identificador de paquete Python
│   ├── extract.py              # Módulo de Ingesta / Extracción de datos
│   ├── transformations.py      # Módulo independiente de limpieza y transformaciones
│   ├── load.py                 # Módulo de Carga (Exportación a Parquet)
│   └── etl_pipeline.py         # Orquestador que coordina el flujo ETL completo
├── data/                       # Almacenamiento de datos
│   ├── raw/
│   │   └── ventas_starbucks.csv # Dataset original con nulos y duplicados
│   └── output/                 # Archivos finales procesados (generado automáticamente)
│       └── ventas_starbucks_limpio.parquet
├── Objetivos de la pre-entrega.md
├── requirements.txt            # Dependencias necesarias para ejecutar el proyecto
├── .gitignore                  # Archivos ignorados por Git
└── README.md                   # Documentación técnica completa
```

---

## ⚙️ Descripción Detallada de las Etapas del Pipeline

### 1. Extracción (`src/extract.py`)
- **Función:** `extraer_datos_csv(filepath)`
- **Descripción:** Se encarga de la ingesta modular del archivo CSV localizado en `data/raw/ventas_starbucks.csv`. Verifica la existencia del archivo de origen y lo carga en un DataFrame de Pandas reportando la cantidad inicial de filas y columnas.

### 2. Transformación (`src/transformations.py`)
Contiene la lógica de limpieza dividida en funciones independientes:
- **Normalización de Nombres de Columnas (`normalizar_nombres_columnas`)**:
  - Convierte todos los encabezados a minúsculas, remueve acentos/tildes y sustituye espacios por guiones bajos (`snake_case`).
  - *Justificación:* Previene errores tipográficos y facilita el acceso programático a las columnas.
- **Remoción de Duplicados (`eliminar_duplicados`)**:
  - Detecta y elimina filas idénticas usando `drop_duplicates()`.
  - *Justificación:* Evita distorsiones estadísticas e ingresos sobreestimados en el análisis financiero.
- **Tratamiento Justificado de Valores Nulos (`gestionar_valores_nulos`)**:
  - **`monto_total`**: Se imputa calculando `precio_unitario * cantidad`. *Justificación:* Es una relación matemática exacta que permite recuperar el dato factual sin descartar la transacción.
  - **`categoria`**: Se imputa con la etiqueta `'Sin Categoría'`. *Justificación:* Permite mantener el registro de venta sin perder información cuantitativa.
  - **`metodo_pago`**: Se imputa con la etiqueta `'No Especificado'`. *Justificación:* Conserva la trazabilidad del ticket de compra.
- **Formateo de Fechas**: Conversión de la columna `fecha` al tipo de dato `datetime64[ns]`.

### 3. Carga (`src/load.py`)
- **Función:** `cargar_datos_parquet(df, output_path)`
- **Descripción:** Crea la carpeta de salida si no existe y exporta el DataFrame procesado a un archivo comprimido Parquet (`data/output/ventas_starbucks_limpio.parquet`).

---

## 💡 Justificación del Formato Parquet para Machine Learning

El formato **Parquet** es el estándar moderno en Data Science y Machine Learning debido a:

1. **Almacenamiento Orientado a Columnas (Columnar Storage)**: Permite leer únicamente las características (*features*) necesarias para entrenar un modelo sin cargar todo el dataset en memoria RAM.
2. **Preservación Integrada del Esquema**: Mantiene los tipos de datos exactos (`datetime`, `int64`, `float64`), evitando errores de casteo al recargar con Pandas o Scikit-Learn.
3. **Alta Compresión y Eficiencia de I/O**: Reduce el tamaño del archivo hasta en un 80% mediante compresión Snappy, disminuyendo costos de almacenamiento y agilizando la transferencia en red.
4. **Compatibilidad con Big Data**: Integración nativa con Apache Spark, Dask, Polars y DuckDB.

---

## 🛠️ Requisitos e Instalación de Dependencias

### Prerrequisitos
- Python 3.8 o superior instalado.

### Paso 1: Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/REPOSITORIO.git
cd REPOSITORIO
```

### Paso 2: Crear e iniciar un entorno virtual (Opcional recomendado)
En Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### Paso 3: Instalar dependencias
```bash
pip install -r requirements.txt
```

---

## 🚀 Instrucciones de Ejecución Paso a Paso

Para ejecutar el pipeline de principio a fin, corre el script `main.py` en la raíz del proyecto:

```bash
python main.py
```

### Salida esperada en la consola:
```text
============================================================
 INICIANDO EJECUCIÓN DEL PIPELINE ETL (VENTAS STARBUCKS)
============================================================
[EXTRACCIÓN] Leyendo datos desde el origen CSV: '.../data/raw/ventas_starbucks.csv'...
[EXTRACCIÓN] ✓ Ingesta exitosa: 14 filas y 9 columnas leídas.

--- INICIO DE ETAPA DE TRANSFORMACIÓN ---
[NORMALIZACIÓN] Nombres de columnas normalizados a snake_case: ['transaction_id', 'fecha', 'tienda_id', 'producto', 'categoria', 'precio_unitario', 'cantidad', 'monto_total', 'metodo_pago']
[DUPLICADOS] Registros duplicados detectados: 2
[DUPLICADOS] 2 registros duplicados eliminados exitosamente.
[NULOS] Conteo inicial de valores nulos por columna:
  - Columna 'categoria': 1 nulos
  - Columna 'monto_total': 2 nulos
  - Columna 'metodo_pago': 1 nulos
  ✓ [IMPUTACIÓN CALCULADA] Imputados 2 valores en 'monto_total' mediante (precio_unitario * cantidad).
  ✓ [IMPUTACIÓN CATEGÓRICA] Imputados 1 valores en 'categoria' como 'Sin Categoría'.
  ✓ [IMPUTACIÓN CATEGÓRICA] Imputados 1 valores en 'metodo_pago' como 'No Especificado'.
--- FIN DE ETAPA DE TRANSFORMACIÓN ---

[CARGA] Exportando datos procesados a formato Parquet en: '.../data/output/ventas_starbucks_limpio.parquet'...
[CARGA] ✓ Carga finalizada correctamente. Archivo '.parquet' generado.
============================================================
 ¡Pipeline finalizado con éxito!
 Total de registros procesados y guardados: 12
============================================================
```

El archivo Parquet procesado estará listo en `data/output/ventas_starbucks_limpio.parquet`.
