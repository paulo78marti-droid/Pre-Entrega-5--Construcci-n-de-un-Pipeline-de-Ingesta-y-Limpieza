"""
Módulo de Extracción (Extract) para el Pipeline ETL.
Encargado de la ingesta modular de datos desde fuentes en formato CSV.
"""

import os
import pandas as pd


def extraer_datos_csv(filepath: str) -> pd.DataFrame:
    """
    Etapa E: Extrae los datos desde un archivo CSV.

    Args:
        filepath (str): Ruta relativa o absoluta al archivo CSV de entrada.

    Returns:
        pd.DataFrame: DataFrame con los datos originales cargados.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No se encontró el archivo de entrada en la ruta: {filepath}")
        
    print(f"[EXTRACCIÓN] Leyendo datos desde el origen CSV: '{filepath}'...")
    df = pd.read_csv(filepath)
    print(f"[EXTRACCIÓN] ✓ Ingesta exitosa: {len(df)} filas y {len(df.columns)} columnas leídas.")
    return df
