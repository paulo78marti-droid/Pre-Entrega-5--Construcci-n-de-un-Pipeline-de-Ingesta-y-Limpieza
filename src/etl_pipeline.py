"""
Módulo Orquestador del Pipeline ETL (Extracción, Transformación y Carga).
Importa la lógica modular de ingesta (src.extract), limpieza (src.transformations)
y carga en formato Parquet (src.load).
"""

import pandas as pd
from src.extract import extraer_datos_csv
from src.transformations import aplicar_transformaciones
from src.load import cargar_datos_parquet


def ejecutar_pipeline(input_path: str, output_path: str) -> pd.DataFrame:
    """
    Ejecuta la secuencia completa e integrada del Pipeline ETL:
    1. Ingesta desde CSV.
    2. Limpieza de duplicados, normalización e imputación justificada de nulos.
    3. Carga en archivo Parquet con justificación técnica para Machine Learning.
    
    Args:
        input_path (str): Ruta al archivo de datos de origen (CSV).
        output_path (str): Ruta donde se exportará el resultado (Parquet).
        
    Returns:
        pd.DataFrame: DataFrame transformado resultante.
    """
    print("\n" + "=" * 60)
    print(" INICIANDO EJECUCIÓN DEL PIPELINE ETL (VENTAS STARBUCKS)")
    print("=" * 60)
    
    # 1. Extracción
    df_raw = extraer_datos_csv(input_path)
    
    # 2. Transformación
    df_clean = aplicar_transformaciones(df_raw)
    
    # 3. Carga
    cargar_datos_parquet(df_clean, output_path)
    
    return df_clean
