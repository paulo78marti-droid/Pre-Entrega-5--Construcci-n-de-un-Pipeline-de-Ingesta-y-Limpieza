"""
Módulo de lógica ETL (Extracción, Transformación y Carga)
para el procesamiento de datos de ventas de Starbucks.
Nivel: Data Science II - Pre-Entrega 5 (Principiante)
"""

import os
import pandas as pd


def extraer_datos(filepath: str) -> pd.DataFrame:
    """
    Etapa E: Extrae los datos desde un archivo CSV.
    
    Args:
        filepath (str): Ruta al archivo CSV de entrada.
        
    Returns:
        pd.DataFrame: DataFrame con los datos originales.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"El archivo de entrada no existe en la ruta: {filepath}")
        
    print(f"[EXTRACCIÓN] Leyendo datos desde '{filepath}'...")
    df = pd.read_csv(filepath)
    print(f"[EXTRACCIÓN] Registros leídos correctamente: {len(df)} filas, {len(df.columns)} columnas.")
    return df


def transformar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Etapa T: Limpieza y transformación de datos.
    - Manejo de valores duplicados.
    - Manejo de valores nulos e imputación de columnas.
    - Formateo de fechas y tipos de datos.
    
    Args:
        df (pd.DataFrame): DataFrame original.
        
    Returns:
        pd.DataFrame: DataFrame transformado y limpio.
    """
    print("[TRANSFORMACIÓN] Iniciando etapa de limpieza y transformación...")
    df_clean = df.copy()
    
    # 1. Manejo de duplicados
    duplicados = df_clean.duplicated().sum()
    print(f"  - Registros duplicados detectados: {duplicados}")
    df_clean = df_clean.drop_duplicates()
    print(f"  - Registros tras eliminar duplicados: {len(df_clean)}")
    
    # 2. Manejo de valores nulos
    print("  - Reporte de valores nulos por columna:")
    for col, count in df_clean.isnull().sum().items():
        if count > 0:
            print(f"    * {col}: {count} nulos")
            
    # Imputación de 'monto_total' si falta (precio_unitario * cantidad)
    if 'monto_total' in df_clean.columns:
        df_clean['monto_total'] = df_clean['monto_total'].fillna(
            df_clean['precio_unitario'] * df_clean['cantidad']
        )
        
    # Imputación de columnas categóricas nulas
    if 'categoria' in df_clean.columns:
        df_clean['categoria'] = df_clean['categoria'].fillna('Sin Categoría')
        
    if 'metodo_pago' in df_clean.columns:
        df_clean['metodo_pago'] = df_clean['metodo_pago'].fillna('No Especificado')
        
    # 3. Conversión de tipos de datos
    if 'fecha' in df_clean.columns:
        df_clean['fecha'] = pd.to_datetime(df_clean['fecha'])
        
    print(f"[TRANSFORMACIÓN] Proceso finalizado. Registros limpios: {len(df_clean)}.")
    return df_clean


def cargar_datos(df: pd.DataFrame, output_path: str) -> None:
    """
    Etapa L: Carga los datos transformados a un archivo en formato Parquet.
    
    Args:
        df (pd.DataFrame): DataFrame limpio.
        output_path (str): Ruta donde se guardará el archivo Parquet.
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
    df_clean = transformar_datos(df_raw)
    cargar_datos(df_clean, output_path)
    return df_clean
