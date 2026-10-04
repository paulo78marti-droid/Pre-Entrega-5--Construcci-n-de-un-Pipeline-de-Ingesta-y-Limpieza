import os
import pandas as pd

def extract_data(file_path: str) -> pd.DataFrame:
    """
    Lee un archivo CSV desde la ruta especificada y carga los datos en un DataFrame de Pandas.
    Optimiza el uso de memoria verificando la estructura de los datos.

    Parametros:
        file_path (str): Ruta relativa o absoluta del archivo CSV a extraer.

    Retorna:
        pd.DataFrame: DataFrame de Pandas con los datos crudos extraidos.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"El archivo especificado no existe en la ruta: {file_path}")

    print(f" Extrayendo datos desde: {file_path}...")
    
    # Carga del dataset desde CSV
    df = pd.read_csv(file_path)

    # Informacion sobre el tamaño y uso de memoria inicial
    filas, columnas = df.shape
    memoria_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)

    print(f" Extraction completada exitosamente:")
    print(f"   - Dimensiones: {filas} filas x {columnas} columnas")
    print(f"   - Uso de memoria aproximado: {memoria_mb:.2f} MB\n")

    return df
