"""
Pipeline ETL - Ventas Starbucks (Script Auto-contenido con Kagglehub)
Dataset: guadalupesaraviaweht/ventas-starbucks
Curso: Data Science II - Pre-Entrega 5
"""

import os
import glob
import unicodedata
import pandas as pd
import kagglehub


def descargar_dataset_kaggle() -> str:
    print("[KAGGLE] Descargando la última versión del dataset 'guadalupesaraviaweht/ventas-starbucks'...")
    path = kagglehub.dataset_download("guadalupesaraviaweht/ventas-starbucks")
    print(f"[KAGGLE] ✓ Dataset descargado en: '{path}'")
    
    csv_files = glob.glob(os.path.join(path, "*.csv"))
    if csv_files:
        print(f"[KAGGLE] Archivo CSV encontrado: '{csv_files[0]}'")
        return csv_files[0]
    else:
        raise FileNotFoundError("No se encontró ningún archivo .csv en la ruta descargada de Kaggle.")


def extraer_datos_csv(filepath: str) -> pd.DataFrame:
    print(f"[EXTRACCIÓN] Leyendo origen: '{filepath}'...")
    df = pd.read_csv(filepath)
    print(f"[EXTRACCIÓN] ✓ Ingesta exitosa: {len(df)} filas, {len(df.columns)} columnas.")
    return df


def normalizar_nombres_columnas(df: pd.DataFrame) -> pd.DataFrame:
    df_res = df.copy()
    nuevas_cols = []
    for col in df_res.columns:
        col_norm = unicodedata.normalize('NFD', col).encode('ascii', 'ignore').decode("utf-8")
        col_clean = col_norm.strip().lower().replace(" ", "_")
        nuevas_cols.append(col_clean)
    df_res.columns = nuevas_cols
    print(f"[NORMALIZACIÓN] Nombres de columnas en snake_case: {list(df_res.columns)}")
    return df_res


def eliminar_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    df_res = df.copy()
    cant_dup = df_res.duplicated().sum()
    print(f"[DUPLICADOS] Registros duplicados detectados: {cant_dup}")
    if cant_dup > 0:
        df_res = df_res.drop_duplicates()
        print(f"[DUPLICADOS] ✓ {cant_dup} duplicados eliminados.")
    else:
        print("[DUPLICADOS] ✓ No se encontraron registros duplicados.")
    return df_res


def gestionar_valores_nulos(df: pd.DataFrame) -> pd.DataFrame:
    df_res = df.copy()
    # Imputación estructural en 'tamano'
    if 'tamano' in df_res.columns:
        nulos_tam = df_res['tamano'].isnull().sum()
        if nulos_tam > 0:
            df_res['tamano'] = df_res['tamano'].fillna('No Aplica')
            print(f"  ✓ [IMPUTACIÓN ESTRUCTURAL] Imputados {nulos_tam} nulos en 'tamano' como 'No Aplica'.")
            
    # Imputación matemática de total_venta
    if 'total_venta' in df_res.columns and 'precio_unitario' in df_res.columns and 'cantidad' in df_res.columns:
        mask_nulo = df_res['total_venta'].isnull()
        if mask_nulo.sum() > 0:
            df_res.loc[mask_nulo, 'total_venta'] = (
                df_res.loc[mask_nulo, 'precio_unitario'] * df_res.loc[mask_nulo, 'cantidad']
            )
            print(f"  ✓ [IMPUTACIÓN CALCULADA] Imputados {mask_nulo.sum()} nulos en 'total_venta' mediante (precio * cantidad).")
            
    # Imputación categórica
    for col in ['categoria_producto', 'metodo_de_pago', 'metodo_de_compra']:
        if col in df_res.columns and df_res[col].isnull().sum() > 0:
            cnt = df_res[col].isnull().sum()
            df_res[col] = df_res[col].fillna('No Especificado')
            print(f"  ✓ [IMPUTACIÓN CATEGÓRICA] Imputados {cnt} nulos en '{col}' como 'No Especificado'.")
            
    if 'fecha' in df_res.columns:
        df_res['fecha'] = pd.to_datetime(df_res['fecha'])
        
    return df_res


def aplicar_transformaciones(df: pd.DataFrame) -> pd.DataFrame:
    print("\n--- INICIO DE ETAPA DE TRANSFORMACIÓN ---")
    df_norm = normalizar_nombres_columnas(df)
    df_dedup = eliminar_duplicados(df_norm)
    df_clean = gestionar_valores_nulos(df_dedup)
    print("--- FIN DE ETAPA DE TRANSFORMACIÓN ---\n")
    return df_clean


def cargar_datos_parquet(df: pd.DataFrame, output_path: str) -> None:
    print(f"[CARGA] Exportando datos procesados a Parquet: '{output_path}'...")
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    df.to_parquet(output_path, index=False, engine='pyarrow')
    kb = os.path.getsize(output_path) / 1024
    print(f"[CARGA] ✓ Archivo Parquet generado exitosamente ({kb:.2f} KB).")


def ejecutar_pipeline(input_path: str, output_path: str) -> pd.DataFrame:
    df_raw = extraer_datos_csv(input_path)
    df_clean = aplicar_transformaciones(df_raw)
    cargar_datos_parquet(df_clean, output_path)
    return df_clean


if __name__ == "__main__":
    print("==================================================")
    print(" PIPELINE ETL - VENTAS STARBUCKS (KAGGLE DATASET)")
    print("==================================================")
    
    input_csv = descargar_dataset_kaggle()
    output_parquet = "data/output/ventas_starbucks_limpio.parquet"
    
    df_final = ejecutar_pipeline(input_csv, output_parquet)
    
    print("==================================================")
    print(" ¡Pipeline finalizado con éxito!")
    print(f" Total de registros procesados y guardados: {len(df_final)}")
    print("==================================================")
    
    print("\n📊 Muestra de datos limpios guardados en Parquet:")
    print(df_final.head(10))
