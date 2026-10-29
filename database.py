import streamlit as st
from supabase import create_client, Client

### Inicializar cliente de Supabase usando el caché de Streamlit para no reconectar en cada rerun
@st.cache_resource
def get_supabase_client() -> Client:
    url = st.secrets["supabase"]["SUPABASE_URL"]
    key = st.secrets["supabase"]["SUPABASE_KEY"]
    return create_client(url, key)

supabase = get_supabase_client()

### =========================================================
### --- FUNCIONES DE ESTACIONES ---
### =========================================================
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

### =========================================================
### --- FUNCIONES DE INVENTARIOS ---
### =========================================================
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

### =========================================================
### --- FUNCIONES DE VENTAS ---
### =========================================================
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

### =========================================================
### --- FUNCIONES DE VISTAS SQL (ÚLTIMAS 12 SEMANAS) ---
### =========================================================
def obtener_venta_semanal_promedio_12w():
    """Obtiene la venta semanal de las últimas 12 semanas por estación y producto desde Supabase."""
    response = supabase.table("venta_semanal_promedio_12w").select("*").execute()
    return response.data

def obtener_venta_promedio_dia_semana_12w():
    """Obtiene la venta promedio por día de la semana de las últimas 12 semanas por estación y producto desde Supabase."""
    response = supabase.table("venta_promedio_dia_de_la_semana_12w").select("*").execute()
    return response.data

### =========================================================
### --- FUNCIONES DE ASIGNACIÓN DE ESTACIONES POR USUARIO ---
### =========================================================
def obtener_estaciones_por_usuario(usuario_id):
    """Obtiene las estaciones asignadas a un usuario específico, incluyendo los detalles de la estación."""
    response = supabase.table("estaciones_usuario").select("id_estacion, estaciones(*)").eq("usuario", usuario_id).execute()
    return response.data

def asignar_estacion_usuario(id_estacion, usuario_id):
    """Asigna una estación a un usuario."""
    data = {
        "id_estacion": id_estacion,
        "usuario": usuario_id
    }
    return supabase.table("estaciones_usuario").insert(data).execute()

def eliminar_asignacion_estacion(id_estacion, usuario_id):
    """Elimina la asignación de una estación a un usuario."""
    return supabase.table("estaciones_usuario").delete().eq("id_estacion", id_estacion).eq("usuario", usuario_id).execute()
