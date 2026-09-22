# Pipeline de Ingesta, Limpieza y Transformación (ETL) - Ventas Starbucks

**Curso:** Data Science II  
**Entregable:** Pre-Entrega 5 - Construcción de un Pipeline de Ingesta y Limpieza  
**Nivel:** Principiante Inicial  

---

## 📌 Descripción del Proyecto

Este proyecto consiste en el diseño e implementación de un **Pipeline de Datos ETL automatizado** en Python utilizando **Pandas**. El pipeline procesa un dataset de transacciones de ventas de Starbucks, aplicando etapas modulares para:
1. Normalización de nombres de columnas (formato `snake_case`).
2. Remoción justificada de registros duplicados.
3. Gestión e imputación justificada de valores nulos.
4. Exportación final de datos procesados en formato comprimido de alto rendimiento **Parquet**.

---

## 📁 Estructura Modular del Repositorio

```text
├── main.py                     # Script principal para ejecución del pipeline
├── src/                        # Módulos de lógica del pipeline
│   ├── __init__.py             # Inicializador de paquete Python
│   ├── etl_pipeline.py         # Coordinador de etapas ETL (Extracción y Carga)
│   └── transformations.py      # Módulo independiente de limpieza y transformaciones
├── data/                       # Gestión de datos
│   ├── raw/
│   │   └── ventas_starbucks.csv # Dataset original con nulos y duplicados
│   └── output/                 # Salida procesada en formato Parquet
├── Objetivos de la pre-entrega.md
├── requirements.txt            # Dependencias del proyecto (pandas, pyarrow)
├── .gitignore                  # Reglas de exclusión de Git
└── README.md                   # Documentación técnica del proyecto
```

---

## ⚙️ Funciones de Transformación y Justificaciones (`src/transformations.py`)

La lógica de transformación se encuentra encapsulada en funciones independientes dentro del módulo `src/transformations.py`:

- **`normalizar_nombres_columnas`**:
  - Convierte nombres de columnas a minúsculas, remueve espacios y tildes, aplicando formato `snake_case`.
  - *Justificación*: Previene errores de sintaxis y asegura consistencia programática.
- **`eliminar_duplicados`**:
  - Identifica y elimina filas idénticas mediante `drop_duplicates()`.
  - *Justificación*: Evita la sobreestimación de ventas e ingresos en métricas financieras.
- **`gestionar_valores_nulos`**:
  - `monto_total`: Imputado derivando dinámicamente el producto `precio_unitario * cantidad`.
  - `categoria`: Imputado con `'Sin Categoría'`.
  - `metodo_pago`: Imputado con `'No Especificado'`.
  - *Justificación*: Permite recuperar información fáctica exacta sin descartar transacciones válidas para análisis.

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

Al finalizar la ejecución, se mostrará en consola el detalle del proceso de limpieza y se generará el archivo `data/output/ventas_starbucks_limpio.parquet`.
