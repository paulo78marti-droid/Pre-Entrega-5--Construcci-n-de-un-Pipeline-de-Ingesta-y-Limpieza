"""
Módulo de Carga (Load) - Pipeline ETL
Exporta el resultado procesado a un archivo en formato Parquet
e incluye la justificación técnica de su uso en proyectos de Machine Learning.
"""

import os
import pandas as pd


def justificar_formato_parquet() -> str:
    """
    Justificación técnica de por qué Parquet es el formato preferido para Machine Learning.
    """
    return (
        "\n====================================================================================\n"
        " 📊 JUSTIFICACIÓN TÉCNICA DEL FORMATO PARQUET EN MACHINE LEARNING\n"
        "====================================================================================\n"
        "1. ALMACENAMIENTO ORIENTADO A COLUMNAS:\n"
        "   Parquet almacena los datos por columnas en lugar de por filas (como en CSV).\n"
        "   Los algoritmos de Machine Learning suelen seleccionar columnas específicas (features).\n"
        "   Parquet permite leer únicamente las columnas requeridas (projection pushdown),\n"
        "   minimizando el uso de memoria RAM y acelerando la lectura (I/O).\n\n"
        "2. PRESERVACIÓN DE ESQUEMA Y TIPOS DE DATOS:\n"
        "   Parquet conserva los tipos de datos nativos (datetime, int, float, string).\n"
        "   Evita la necesidad de re-inferir tipos o parsear texto cada vez que se carga el dataset.\n\n"
        "3. ALTA COMPRESIÓN Y EFICIENCIA DE ESPACIO:\n"
        "   Usa compresión columnar (ej. Snappy), logrando archivos significativamente más pequeños\n"
        "   que los CSV planos (reducción entre 70% y 80% del peso en disco).\n\n"
        "4. ESTÁNDAR INDUSTRIAL Y EFICIENCIA CON GRANDES VOLÚMENES:\n"
        "   Es compatible de forma nativa con Pandas, PyArrow, Dask, Polars, PySpark y DuckDB.\n"
        "====================================================================================\n"
    )


def cargar_datos_parquet(df: pd.DataFrame, output_path: str) -> None:
    """
    Exporta el DataFrame transformado a un archivo Parquet.

    Args:
        df (pd.DataFrame): DataFrame limpio y transformado.
        output_path (str): Ruta del archivo Parquet de salida.
    """
    print(f"[CARGA] Exportando datos procesados a Parquet en: '{output_path}'...")
    
    # Crear directorio de salida si no existe
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        
    # Guardar en formato Parquet
    df.to_parquet(output_path, index=False, engine='pyarrow')
    
    size_kb = os.path.getsize(output_path) / 1024
    print(f"[CARGA] ✓ Carga exitosa. Archivo Parquet generado ({size_kb:.2f} KB).")
    print(justificar_formato_parquet())
