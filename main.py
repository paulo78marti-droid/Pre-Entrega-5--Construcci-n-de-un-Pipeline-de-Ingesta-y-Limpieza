"""
Script Principal para la Ejecución del Pipeline ETL (Ventas Starbucks)
Curso: Data Science II - Pre-Entrega 5
Autor: Estudiante de Ciencia de Datos / Nacho
"""

import os
from src.etl_pipeline import ejecutar_pipeline

def main():
    print("==================================================")
    print(" ☕ PIPELINE ETL - PROCESAMIENTO DE VENTAS STARBUCKS")
    print("==================================================")
    
    # Definición de rutas relativas
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_csv = os.path.join(base_dir, "data", "raw", "ventas_starbucks.csv")
    output_parquet = os.path.join(base_dir, "data", "output", "ventas_starbucks_limpio.parquet")
    
    # Ejecución del pipeline ETL modular
    df_procesado = ejecutar_pipeline(input_csv, output_parquet)
    
    print("==================================================")
    print(" ¡Pipeline finalizado con éxito!")
    print(f" Registros totales limpios y guardados: {len(df_procesado)}")
    print("==================================================")

if __name__ == "__main__":
    main()
