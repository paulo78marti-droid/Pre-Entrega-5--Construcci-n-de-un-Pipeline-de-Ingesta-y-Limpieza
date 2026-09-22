# Pipeline de Ingesta, Limpieza y Transformación (ETL) - Ventas Starbucks

**Curso:** Data Science II  
**Entregable:** Pre-Entrega 5 - Construcción de un Pipeline de Ingesta y Limpieza  
**Nivel:** Principiante Inicial  

---

## 📌 Descripción del Proyecto

Este proyecto consiste en el diseño e implementación de un **Pipeline de Datos ETL automatizado** utilizando **Pandas**. El pipeline procesa datos de transacciones de ventas de Starbucks, aplicando transformaciones para la limpieza de registros duplicados, tratamiento de valores nulos e imputación de datos faltantes, y finalmente exporta los resultados limpios en formato comprimido y eficiente **Parquet**.

---

## 📁 Estructura del Repositorio

```text
├── main.py                     # Script principal de ejecución del pipeline
├── src/                        # Módulos de lógica modular del pipeline
│   ├── __init__.py             # Inicializador de paquete Python
│   └── etl_pipeline.py         # Funciones modulares de Extracción, Transformación y Carga
├── data/                       # Gestión de datos (Raw y Output)
│   ├── raw/
│   │   └── ventas_starbucks.csv # Dataset original de ventas
│   └── output/                 # Salida generada por el script (Parquet)
├── Objetivos de la pre-entrega.md
├── requirements.txt            # Dependencias del proyecto
├── .gitignore                  # Exclusiones para control de versiones Git
└── README.md                   # Documentación técnica del repositorio
```

---

## ⚙️ Etapas del Pipeline ETL

1. **Extracción (`extraer_datos`)**:
   - Ingesta del archivo CSV localizado en `data/raw/ventas_starbucks.csv`.
2. **Transformación (`transformar_datos`)**:
   - **Eliminación de duplicados**: Detección y remoción de filas exactamente iguales (`drop_duplicates`).
   - **Tratamiento de valores nulos**:
     - Imputación de `monto_total` calculando `precio_unitario * cantidad`.
     - Imputación de columnas categóricas (`categoria` -> `'Sin Categoría'`, `metodo_pago` -> `'No Especificado'`).
   - **Casteo de tipos**: Conversión de columna `fecha` a formato `datetime`.
3. **Carga (`cargar_datos`)**:
   - Creación automática del directorio de salida y guardado del DataFrame resultante en formato de alto rendimiento **Parquet** (`.parquet`).

---

## 🛠️ Instalación de Dependencias

Se recomienda utilizar un entorno virtual de Python. Para instalar las dependencias requeridas, ejecuta:

```bash
pip install -r requirements.txt
```

Las dependencias principales son:
- `pandas`
- `pyarrow` (requerido para soporte con archivos `.parquet`)

---

## 🚀 Instrucciones de Ejecución

Para correr el pipeline ETL completo, ejecuta el archivo principal `main.py` desde la raíz del proyecto:

```bash
python main.py
```

Al finalizar, el script mostrará en consola el reporte de limpieza y generará el archivo Parquet en `data/output/ventas_starbucks_limpio.parquet`.
