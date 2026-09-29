"""
Módulo Orquestador del Pipeline ETL
Importa las funciones modulares de extracción, transformación y carga
para coordinar la ejecución del pipeline completo.
"""

import pandas as pd
from src.extract import extraer_datos_csv
from src.transformations import aplicar_transformaciones
from src.load import cargar_datos_parquet


def ejecutar_pipeline(input_path: str, output_path: str) -> pd.DataFrame:
    """
    Ejecuta el Pipeline ETL modular completo.
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
