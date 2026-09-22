"""
Módulo principal del Pipeline ETL (Extracción, Transformación y Carga).
Coordina la lectura de archivos, invoca el módulo de transformaciones
y exporta los datos en formato Parquet.
"""

import os
import pandas as pd
from src.transformations import aplicar_transformaciones


def extraer_datos(filepath: str) -> pd.DataFrame:
    """
    Etapa E: Extrae los datos desde un archivo CSV.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"El archivo de entrada no existe en la ruta: {filepath}")
        
    print(f"[EXTRACCIÓN] Leyendo datos desde '{filepath}'...")
    df = pd.read_csv(filepath)
    print(f"[EXTRACCIÓN] Registros leídos correctamente: {len(df)} filas, {len(df.columns)} columnas.")
    return df


def cargar_datos(df: pd.DataFrame, output_path: str) -> None:
    """
    Etapa L: Carga los datos transformados a un archivo en formato Parquet.
    """
    print(f"[CARGA] Exportando datos procesados a formato Parquet: '{output_path}'...")
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        
    df.to_parquet(output_path, index=False)
    print(f"[CARGA] Archivo Parquet generado exitosamente en '{output_path}'.")


def ejecutar_pipeline(input_path: str, output_path: str) -> pd.DataFrame:
    """
    Ejecuta la secuencia completa del pipeline ETL.
    """
    df_raw = extraer_datos(input_path)
    df_clean = aplicar_transformaciones(df_raw)
    cargar_datos(df_clean, output_path)
    return df_clean
