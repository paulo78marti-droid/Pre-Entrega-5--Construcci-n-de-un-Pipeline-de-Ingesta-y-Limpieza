# Pipeline ETL de Ingesta y Limpieza de Datos

**Curso:** Data Science II  
**Entregable:** Pre-Entrega 5 - Construcción de un Pipeline de Ingesta y Limpieza  
**Autor:** Estudiante Data Science II  

---

## 📌 Descripción del Proyecto

Este proyecto consiste en un **Pipeline de Extracción, Transformación y Carga (ETL)** modular y automatizado, desarrollado en Python utilizando la librería **Pandas**. 

El objetivo principal es tomar un conjunto de datos crudos sobre transacciones de ventas (*E-commerce / Retail*), automatizar su ingesta, corregir problemas de calidad de datos (nombres de columnas irregulares, duplicados y valores nulos) y exportar el resultado limpio en un archivo de alta eficiencia en formato **Parquet**.

---

## 🛠️ Estructura Modular del Proyecto

La estructura del código sigue las mejores prácticas de desarrollo modular en Data Science:

```text
├── data/
│   ├── raw/                      # Datos crudos de entrada (ventas_retail_raw.csv)
│   └── processed/                # Datos limpios resultantes (ventas_retail_limpio.parquet)
├── src/
│   ├── __init__.py               # Inicializador del paquete Python
│   ├── extract.py                # Módulo de Extracción (lectura de datos)
│   ├── transform.py              # Módulo de Transformación (normalización y limpieza)
│   └── load.py                   # Módulo de Carga (exportación a Parquet)
├── main.py                       # Script principal de ejecución del Pipeline
├── requirements.txt              # Dependencias del proyecto
└── README.md                     # Documentación técnica
```

---

## ⚙️ Requisitos e Instalación

### 1. Clonar el Repositorio
```bash
git clone <URL_DE_TU_REPOSITORIO_EN_GITHUB>
cd "Pre-Entrega 5- Construcción de un Pipeline de Ingesta y Limpieza"
```

### 2. Crear un Entorno Virtual (Opcional pero recomendado)
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

---

## 🚀 Ejecución del Pipeline

Para ejecutar el pipeline completo de inicio a fin, corre el siguiente comando en la terminal:

```bash
python main.py
```

Al finalizar la ejecución, el script imprimirá en pantalla el progreso de cada etapa y generará el archivo final limpio en `data/processed/ventas_retail_limpio.parquet`.

---

## 🔍 Explicación Técnica de las Etapas del Pipeline

### 1. Extracción (`src/extract.py`)
- La función `extract_data()` lee el archivo CSV de entrada (`data/raw/ventas_retail_raw.csv`).
- Informa las dimensiones iniciales (filas y columnas) y calcula el uso aproximado de memoria RAM en MB.

### 2. Transformación (`src/transform.py`)
La función `transform_data()` aplica una secuencia de reglas de calidad de datos:

- **Normalización de encabezados:**
  - Convierte los nombres de columnas a minúsculas.
  - Remueve espacios adicionales y caracteres especiales (`$`, `()`, etc.).
  - Reemplaza los espacios por guiones bajos (`_`). Ejemplo: ` Price ($) ` $\rightarrow$ `price`.
- **Tratamiento de Duplicados:**
  - Identifica filas totalmente repetidas y las elimina conservando solo la primera ocurrencia con `.drop_duplicates()`.
- **Tratamiento de Valores Nulos (Justificado):**
  - **Identificadores principales (`id`):** Se eliminan filas sin ID válido (`.dropna()`), ya que no pueden atribuirse a ninguna transacción legítima.
  - **Variables Numéricas (`precio_unitario`, `cantidad`):** Se imputan los datos faltantes con la **mediana** de la columna. Se elige la mediana en lugar de la media para evitar que valores extremos (*outliers*) distorsionen los datos imputados.
  - **Variables Categóricas (`categoria_producto`, `metodo_pago`):** Se reemplazan los valores nulos con la etiqueta `'Desconocido'`, preservando el resto del registro sin perder información valiosa de la transacción.

### 3. Carga (`src/load.py`)
- La función `load_data()` exporta el DataFrame transformado a un archivo en formato **Parquet** dentro de `data/processed/ventas_retail_limpio.parquet`.

---

## 💡 ¿Por qué exportar a formato Parquet para Machine Learning?

En proyectos de Data Science e Inteligencia Artificial, el formato **Parquet** ofrece importantes ventajas sobre **CSV**:

1. **Almacenamiento Columnar y Compresión:** A diferencia de CSV (orientado a filas), Parquet organiza los datos por columnas. Esto permite aplicar algoritmos de compresión muy potentes (como Snappy), reduciendo drásticamente el espacio en disco.
2. **Mayor Velocidad de Lectura:** Al entrenar modelos de Machine Learning, los algoritmos suelen consultar únicamente un subconjunto de columnas. Parquet permite leer en memoria solo las columnas requeridas sin necesidad de escanear todo el dataset.
3. **Preservación de Tipos de Datos (Esquema Nativo):** CSV guarda todo como texto simple, obligando a redefinir tipos de datos al volver a cargarlo. Parquet conserva nativamente los tipos de datos (enteros, flotantes, fechas, categóricos).
