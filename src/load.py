"""
Módulo de Carga (Load) para el Pipeline ETL.
Encargado de simular la carga de datos procesados exportando el resultado final
a un archivo en formato Parquet, con justificación técnica para Big Data y Machine Learning.
"""

import os
import pandas as pd


def justificar_formato_parquet() -> str:
    """
    Retorna la justificación técnica de la elección del formato Parquet para proyectos
    de Ciencia de Datos y Machine Learning.
    """
    return (
        "\n====================================================================================\n"
        " 📊 JUSTIFICACIÓN TÉCNICA DEL FORMATO PARQUET EN MACHINE LEARNING\n"
        "====================================================================================\n"
        "1. ALMACENAMIENTO ORIENTADO A COLUMNAS:\n"
        "   Parquet almacena los datos por columnas en lugar de por filas (como CSV).\n"
        "   Los modelos de Machine Learning suelen seleccionar características específicas (features).\n"
        "   Parquet permite leer únicamente las columnas requeridas (projection pushdown),\n"
        "   minimizando drásticamente el consumo de memoria RAM y las operaciones de entrada/salida (I/O).\n\n"
        "2. CONSERVACIÓN DE ESQUEMA Y TIPOS DE DATOS (METADATOS INTEGRADOS):\n"
        "   Parquet conserva la estructura binaria exacta y tipos de datos (datetime, int, float).\n"
        "   Esto elimina la necesidad de parsear o re-inferir tipos al volver a cargar los datos en\n"
        "   Pandas, Dask o Scikit-Learn, garantizando consistencia absoluta sin pérdida de precisión.\n\n"
        "3. ALTA COMPRESIÓN Y EFICIENCIA DE ALMACENAMIENTO:\n"
        "   Utiliza compresión avanzada por columna (ej. Snappy), logrando archivos significativamente\n"
        "   más pequeños que los equivalentes en formato CSV o JSON (hasta 75% a 80% de reducción).\n\n"
        "4. EXCELENTE INTEGRACIÓN CON ECOSISTEMAS DE BIG DATA:\n"
        "   Es el estándar nativo para frameworks de computación distribuida y paralela como\n"
        "   PySpark, Dask, Polars y DuckDB, permitiendo procesar volúmenes masivos de datos eficientemente.\n"
        "====================================================================================\n"
    )


def cargar_datos_parquet(df: pd.DataFrame, output_path: str) -> None:
    """
    Simula la etapa de carga exportando el DataFrame procesado a un archivo Parquet.

    Args:
        df (pd.DataFrame): DataFrame transformado y limpio.
        output_path (str): Ruta de destino donde se guardará el archivo Parquet.
    """
    print(f"[CARGA] Exportando datos procesados a formato Parquet en: '{output_path}'...")
    
    # Creación del directorio de destino si no existe
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        
    # Guardar en formato Parquet
    df.to_parquet(output_path, index=False, engine='pyarrow')
    
    size_kb = os.path.getsize(output_path) / 1024
    print(f"[CARGA] ✓ Carga finalizada correctamente. Archivo '.parquet' generado ({size_kb:.2f} KB).")
    print(justificar_formato_parquet())
