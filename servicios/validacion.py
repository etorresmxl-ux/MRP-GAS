import pandas as pd
import database as db

def obtener_mapa_tanques():
    """Obtiene y normaliza la relación de estaciones y productos desde tanques_estaciones."""
    datos = db.obtener_tanques_estaciones()
    if not datos:
        return pd.DataFrame()
    df = pd.DataFrame(datos)
    if "producto" in df.columns:
        df["producto"] = df["producto"].str.capitalize()
    return df

def estacion_tiene_producto(id_estacion, producto, df_tanques=None):
    """Verifica si un id_estacion cuenta con un producto específico en tanques_estaciones."""
    if df_tanques is None or df_tanques.empty:
        df_tanques = obtener_mapa_tanques()
    if df_tanques.empty:
        return False
    
    prod_cap = producto.capitalize()
    match = df_tanques[
        (df_tanques["id_estacion"] == id_estacion) & 
        (df_tanques["producto"] == prod_cap)
    ]
    return not match.empty

def validar_matriz_productos(df_estaciones, df_resultado, productos=["Regular", "Premium", "Diesel"]):
    """
    Revisa tanques_estaciones: si un id_estacion no cuenta con un producto,
    coloca 'N/A' en lugar de valores numéricos para bloquear su uso/escritura.
    """
    df_tanques = obtener_mapa_tanques()
    df_valido = df_resultado.copy()
    
    for idx, row in df_valido.iterrows():
        id_est = row["id_estacion"]
        for prod in productos:
            if not estacion_tiene_producto(id_est, prod, df_tanques):
                df_valido.loc[idx, prod] = "N/A"
                
    return df_valido
