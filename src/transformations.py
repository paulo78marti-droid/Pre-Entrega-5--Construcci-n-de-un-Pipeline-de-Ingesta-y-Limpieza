"""
Módulo de Transformación (Transform) - Pipeline ETL
Contiene funciones independientes para la limpieza y preparación de datos:
- Normalización de nombres de columnas (snake_case, sin acentos).
- Eliminación de registros duplicados.
- Gestión justificada de valores nulos (imputación lógica y categórica).
- Conversión de tipos de datos (fechas).
"""

import pandas as pd
import unicodedata


def normalizar_nombres_columnas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza los nombres de las columnas del DataFrame:
    - Convierte a minúsculas.
    - Elimina espacios sobrantes.
    - Convierte a formato snake_case.
    - Remueve tildes y caracteres especiales.
    """
    df_result = df.copy()
    nuevas_columnas = []
    
    for col in df_result.columns:
        # Remueve acentos (ej. Categoría -> Categoria)
        col_norm = unicodedata.normalize('NFD', col).encode('ascii', 'ignore').decode("utf-8")
        # Pasa a minúsculas y sustituye espacios por guiones bajos
        col_clean = col_norm.strip().lower().replace(" ", "_")
        nuevas_columnas.append(col_clean)
        
    df_result.columns = nuevas_columnas
    print(f"[TRANSFORMACIÓN] Columnas normalizadas a snake_case.")
    return df_result


def eliminar_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Elimina filas duplicadas presentes en el DataFrame.
    """
    df_result = df.copy()
    cant_duplicados = df_result.duplicated().sum()
    
    if cant_duplicados > 0:
        df_result = df_result.drop_duplicates()
        print(f"[TRANSFORMACIÓN] ✓ Registros duplicados eliminados: {cant_duplicados}.")
    else:
        print("[TRANSFORMACIÓN] ✓ No se detectaron filas duplicadas.")
        
    return df_result


def gestionar_valores_nulos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Gestión e imputación justificada de valores nulos:
    1. Si falta 'total_venta', se recalcula mediante (precio_unitario * cantidad).
    2. En variables categóricas, los nulos se completan como 'No Especificado'.
    3. Asegura el casteo correcto de la columna 'fecha' a datetime.
    """
    df_result = df.copy()
    
    # 1. Imputación calculada de total_venta
    if 'total_venta' in df_result.columns and 'precio_unitario' in df_result.columns and 'cantidad' in df_result.columns:
        mask_monto_nulo = df_result['total_venta'].isnull()
        cant_monto_nulo = mask_monto_nulo.sum()
        if cant_monto_nulo > 0:
            df_result.loc[mask_monto_nulo, 'total_venta'] = (
                df_result.loc[mask_monto_nulo, 'precio_unitario'] * df_result.loc[mask_monto_nulo, 'cantidad']
            )
            print(f"  ✓ Imputados {cant_monto_nulo} valores nulos en 'total_venta' calculando (precio_unitario * cantidad).")

    # 2. Imputación de columnas categóricas
    cols_categoricas = ['categoria_producto', 'metodo_de_pago', 'metodo_de_compra', 'promocion_aplicada']
    for col in cols_categoricas:
        if col in df_result.columns and df_result[col].isnull().sum() > 0:
            cnt = df_result[col].isnull().sum()
            df_result[col] = df_result[col].fillna('No Especificado')
            print(f"  ✓ Imputados {cnt} valores nulos en '{col}' como 'No Especificado'.")

    # 3. Casteo de fechas a datetime
    if 'fecha' in df_result.columns:
        df_result['fecha'] = pd.to_datetime(df_result['fecha'], errors='coerce')
        print("  ✓ Columna 'fecha' parseada correctamente a formato datetime.")

    return df_result


def aplicar_transformaciones(df: pd.DataFrame) -> pd.DataFrame:
    """
    Función modular independiente que coordina las etapas de limpieza.
    """
    print("\n--- INICIO DE ETAPA DE TRANSFORMACIÓN ---")
    df_norm = normalizar_nombres_columnas(df)
    df_sin_duplicados = eliminar_duplicados(df_norm)
    df_clean = gestionar_valores_nulos(df_sin_duplicados)
    print("--- FIN DE ETAPA DE TRANSFORMACIÓN ---\n")
    return df_clean
