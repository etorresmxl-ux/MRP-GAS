import streamlit as st
from supabase import create_client, Client

# Inicializar cliente de Supabase usando el caché de Streamlit para no reconectar en cada rerun
@st.cache_resource
def get_supabase_client() -> Client:
    url = st.secrets["supabase"]["SUPABASE_URL"]
    key = st.secrets["supabase"]["SUPABASE_KEY"]
    return create_client(url, key)

supabase = get_supabase_client()

# --- FUNCIONES DE ESTACIONES ---
def obtener_estaciones():
    response = supabase.table("estaciones").select("*").execute()
    return response.data

def insertar_estacion(id_estacion, nombre, plaza, tad):
    data = {
        "id_estacion": id_estacion,
        "nombre": nombre,
        "plaza": plaza,
        "tad": tad
    }
    return supabase.table("estaciones").insert(data).execute()

# --- FUNCIONES DE INVENTARIOS ---
def obtener_inventarios():
    response = supabase.table("inventarios").select("*, estaciones(nombre)").execute()
    return response.data

def insertar_inventario(id_estacion, fecha, producto, volumen):
    data = {
        "id_estacion": id_estacion,
        "fecha": str(fecha),
        "producto": producto,
        "volumen": float(volumen)
    }
    return supabase.table("inventarios").insert(data).execute()

# --- FUNCIONES DE VENTAS ---
def obtener_ventas():
    response = supabase.table("ventas").select("*, estaciones(nombre)").execute()
    return response.data

def insertar_venta(id_estacion, fecha, producto, volumen):
    data = {
        "id_estacion": id_estacion,
        "fecha": str(fecha),
        "producto": producto,
        "volumen": float(volumen)
    }
    return supabase.table("ventas").insert(data).execute()
