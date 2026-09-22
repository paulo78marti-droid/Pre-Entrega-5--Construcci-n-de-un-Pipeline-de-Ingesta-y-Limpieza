"""
Módulo de Transformaciones para el Pipeline ETL.
Contiene funciones dedicadas a la limpieza de datos, normalización de columnas,
gestión justificada de valores nulos y remoción de registros duplicados.
"""

import pandas as pd
import unicodedata


def normalizar_nombres_columnas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza los nombres de las columnas del DataFrame:
    - Convierte a minúsculas.
    - Elimina espacios al inicio y final.
    - Reemplaza espacios por guiones bajos (snake_case).
    - Remueve tildes y caracteres especiales.

    Justificación:
    Estandarizar los nombres de columnas previene errores de sintaxis, facilita 
    el acceso programático a atributos y asegura consistencia en el pipeline.
    """
    df_result = df.copy()
    nuevas_columnas = []
    for col in df_result.columns:
        # Normalización Unicode para eliminar acentos (ej. 'categoría' -> 'categoria')
        col_norm = unicodedata.normalize('NFD', col).encode('ascii', 'ignore').decode("utf-8")
        # Limpieza de espacios y formato snake_case
        col_clean = col_norm.strip().lower().replace(" ", "_")
        nuevas_columnas.append(col_clean)
        
    df_result.columns = nuevas_columnas
    print(f"[NORMALIZACIÓN] Nombres de columnas normalizados a snake_case: {list(df_result.columns)}")
    return df_result


def eliminar_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identifica y remueve registros totalmente duplicados en el dataset.

    Justificación:
    Los registros duplicados distorsionan el análisis estadístico y financiero,
    provocando una sobreestimación en las métricas de ingresos y unidades vendidas.
    """
    df_result = df.copy()
    cant_duplicados = df_result.duplicated().sum()
    print(f"[DUPLICADOS] Registros duplicados detectados: {cant_duplicados}")
    
    if cant_duplicados > 0:
        df_result = df_result.drop_duplicates()
        print(f"[DUPLICADOS] {cant_duplicados} registros duplicados eliminados exitosamente.")
    else:
        print("[DUPLICADOS] No se encontraron registros duplicados.")
        
    return df_result


def gestionar_valores_nulos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Gestiona los valores nulos mediante estrategias fundamentadas:

    Justificaciones:
    1. 'monto_total': Imputación matemática. Al contar con 'precio_unitario' y 'cantidad',
       el monto se calcula directamente (precio_unitario * cantidad) para recuperar el dato exacto sin perder filas.
    2. 'categoria': Imputación por etiqueta por defecto ('Sin Categoría'). Evita descartar
       transacciones válidas de ventas cuando el producto no fue etiquetado correctamente.
    3. 'metodo_pago': Imputación por etiqueta por defecto ('No Especificado'). Permite preservar
       el registro de venta para auditorías cuantitativas aunque el medio de pago sea desconocido.
    """
    df_result = df.copy()
    
    nulos_iniciales = df_result.isnull().sum()
    print("[NULOS] Conteo inicial de valores nulos por columna:")
    for col, count in nulos_iniciales.items():
        if count > 0:
            print(f"  - Columna '{col}': {count} nulos")

    # 1. Imputación calculada de monto_total si faltase
    if 'monto_total' in df_result.columns and 'precio_unitario' in df_result.columns and 'cantidad' in df_result.columns:
        mask_monto_nulo = df_result['monto_total'].isnull()
        cant_monto_nulo = mask_monto_nulo.sum()
        if cant_monto_nulo > 0:
            df_result.loc[mask_monto_nulo, 'monto_total'] = (
                df_result.loc[mask_monto_nulo, 'precio_unitario'] * df_result.loc[mask_monto_nulo, 'cantidad']
            )
            print(f"  ✓ [IMPUTACIÓN CALCULADA] Imputados {cant_monto_nulo} valores en 'monto_total' mediante (precio_unitario * cantidad).")

    # 2. Imputación de columnas categóricas
    if 'categoria' in df_result.columns:
        nulos_cat = df_result['categoria'].isnull().sum()
        if nulos_cat > 0:
            df_result['categoria'] = df_result['categoria'].fillna('Sin Categoría')
            print(f"  ✓ [IMPUTACIÓN CATEGÓRICA] Imputados {nulos_cat} valores en 'categoria' como 'Sin Categoría'.")

    if 'metodo_pago' in df_result.columns:
        nulos_pago = df_result['metodo_pago'].isnull().sum()
        if nulos_pago > 0:
            df_result['metodo_pago'] = df_result['metodo_pago'].fillna('No Especificado')
            print(f"  ✓ [IMPUTACIÓN CATEGÓRICA] Imputados {nulos_pago} valores en 'metodo_pago' como 'No Especificado'.")

    # 3. Casteo de fechas
    if 'fecha' in df_result.columns:
        df_result['fecha'] = pd.to_datetime(df_result['fecha'])

    return df_result


def aplicar_transformaciones(df: pd.DataFrame) -> pd.DataFrame:
    """
    Función independiente que coordina de manera secuencial la lógica de limpieza y transformación.
    
    Args:
        df (pd.DataFrame): DataFrame original extraído.
        
    Returns:
        pd.DataFrame: DataFrame transformado, limpio y normalizado.
    """
    print("\n--- INICIO DE ETAPA DE TRANSFORMACIÓN ---")
    df_norm = normalizar_nombres_columnas(df)
    df_sin_duplicados = eliminar_duplicados(df_norm)
    df_clean = gestionar_valores_nulos(df_sin_duplicados)
    print("--- FIN DE ETAPA DE TRANSFORMACIÓN ---\n")
    return df_clean
