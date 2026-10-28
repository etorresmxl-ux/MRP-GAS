import streamlit as st
import pandas as pd
from datetime import date
import database as db

# Configuración inicial de la página
st.set_page_config(
    page_title="Gestión de Combustibles",
    page_icon="⛽",
    layout="wide"
)

st.title("⛽ Sistema de Gestión de Combustible")

# Menú lateral
menu = st.sidebar.selectbox(
    "Navegación",
    ["Estaciones", "Inventarios", "Ventas"]
)

# ---------------------------------------------------------
# SECCIÓN 1: ESTACIONES
# ---------------------------------------------------------
if menu == "Estaciones":
    st.header("📍 Gestión de Estaciones")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Registrar Nueva Estación")
        with st.form("form_estaciones", clear_on_submit=True):
            id_estacion = st.text_input("ID Estación (único)*", placeholder="ej. EST-001")
            nombre = st.text_input("Nombre de la Estación*")
            plaza = st.text_input("Plaza")
            tad = st.text_input("TAD")
            
            submitted = st.form_submit_button("Guardar Estación")
            if submitted:
                if id_estacion and nombre:
                    try:
                        db.insertar_estacion(id_estacion, nombre, plaza, tad)
                        st.success(f"Estación '{nombre}' registrada con éxito.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al guardar: {e}")
                else:
                    st.warning("El ID y el Nombre son obligatorios.")

    with col2:
        st.subheader("Estaciones Registradas")
        estaciones_data = db.obtener_estaciones()
        if estaciones_data:
            df_estaciones = pd.DataFrame(estaciones_data)
            st.dataframe(df_estaciones, use_container_width=True)
        else:
            st.info("No hay estaciones registradas aún.")

# ---------------------------------------------------------
# SECCIÓN 2: INVENTARIOS
# ---------------------------------------------------------
elif menu == "Inventarios":
    st.header("📦 Registro de Inventarios")
    
    estaciones_data = db.obtener_estaciones()
    
    if not estaciones_data:
        st.warning("Primero debes registrar al menos una Estación en el menú 'Estaciones'.")
    else:
        # Mapeo para seleccionar la estación fácilmente
        opciones_estaciones = {e['nombre']: e['id_estacion'] for e in estaciones_data}
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Capturar Inventario")
            with st.form("form_inventario", clear_on_submit=True):
                estacion_sel = st.selectbox("Estación", list(opciones_estaciones.keys()))
                fecha_inv = st.date_input("Fecha", value=date.today())
                producto_inv = st.selectbox("Producto", ["Magna", "Premium", "Diesel"])
                volumen_inv = st.number_input("Volumen (Lts/Gals)", min_value=0.0, step=100.0, format="%.2f")
                
                submitted = st.form_submit_button("Guardar Inventario")
                if submitted:
                    try:
                        id_est = opciones_estaciones[estacion_sel]
                        db.insertar_inventario(id_est, fecha_inv, producto_inv, volumen_inv)
                        st.success("Inventario guardado correctamente.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al registrar inventario: {e}")

        with col2:
            st.subheader("Historial de Inventarios")
            inventarios_data = db.obtener_inventarios()
            if inventarios_data:
                df_inv = pd.DataFrame(inventarios_data)
                # Formatear el nombre de la estación si viene relacional
                if 'estaciones' in df_inv.columns:
                    df_inv['estacion_nombre'] = df_inv['estaciones'].apply(lambda x: x.get('nombre') if isinstance(x, dict) else '')
                    df_inv = df_inv.drop(columns=['estaciones'])
                
                st.dataframe(df_inv, use_container_width=True)
            else:
                st.info("No hay inventarios registrados.")

# ---------------------------------------------------------
# SECCIÓN 3: VENTAS
# ---------------------------------------------------------
elif menu == "Ventas":
    st.header("💰 Registro de Ventas")
    
    estaciones_data = db.obtener_estaciones()
    
    if not estaciones_data:
        st.warning("Primero debes registrar al menos una Estación en el menú 'Estaciones'.")
    else:
        opciones_estaciones = {e['nombre']: e['id_estacion'] for e in estaciones_data}
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Capturar Venta")
            with st.form("form_ventas", clear_on_submit=True):
                estacion_sel = st.selectbox("Estación", list(opciones_estaciones.keys()))
                fecha_venta = st.date_input("Fecha", value=date.today())
                producto_venta = st.selectbox("Producto", ["Magna", "Premium", "Diesel"])
                volumen_venta = st.number_input("Volumen Vendido", min_value=0.0, step=100.0, format="%.2f")
                
                submitted = st.form_submit_button("Guardar Venta")
                if submitted:
                    try:
                        id_est = opciones_estaciones[estacion_sel]
                        db.insertar_venta(id_est, fecha_venta, producto_venta, volumen_venta)
                        st.success("Venta guardada correctamente.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al registrar venta: {e}")

        with col2:
            st.subheader("Historial de Ventas")
            ventas_data = db.obtener_ventas()
            if ventas_data:
                df_ventas = pd.DataFrame(ventas_data)
                if 'estaciones' in df_ventas.columns:
                    df_ventas['estacion_nombre'] = df_ventas['estaciones'].apply(lambda x: x.get('nombre') if isinstance(x, dict) else '')
                    df_ventas = df_ventas.drop(columns=['estaciones'])
                
                st.dataframe(df_ventas, use_container_width=True)
            else:
                st.info("No hay ventas registradas.")
