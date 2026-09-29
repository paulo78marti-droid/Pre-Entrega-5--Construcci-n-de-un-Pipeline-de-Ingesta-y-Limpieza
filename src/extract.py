"""
Módulo de Extracción (Extract) - Pipeline ETL
Encargado de la ingesta modular de datos desde un archivo CSV
asegurando el uso correcto de memoria.
"""

import os
import pandas as pd


def extraer_datos_csv(filepath: str) -> pd.DataFrame:
    """
    Etapa E (Extract): Lee el conjunto de datos desde un archivo CSV.

    Args:
        filepath (str): Ruta al archivo CSV de entrada.

    Returns:
        pd.DataFrame: DataFrame con los datos originales cargados.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No se encontró el archivo de entrada en la ruta: {filepath}")
        
    print(f"[EXTRACCIÓN] Leyendo datos desde el origen CSV: '{filepath}'...")
    df = pd.read_csv(filepath)
    
    # Reporte de uso eficiente de memoria
    mem_kb = df.memory_usage(deep=True).sum() / 1024
    print(f"[EXTRACCIÓN] ✓ Ingesta exitosa: {len(df)} filas y {len(df.columns)} columnas leídas ({mem_kb:.2f} KB en RAM).")
    return df
