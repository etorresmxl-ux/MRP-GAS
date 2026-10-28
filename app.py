import streamlit as st
import pandas as pd
from datetime import date
import database as db
from modulos import importador
from modulos import estaciones

# Configuración inicial de la página
st.set_page_config(
    page_title="Gestión de Combustibles",
    page_icon="⛽",
    layout="wide"
)

st.title("⛽ Sistema de Gestión de Combustible")

# Menú lateral de navegación con todas las opciones
menu = st.sidebar.selectbox(
    "Navegación",
    ["Estaciones", "Inventarios", "Ventas", "Importador"]
)

# ---------------------------------------------------------
# SECCIÓN 1: ESTACIONES
# ---------------------------------------------------------
if menu == "Estaciones":
    estaciones.mostrar_estaciones()

# ---------------------------------------------------------
# SECCIÓN 2: INVENTARIOS
# ---------------------------------------------------------
elif menu == "Inventarios":
    st.header("📦 Gestión de Inventarios")
    st.write("Consulta y registro de inventarios por estación.")
    # Aquí puedes agregar la lógica o módulo correspondiente a inventarios

# ---------------------------------------------------------
# SECCIÓN 3: VENTAS
# ---------------------------------------------------------
elif menu == "Ventas":
    st.header("💰 Gestión de Ventas")
    st.write("Consulta y registro de ventas por estación.")
    # Aquí puedes agregar la lógica o módulo correspondiente a ventas

# ---------------------------------------------------------
# SECCIÓN 4: IMPORTADOR MASIVO EN 3 PESTAÑAS
# ---------------------------------------------------------
elif menu == "Importador":
    st.header("📁 Módulo de Importación Masiva")
    st.write("Sube tus archivos de Excel (.xlsx) para verificar los datos antes de guardarlos en Supabase.")
    
    # Separación por 3 pestañas independientes
    tab_estaciones, tab_inventarios, tab_ventas = st.tabs(["📍 Estaciones", "📦 Inventarios", "💰 Ventas"])
    
    # -----------------------------------------------------
    # PESTAÑA 1: ESTACIONES
    # -----------------------------------------------------
    with tab_estaciones:
        st.subheader("Importador de Estaciones")
        st.info("Columnas obligatorias: `id_estacion`, `nombre`, `plaza`, `tad`")
        
        archivo_est = st.file_uploader("Subir Excel de Estaciones", type=["xlsx"], key="up_estaciones")
        if archivo_est is not None:
            try:
                df_limpio = importador.limpiar_y_normalizar_estaciones(pd.read_excel(archivo_est))
                
                # Inspección de datos
                st.markdown("### 📊 Confirmación de Datos a Registrar")
                c1, c2 = st.columns(2)
                c1.metric("Total Registros Únicos", len(df_limpio))
                c2.metric("Plazas Detectadas", df_limpio['plaza'].nunique())
                
                st.dataframe(df_limpio, use_container_width=True)
                
                if st.button("Confirmar y Guardar Estaciones", key="btn_estaciones"):
                    exito, res_exitos, res_errores, _ = importador.procesar_importacion_estaciones(archivo_est)
                    if exito:
                        st.success(f"¡Éxito! Registros guardados: {res_exitos}. Errores/Omitidos: {res_errores}")
                        st.rerun()
                    else:
                        st.error(f"Error al procesar: {res_exitos}")
            except Exception as e:
                st.error(f"Error en la estructura del Excel: {e}")

    # -----------------------------------------------------
    # PESTAÑA 2: INVENTARIOS
    # -----------------------------------------------------
    with tab_inventarios:
        st.subheader("Importador de Inventarios")
        st.info("Columnas obligatorias: `id_estacion`, `fecha`, `producto`, `volumen`")
        
        archivo_inv = st.file_uploader("Subir Excel de Inventarios", type=["xlsx"], key="up_inventarios")
        if archivo_inv is not None:
            try:
                df_limpio = importador.limpiar_y_normalizar_inventarios(pd.read_excel(archivo_inv))
                
                # Inspección de datos
                st.markdown("### 📊 Confirmación de Datos a Registrar")
                c1, c2, c3 = st.columns(3)
                c1.metric("Total Registros", len(df_limpio))
                c2.metric("Volumen Total", f"{df_limpio['volumen'].sum():,.2f} Lts")
                c3.metric("Productos", ", ".join(df_limpio['producto'].unique()))
                
                st.dataframe(df_limpio, use_container_width=True)
                
                if st.button("Confirmar y Guardar Inventarios", key="btn_inventarios"):
                    exito, res_exitos, res_errores, _ = importador.procesar_importacion_inventarios(archivo_inv)
                    if exito:
                        st.success(f"¡Éxito! Registros guardados: {res_exitos}. Errores/Omitidos: {res_errores}")
                        st.rerun()
                    else:
                        st.error(f"Error al procesar: {res_exitos}")
            except Exception as e:
                st.error(f"Error en la estructura del Excel: {e}")

    # -----------------------------------------------------
    # PESTAÑA 3: VENTAS
    # -----------------------------------------------------
    with tab_ventas:
        st.subheader("Importador de Ventas")
        st.info("Columnas obligatorias: `id_estacion`, `fecha`, `producto`, `volumen`")
        
        archivo_ven = st.file_uploader("Subir Excel de Ventas", type=["xlsx"], key="up_ventas")
        if archivo_ven is not None:
            try:
                df_limpio = importador.limpiar_y_normalizar_ventas(pd.read_excel(archivo_ven))
                
                # Inspección de datos
                st.markdown("### 📊 Confirmación de Datos a Registrar")
                c1, c2, c3 = st.columns(3)
                c1.metric("Total Registros", len(df_limpio))
                c2.metric("Volumen Vendido Total", f"{df_limpio['volumen'].sum():,.2f} Lts")
                c3.metric("Productos", ", ".join(df_limpio['producto'].unique()))
                
                st.dataframe(df_limpio, use_container_width=True)
                
                if st.button("Confirmar y Guardar Ventas", key="btn_ventas"):
                    exito, res_exitos, res_errores, _ = importador.procesar_importacion_ventas(archivo_ven)
                    if exito:
                        st.success(f"¡Éxito! Registros guardados: {res_exitos}. Errores/Omitidos: {res_errores}")
                        st.rerun()
                    else:
                        st.error(f"Error al procesar: {res_exitos}")
            except Exception as e:
                st.error(f"Error en la estructura del Excel: {e}")
