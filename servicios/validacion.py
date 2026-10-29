import pandas as pd
import database as db


def _normalizar_producto(valor):
    """Normaliza nombres de producto para comparar en toda la app."""
    if pd.isna(valor):
        return ""
    return str(valor).strip().capitalize()


def obtener_mapa_tanques():
    """Obtiene y normaliza la relación de estaciones y productos desde tanques_estaciones."""
    datos = db.obtener_tanques_estaciones()
    if not datos:
        return pd.DataFrame()

    df = pd.DataFrame(datos)

    if "id_estacion" in df.columns:
        df["id_estacion"] = df["id_estacion"].astype(str).str.strip().str.upper()

    if "producto" in df.columns:
        df["producto"] = df["producto"].map(_normalizar_producto)

    return df


def estacion_tiene_producto(id_estacion, producto, df_tanques=None):
    """Verifica si un id_estacion cuenta con un producto específico en tanques_estaciones."""
    if df_tanques is None or df_tanques.empty:
        df_tanques = obtener_mapa_tanques()
    if df_tanques.empty:
        return False

    id_est = str(id_estacion).strip().upper()
    prod_cap = _normalizar_producto(producto)

    match = df_tanques[
        (df_tanques["id_estacion"].astype(str).str.strip().str.upper() == id_est) &
        (df_tanques["producto"].astype(str).str.strip() == prod_cap)
    ]
    return not match.empty


def validar_matriz_productos(df_estaciones, df_resultado, productos=["Regular", "Premium", "Diesel"]):
    """
    Revisa tanques_estaciones: si un id_estacion no cuenta con un producto,
    coloca 'N/A' en lugar de valores numéricos para bloquear su uso/escritura.
    """
    df_tanques = obtener_mapa_tanques()
    df_valido = df_resultado.copy()

    # Asegurar que las columnas de productos admitan texto (tipo object) para evitar LossySetitemError
    for prod in productos:
        if prod in df_valido.columns:
            df_valido[prod] = df_valido[prod].astype(object)

    for idx, row in df_valido.iterrows():
        id_est = str(row["id_estacion"]).strip().upper()
        for prod in productos:
            if not estacion_tiene_producto(id_est, prod, df_tanques):
                df_valido.loc[idx, prod] = "N/A"

    return df_valido
