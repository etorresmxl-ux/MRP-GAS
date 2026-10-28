import pandas as pd
import database as db

def limpiar_y_normalizar_estaciones(df):
    """Limpia y normaliza el DataFrame de estaciones antes de guardarlo."""
    # Asegurar nombres de columnas en minúsculas y sin espacios
    df.columns = df.columns.str.strip().str.lower()
    
    columnas_requeridas = ['id_estacion', 'nombre', 'plaza', 'tad']
    for col in columnas_requeridas:
        if col not in df.columns:
            raise ValueError(f"Falta la columna obligatoria en el Excel: {col}")
            
    # Limpieza de datos (texto plano, sin espacios extra, mayúsculas en ID)
    df['id_estacion'] = df['id_estacion'].astype(str).str.strip().str.upper()
    df['nombre'] = df['nombre'].astype(str).str.strip()
    df['plaza'] = df['plaza'].astype(str).str.strip().fillna('')
    df['tad'] = df['tad'].astype(str).str.strip().fillna('')
    
    # Eliminar duplicados locales por id_estacion quedándose con el último
    df = df.drop_duplicates(subset=['id_estacion'], keep='last')
    
    return df

def procesar_importacion_estaciones(archivo_subido):
    """Procesa el archivo subido, lo limpia y realiza la inserción masiva."""
    try:
        df_raw = pd.read_excel(archivo_subido)
        df_limpio = limpiar_y_normalizar_estaciones(df_raw)
        
        exitos = 0
        errores = 0
        
        for _, row in df_limpio.iterrows():
            try:
                db.insertar_estacion(
                    id_estacion=row['id_estacion'],
                    nombre=row['nombre'],
                    plaza=row['plaza'],
                    tad=row['tad']
                )
                exitos += 1
            except Exception:
                errores += 1
                
        return True, exitos, errores, df_limpio
    except Exception as e:
        return False, str(e), 0, None
