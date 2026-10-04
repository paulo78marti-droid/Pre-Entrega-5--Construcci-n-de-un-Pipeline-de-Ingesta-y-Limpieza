import sys
import os

# Asegurar que el directorio raíz está en el path de Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.extract import extract_data
from src.transform import transform_data
from src.load import load_data


def run_pipeline():
    """
    Funcion principal que coordina la ejecucion secuencial del Pipeline ETL:
    1. Extraccion de datos desde el archivo CSV crudo.
    2. Transformacion y limpieza de datos (columnas, nulos, duplicados).
    3. Carga y exportacion del resultado en formato Parquet.
    """
    print("==================================================")
    print("   INICIANDO PIPELINE ETL DE INGESTA Y LIMPIEZA   ")
    print("==================================================\n")

    # Rutas de entrada y salida
    raw_data_path = os.path.join("data", "raw", "ventas_retail_raw.csv")
    processed_data_path = os.path.join("data", "processed", "ventas_retail_limpio.parquet")

    try:
        # Step 1: Extraction
        df_raw = extract_data(raw_data_path)

        # Step 2: Transformation
        df_clean = transform_data(df_raw)

        # Step 3: Load
        load_data(df_clean, processed_data_path)

        print("==================================================")
        print("   PIPELINE FINALIZADO CON EXITO CON PANDAS/PARQUET   ")
        print("==================================================\n")

    except Exception as e:
        print(f" Error durante la ejecucion del pipeline: {e}")

if __name__ == "__main__":
    run_pipeline()
