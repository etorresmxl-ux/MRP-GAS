import pandas as pd
import database as db

# =========================================================
# 1. ESTACIONES
# =========================================================
def limpiar_y_normalizar_estaciones(df):
    """Limpia y normaliza el DataFrame de estaciones."""
    df.columns = df.columns.str.strip().str.lower()
    
    columnas_requeridas = ['id_estacion', 'nombre', 'plaza', 'tad']
    for col in columnas_requeridas:
        if col not in df.columns:
            raise ValueError(f"Falta la columna obligatoria en el Excel: {col}")
            
    df['id_estacion'] = df['id_estacion'].astype(str).str.strip().str.upper()
    df['nombre'] = df['nombre'].astype(str).str.strip()
    df['plaza'] = df['plaza'].astype(str).str.strip().fillna('')
    df['tad'] = df['tad'].astype(str).str.strip().fillna('')
    
    df = df.drop_duplicates(subset=['id_estacion'], keep='last')
    return df

def procesar_importacion_estaciones(archivo_subido):
    try:
        df_raw = pd.read_excel(archivo_subido)
        df_limpio = limpiar_y_normalizar_estaciones(df_raw)
        
        exitos = 0
        errores = 0
        ultimo_error = ""
        
        for _, row in df_limpio.iterrows():
            try:
                db.insertar_estacion(
                    id_estacion=row['id_estacion'],
                    nombre=row['nombre'],
                    plaza=row['plaza'],
                    tad=row['tad']
                )
                exitos += 1
            except Exception as e:
                errores += 1
                ultimo_error = str(e)
                
        if errores > 0 and exitos == 0:
            return False, f"Fallaron todos los registros. Último error: {ultimo_error}", errores, df_limpio
            
        return True, exitos, errores, df_limpio
    except Exception as e:
        return False, str(e), 0, None


# =========================================================
# 2. INVENTARIOS
# =========================================================
def limpiar_y_normalizar_inventarios(df):
    """Limpia y normaliza el DataFrame de inventarios."""
    df.columns = df.columns.str.strip().str.lower()
    
    columnas_requeridas = ['id_estacion', 'fecha', 'producto', 'volumen']
    for col in columnas_requeridas:
        if col not in df.columns:
            raise ValueError(f"Falta la columna obligatoria en el Excel: {col}")
            
    df['id_estacion'] = df['id_estacion'].astype(str).str.strip().str.upper()
    df['fecha'] = pd.to_datetime(df['fecha']).dt.strftime('%Y-%m-%d')
    df['producto'] = df['producto'].astype(str).str.strip().str.capitalize()
    df['volumen'] = pd.to_numeric(df['volumen'], errors='coerce').fillna(0.0)
    
    return df

def procesar_importacion_inventarios(archivo_subido):
    try:
        df_raw = pd.read_excel(archivo_subido)
        df_limpio = limpiar_y_normalizar_inventarios(df_raw)
        
        exitos = 0
        errores = 0
        ultimo_error = ""
        
        for _, row in df_limpio.iterrows():
            try:
                db.insertar_inventario(
                    id_estacion=row['id_estacion'],
                    fecha=row['fecha'],
                    producto=row['producto'],
                    volumen=float(row['volumen'])
                )
                exitos += 1
            except Exception as e:
                errores += 1
                ultimo_error = str(e)
                
        if errores > 0 and exitos == 0:
            return False, f"Fallaron todos los registros. Último error: {ultimo_error}", errores, df_limpio
            
        return True, exitos, errores, df_limpio
    except Exception as e:
        return False, str(e), 0, None


# =========================================================
# 3. VENTAS
# =========================================================
def limpiar_y_normalizar_ventas(df):
    """Limpia y normaliza el DataFrame de ventas."""
    df.columns = df.columns.str.strip().str.lower()
    
    columnas_requeridas = ['id_estacion', 'fecha', 'producto', 'volumen']
    for col in columnas_requeridas:
        if col not in df.columns:
            raise ValueError(f"Falta la columna obligatoria en el Excel: {col}")
            
    df['id_estacion'] = df['id_estacion'].astype(str).str.strip().str.upper()
    df['fecha'] = pd.to_datetime(df['fecha']).dt.strftime('%Y-%m-%d')
    df['producto'] = df['producto'].astype(str).str.strip().str.capitalize()
    df['volumen'] = pd.to_numeric(df['volumen'], errors='coerce').fillna(0.0)
    
    return df

def procesar_importacion_ventas(archivo_subido):
    try:
        df_raw = pd.read_excel(archivo_subido)
        df_limpio = limpiar_y_normalizar_ventas(df_raw)
        
        exitos = 0
        errores = 0
        ultimo_error = ""
        
        for _, row in df_limpio.iterrows():
            try:
                db.insertar_venta(
                    id_estacion=row['id_estacion'],
                    fecha=row['fecha'],
                    producto=row['producto'],
                    volumen=float(row['volumen'])
                )
                exitos += 1
            except Exception as e:
                errores += 1
                ultimo_error = str(e)
                
        if errores > 0 and exitos == 0:
            return False, f"Fallaron todos los registros. Último error: {ultimo_error}", errores, df_limpio
            
        return True, exitos, errores, df_limpio
    except Exception as e:
        return False, str(e), 0, None
