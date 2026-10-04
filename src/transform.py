import pandas as pd
import re

def normalizar_nombres_columnas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza los encabezados de las columnas del DataFrame:
    - Convierte a minusculas.
    - Elimina espacios al inicio y al final.
    - Reemplaza espacios y caracteres especiales por guiones bajos (_).
    """
    columnas_nuevas = []
    for col in df.columns:
        nombre_limpio = col.strip().lower()
        nombre_limpio = re.sub(r'[^\w\s]', '', nombre_limpio)
        nombre_limpio = re.sub(r'\s+', '_', nombre_limpio)
        columnas_nuevas.append(nombre_limpio)
    
    df.columns = columnas_nuevas
    return df

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica el flujo de transformacion y limpieza de datos:
    1. Normalizacion de nombres de columnas.
    2. Tratamiento de registros duplicados.
    3. Tratamiento justificado de valores nulos (imputacion y filtrado).

    Parametros:
        df (pd.DataFrame): DataFrame con datos crudos.

    Retorna:
        pd.DataFrame: DataFrame transformado y limpio.
    """
    print(" Iniciando etapa de transformacion de datos...")
    df_transform = df.copy()

    # 1. Normalizacion de Columnas
    print("  -> Normalizando nombres de columnas...")
    df_transform = normalizar_nombres_columnas(df_transform)

    # 2. Manejo de Duplicados
    duplicados_iniciales = df_transform.duplicated().sum()
    if duplicados_iniciales > 0:
        print(f"  -> Se encontraron {duplicados_iniciales} filas duplicadas. Eliminando duplicados...")
        df_transform = df_transform.drop_duplicates().reset_index(drop=True)
    else:
        print("  -> No se encontraron registros duplicados.")

    # 3. Tratamiento Justificado de Valores Nulos
    print("  -> Gestionando valores nulos...")

    # Identificar nulos antes de la limpieza
    nulos_por_columna = df_transform.isnull().sum()
    print("     Nulos por columna detectados:")
    for col, nulos in nulos_por_columna.items():
        if nulos > 0:
            print(f"       * {col}: {nulos} nulos")

    # Estrategia de Imputacion / Limpieza:
    # A) Columnas de Identificador Clave (ej. id_transaccion / id_cliente):
    #    Si falta el identificador principal, se descartan las filas ya que no se pueden atribuir.
    cols_id = [col for col in df_transform.columns if 'id' in col]
    for col_id in cols_id:
        if df_transform[col_id].isnull().sum() > 0:
            df_transform = df_transform.dropna(subset=[col_id])

    # B) Columnas Numericas (ej. precio_unitario, cantidad, monto_total):
    #    Se imputan valores faltantes con la mediana de la columna para evitar sesgos por outliers.
    cols_numericas = df_transform.select_dtypes(include=['number']).columns
    for col in cols_numericas:
        if df_transform[col].isnull().sum() > 0:
            mediana = df_transform[col].median()
            df_transform[col] = df_transform[col].fillna(mediana)
            print(f"     [Imputacion] Se completo la columna numerica '{col}' con la mediana ({mediana}).")

    # C) Columnas Categoricas (ej. categoria, metodo_pago, ciudad):
    #    Se reemplazan los nulos por la etiqueta 'Desconocido' para preservar las demas variables de la fila.
    cols_categoricas = df_transform.select_dtypes(include=['object', 'category']).columns
    for col in cols_categoricas:
        if df_transform[col].isnull().sum() > 0:
            df_transform[col] = df_transform[col].fillna('Desconocido')
            print(f"     [Imputacion] Se reemplazaron nulos en '{col}' por la etiqueta 'Desconocido'.")

    print(" Transformacion completada exitosamente.\n")
    return df_transform
