"""
Pipeline ETL Simplificado (Google Colab / Local).
Curso: Data Science II - Pre-Entrega 5
"""

import os
import pandas as pd


def extraer_datos(filepath: str) -> pd.DataFrame:
    """Lee el archivo CSV de entrada."""
    print(f"1. Cargando datos desde '{filepath}'...")
    return pd.read_csv(filepath)


def transformar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia los datos: columnas, duplicados y nulos."""
    print("2. Limpiando datos...")
    df_clean = df.copy()

    # Normalizar nombres de columnas
    df_clean.columns = df_clean.columns.str.strip().str.lower().str.replace(' ', '_')

    # Eliminar duplicados
    df_clean = df_clean.drop_duplicates()

    # Gestionar valores nulos
    if 'tamano' in df_clean.columns:
        df_clean['tamano'] = df_clean['tamano'].fillna('No Aplica')
    elif 'tamaño' in df_clean.columns:
        df_clean['tamaño'] = df_clean['tamaño'].fillna('No Aplica')

    if 'total_venta' in df_clean.columns and 'precio_unitario' in df_clean.columns and 'cantidad' in df_clean.columns:
        df_clean['total_venta'] = df_clean['total_venta'].fillna(df_clean['precio_unitario'] * df_clean['cantidad'])

    for col in ['categoria_producto', 'metodo_de_pago']:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].fillna('No Especificado')

    return df_clean


def cargar_datos_parquet(df: pd.DataFrame, output_path: str) -> None:
    """Guarda el DataFrame en formato Parquet."""
    print(f"3. Guardando resultado en '{output_path}'...")
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    df.to_parquet(output_path, index=False)
    print("¡Archivo Parquet guardado con éxito!")


def ejecutar_pipeline(input_path: str, output_path: str) -> pd.DataFrame:
    df_raw = extraer_datos(input_path)
    df_clean = transformar_datos(df_raw)
    cargar_datos_parquet(df_clean, output_path)
    return df_clean


if __name__ == "__main__":
    input_csv = "data/raw/ventas_starbucks.csv"
    output_parquet = "data/output/ventas_starbucks_limpio.parquet"
    if os.path.exists(input_csv):
        ejecutar_pipeline(input_csv, output_parquet)


