import streamlit as st
import math
from supabase import create_client, Client

# Inicializar cliente de Supabase usando el caché de Streamlit para no reconectar en cada rerun
@st.cache_resource
def get_supabase_client() -> Client:
    url = st.secrets["supabase"]["SUPABASE_URL"]
    key = st.secrets["supabase"]["SUPABASE_KEY"]
    return create_client(url, key)

supabase = get_supabase_client()

def _limpiar_flotante(valor):
    """Convierte valores nulos, NaN o vacíos a 0.0 para cumplir con JSON y Supabase."""
    if valor is None:
        return 0.0
    try:
        f = float(valor)
        if math.isnan(f) or math.isinf(f):
            return 0.0
        return f
    except (ValueError, TypeError):
        return 0.0

# =========================================================
# --- FUNCIONES DE ESTACIONES ---
# =========================================================
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

# =========================================================
# --- FUNCIONES DE TANQUES ESTACIONES ---
# =========================================================
def obtener_tanques_estaciones():
    """Obtiene la relación de tanques y productos configurados por estación."""
    response = supabase.table("tanques_estaciones").select("*").execute()
    return response.data

# =========================================================
# --- FUNCIONES DE ESTACIONES USUARIO ---
# =========================================================
def obtener_estaciones_usuario():
    """Obtiene la relación de estaciones y usuarios asignados desde Supabase."""
    response = supabase.table("estaciones_usuario").select("*, estaciones(nombre, plaza, tad)").execute()
    return response.data

def insertar_estacion_usuario(id_estacion, usuario):
    """Inserta la asignación de una estación a un usuario."""
    data = {
        "id_estacion": id_estacion,
        "usuario": usuario
    }
    return supabase.table("estaciones_usuario").insert(data).execute()

# =========================================================
# --- FUNCIONES DE INVENTARIOS ---
# =========================================================
def obtener_inventarios():
    response = supabase.table("inventarios").select("*, estaciones(nombre)").execute()
    return response.data

def insertar_inventario(id_estacion, fecha, producto, volumen):
    data = {
        "id_estacion": id_estacion,
        "fecha": str(fecha),
        "producto": producto,
        "volumen": _limpiar_flotante(volumen)
    }
    return supabase.table("inventarios").insert(data).execute()

# =========================================================
# --- FUNCIONES DE VENTAS ---
# =========================================================
def obtener_ventas():
    response = supabase.table("ventas").select("*, estaciones(nombre)").execute()
    return response.data

def insertar_venta(id_estacion, fecha, producto, volumen):
    data = {
        "id_estacion": id_estacion,
        "fecha": str(fecha),
        "producto": producto,
        "volumen": _limpiar_flotante(volumen)
    }
    return supabase.table("ventas").insert(data).execute()

# =========================================================
# --- FUNCIONES DE VISTAS SQL (ÚLTIMAS 12 SEMANAS) ---
# =========================================================
def obtener_venta_semanal_promedio_12w():
    """Obtiene la venta semanal de las últimas 12 semanas por estación y producto desde Supabase."""
    response = supabase.table("venta_semanal_promedio_12w").select("*").execute()
    return response.data

def obtener_venta_promedio_dia_semana_12w():
    """Obtiene la venta promedio por día de la semana de las últimas 12 semanas por estación y producto desde Supabase."""
    response = supabase.table("venta_promedio_dia_de_la_semana_12w").select("*").execute()
    return response.data
