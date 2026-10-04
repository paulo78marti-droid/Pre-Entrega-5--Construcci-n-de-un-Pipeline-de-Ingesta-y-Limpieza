import os
import pandas as pd

def load_data(df: pd.DataFrame, output_path: str) -> None:
    """
    Exporta el DataFrame limpio y transformado a un archivo en formato Parquet.

    Parametros:
        df (pd.DataFrame): DataFrame transformado a guardar.
        output_path (str): Ruta completa donde se guardara el archivo Parquet.
    """
    print(f" Guardando datos procesados en formato Parquet...")
    
    # Crear directorio de salida si no existe
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Exportacion a formato Parquet
    df.to_parquet(output_path, index=False)

    print(f" Exportacion completada con exito en:")
    print(f"   -> {output_path}")
    print(" Justificacion de Parquet: Formato columnar optimizado que reduce el espacio en disco,")
    print("   acelera las lecturas en modelos de Machine Learning y conserva el tipo de datos nativo.\n")
