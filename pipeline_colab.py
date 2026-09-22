"""
Pipeline ETL - Ventas Starbucks (Script Auto-contenido para Google Colab / Python Standalone)
Curso: Data Science II - Pre-Entrega 5

Instrucciones para ejecucción en Google Colab:
1. Subir este archivo o copiar el contenido en una celda de código de Google Colab.
2. Ejecutar la celda para correr la ingesta, limpieza y generación del archivo Parquet.
"""

import os
import unicodedata
import pandas as pd


# -------------------------------------------------------------------------
# 1. CREACIÓN DEL DATASET LOCAL DE PRUEBA EN COLAB
# -------------------------------------------------------------------------
def preparar_entorno_y_datos():
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/output", exist_ok=True)
    
    csv_content = """transaction_id,fecha,tienda_id,producto,categoria,precio_unitario,cantidad,monto_total,metodo_pago
TXN-1001,2024-03-01 08:15:00,STB-01,Caffè Latte,Bebida Caliente,4.50,1,4.50,App Starbucks
TXN-1002,2024-03-01 08:22:00,STB-01,Caramel Macchiato,Bebida Caliente,5.20,2,10.40,Tarjeta
TXN-1003,2024-03-01 08:45:00,STB-02,Iced Americano,Bebida Fría,3.80,1,3.80,Efectivo
TXN-1004,2024-03-01 09:10:00,STB-01,Croissant de Almendras,Comida,3.50,1,3.50,Tarjeta
TXN-1005,2024-03-01 09:30:00,STB-03,Java Chip Frappuccino,Bebida Fría,5.80,2,,App Starbucks
TXN-1006,2024-03-01 09:55:00,STB-02,Espresso Double,Bebida Caliente,3.20,1,3.20,Tarjeta
TXN-1002,2024-03-01 08:22:00,STB-01,Caramel Macchiato,Bebida Caliente,5.20,2,10.40,Tarjeta
TXN-1007,2024-03-01 10:15:00,STB-01,Muffin de Arándanos,Comida,3.00,1,3.00,
TXN-1008,2024-03-01 10:40:00,STB-03,Cold Brew,Bebida Fría,4.20,1,4.20,Efectivo
TXN-1009,2024-03-01 11:05:00,STB-02,Green Tea Latte,,4.80,1,4.80,App Starbucks
TXN-1010,2024-03-01 11:30:00,STB-01,Caffè Mocha,Bebida Caliente,5.00,3,15.00,Tarjeta
TXN-1005,2024-03-01 09:30:00,STB-03,Java Chip Frappuccino,Bebida Fría,5.80,2,,App Starbucks
TXN-1011,2024-03-01 12:00:00,STB-02,Panini de Pavo,Comida,6.50,1,6.50,Efectivo
TXN-1012,2024-03-01 12:25:00,STB-03,Chai Tea Latte,Bebida Caliente,4.60,1,,Tarjeta
"""
    input_path = "data/raw/ventas_starbucks.csv"
    with open(input_path, "w", encoding="utf-8") as f:
        f.write(csv_content)
    print(f"✓ Dataset de prueba preparado en '{input_path}'.")
    return input_path


# -------------------------------------------------------------------------
# 2. FUNCIONES MODULARES ETL
# -------------------------------------------------------------------------
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
    return df_res


def gestionar_valores_nulos(df: pd.DataFrame) -> pd.DataFrame:
    df_res = df.copy()
    # Imputación matemática de monto_total
    if 'monto_total' in df_res.columns and 'precio_unitario' in df_res.columns and 'cantidad' in df_res.columns:
        mask_nulo = df_res['monto_total'].isnull()
        if mask_nulo.sum() > 0:
            df_res.loc[mask_nulo, 'monto_total'] = (
                df_res.loc[mask_nulo, 'precio_unitario'] * df_res.loc[mask_nulo, 'cantidad']
            )
            print(f"  ✓ [IMPUTACIÓN] Imputados {mask_nulo.sum()} valores en 'monto_total' mediante (precio * cantidad).")
            
    # Imputación categórica
    if 'categoria' in df_res.columns:
        df_res['categoria'] = df_res['categoria'].fillna('Sin Categoría')
    if 'metodo_pago' in df_res.columns:
        df_res['metodo_pago'] = df_res['metodo_pago'].fillna('No Especificado')
        
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
    df.to_parquet(output_path, index=False, engine='pyarrow')
    kb = os.path.getsize(output_path) / 1024
    print(f"[CARGA] ✓ Archivo Parquet generado exitosamente ({kb:.2f} KB).")


def ejecutar_pipeline(input_path: str, output_path: str) -> pd.DataFrame:
    df_raw = extraer_datos_csv(input_path)
    df_clean = aplicar_transformaciones(df_raw)
    cargar_datos_parquet(df_clean, output_path)
    return df_clean


# -------------------------------------------------------------------------
# 3. EJECUCIÓN PRINCIPAL
# -------------------------------------------------------------------------
if __name__ == "__main__":
    print("==================================================")
    print(" PIPELINE ETL - VENTAS STARBUCKS (GOOGLE COLAB)")
    print("==================================================")
    
    input_csv = preparar_entorno_y_datos()
    output_parquet = "data/output/ventas_starbucks_limpio.parquet"
    
    df_final = ejecutar_pipeline(input_csv, output_parquet)
    
    print("==================================================")
    print(" ¡Pipeline finalizado con éxito!")
    print(f" Total de registros procesados y guardados: {len(df_final)}")
    print("==================================================")
    
    print("\n📊 Muestra de datos limpios guardados en Parquet:")
    print(df_final.head(10))
