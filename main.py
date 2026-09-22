"""
Script principal para la ejecución del Pipeline de Ingesta, Limpieza y Transformación (ETL).
Data Science II - Pre-Entrega 5
"""

import os
from src.etl_pipeline import ejecutar_pipeline

def main():
    print("==================================================")
    print(" PIPELINE DE DATOS ETL - VENTAS STARBUCKS")
    print(" Data Science II - Pre-Entrega 5")
    print("==================================================")
    
    # Definición de rutas relativas
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_csv = os.path.join(base_dir, "data", "raw", "ventas_starbucks.csv")
    output_parquet = os.path.join(base_dir, "data", "output", "ventas_starbucks_limpio.parquet")
    
    # Ejecución del pipeline ETL
    df_procesado = ejecutar_pipeline(input_csv, output_parquet)
    
    print("==================================================")
    print(" ¡Pipeline finalizado con éxito!")
    print(f" Total de registros procesados y guardados: {len(df_procesado)}")
    print("==================================================")

if __name__ == "__main__":
    main()
