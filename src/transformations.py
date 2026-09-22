"""
Módulo de Transformaciones para el Pipeline ETL.
Contiene funciones dedicadas a la limpieza de datos, normalización de columnas,
gestión justificada de valores nulos y remoción de registros duplicados
basado en el dataset de Ventas Starbucks (guadalupesaraviaweht/ventas-starbucks).
"""

import pandas as pd
import unicodedata


def normalizar_nombres_columnas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza los nombres de las columnas del DataFrame:
    - Convierte a minúsculas.
    - Elimina espacios al inicio y final.
    - Reemplaza espacios por guiones bajos (snake_case).
    - Remueve tildes y caracteres especiales (ej. 'Categoría_Producto' -> 'categoria_producto').

    Justificación:
    Estandarizar los nombres de columnas previene errores de sintaxis en Pandas,
    facilita el acceso programático a atributos y asegura consistencia en el pipeline.
    """
    df_result = df.copy()
    nuevas_columnas = []
    for col in df_result.columns:
        # Normalización Unicode para eliminar acentos (ej. 'Categoría' -> 'Categoria')
        col_norm = unicodedata.normalize('NFD', col).encode('ascii', 'ignore').decode("utf-8")
        # Limpieza de espacios y formato snake_case
        col_clean = col_norm.strip().lower().replace(" ", "_")
        nuevas_columnas.append(col_clean)
        
    df_result.columns = nuevas_columnas
    print(f"[NORMALIZACIÓN] Nombres de columnas normalizados a snake_case:\n  {list(df_result.columns)}")
    return df_result


def eliminar_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identifica y remueve registros totalmente duplicados en el dataset.

    Justificación:
    Los registros duplicados distorsionan el análisis estadístico y financiero,
    provocando una sobreestimación en las métricas de ingresos y volumen de ventas.
    """
    df_result = df.copy()
    cant_duplicados = df_result.duplicated().sum()
    print(f"[DUPLICADOS] Registros duplicados detectados: {cant_duplicados}")
    
    if cant_duplicados > 0:
        df_result = df_result.drop_duplicates()
        print(f"[DUPLICADOS] ✓ {cant_duplicados} registros duplicados eliminados exitosamente.")
    else:
        print("[DUPLICADOS] ✓ No se encontraron registros duplicados.")
        
    return df_result


def gestionar_valores_nulos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Gestiona los valores nulos mediante estrategias fundamentadas en el dominio de ventas de Starbucks:

    Justificaciones:
    1. 'tamano': Imputación por etiqueta ('No Aplica'). En el dataset de Starbucks, los productos
       de Merchandising (termos/tazas), Snacks y Café en Granos no tienen tamaño de bebida (Alto, Grande, Venti).
       Por lo tanto, la ausencia de valor es estructural y se imputa como 'No Aplica'.
    2. 'total_venta': Imputación matemática. Si faltase el total, se calcula dinámicamente
       multiplicando (precio_unitario * cantidad) para recuperar el dato exacto sin eliminar la transacción.
    3. Categorías / Métodos de pago: Imputación con 'No Especificado' para mantener la integridad de la transacción.
    """
    df_result = df.copy()
    
    nulos_iniciales = df_result.isnull().sum()
    print("[NULOS] Conteo inicial de valores nulos por columna:")
    hay_nulos = False
    for col, count in nulos_iniciales.items():
        if count > 0:
            print(f"  - Columna '{col}': {count} nulos")
            hay_nulos = True
            
    if not hay_nulos:
        print("  - No se detectaron valores nulos iniciales.")

    # 1. Imputación de 'tamano' (tamaño de la bebida)
    if 'tamano' in df_result.columns:
        nulos_tamano = df_result['tamano'].isnull().sum()
        if nulos_tamano > 0:
            df_result['tamano'] = df_result['tamano'].fillna('No Aplica')
            print(f"  ✓ [IMPUTACIÓN ESTRUCTURAL] Imputados {nulos_tamano} valores nulos en 'tamano' como 'No Aplica' (productos sin tamaño de bebida).")

    # 2. Imputación calculada de total_venta si faltase
    if 'total_venta' in df_result.columns and 'precio_unitario' in df_result.columns and 'cantidad' in df_result.columns:
        mask_monto_nulo = df_result['total_venta'].isnull()
        cant_monto_nulo = mask_monto_nulo.sum()
        if cant_monto_nulo > 0:
            df_result.loc[mask_monto_nulo, 'total_venta'] = (
                df_result.loc[mask_monto_nulo, 'precio_unitario'] * df_result.loc[mask_monto_nulo, 'cantidad']
            )
            print(f"  ✓ [IMPUTACIÓN CALCULADA] Imputados {cant_monto_nulo} valores en 'total_venta' mediante (precio_unitario * cantidad).")

    # 3. Imputación de otras columnas categóricas
    cols_categoricas = ['categoria_producto', 'metodo_de_pago', 'metodo_de_compra', 'promocion_aplicada']
    for col in cols_categoricas:
        if col in df_result.columns and df_result[col].isnull().sum() > 0:
            cnt = df_result[col].isnull().sum()
            df_result[col] = df_result[col].fillna('No Especificado')
            print(f"  ✓ [IMPUTACIÓN CATEGÓRICA] Imputados {cnt} valores en '{col}' como 'No Especificado'.")

    # 4. Casteo de tipo de datos de fecha
    if 'fecha' in df_result.columns:
        df_result['fecha'] = pd.to_datetime(df_result['fecha'])

    return df_result


def aplicar_transformaciones(df: pd.DataFrame) -> pd.DataFrame:
    """
    Función independiente que coordina la secuencia de limpieza y transformación del dataset.
    
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
