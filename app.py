import streamlit as st
import pandas as pd
from datetime import date
import database as db
from modulos import importador   # <-- Importado desde la carpeta modulos
from modulos import estaciones   # <-- Importado desde la carpeta modulos

# Configuración inicial de la página
st.set_page_config(
    page_title="Gestión de Combustibles",
    page_icon="⛽",
    layout="wide"
)

st.title("⛽ Sistema de Gestión de Combustible")

# Menú lateral actualizado con las opciones correspondientes
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
# SECCIÓN 4: IMPORTADOR MASIVO
# ---------------------------------------------------------
elif menu == "Importador":
    st.header("📁 Módulo de Importación Masiva de Estaciones")
    st.write("Sube tu archivo de Excel (.xlsx) para realizar la limpieza, normalización y carga masiva automática a Supabase.")
    
    archivo_excel = st.file_uploader("Selecciona el archivo Excel", type=["xlsx"], key="upload_importador")

    if archivo_excel is not None:
        try:
            # Vista previa rápida del archivo cargado
            df_preview = pd.read_excel(archivo_excel)
            st.subheader("Vista previa de los datos:")
            st.dataframe(df_preview.head(), use_container_width=True)
            
            if st.button("Procesar y Guardar en Supabase"):
                exito, res_exitos, res_errores, df_procesado = importador.procesar_importacion_estaciones(archivo_excel)
                if exito:
                    st.success(f"¡Importación exitosa! Registros guardados: {res_exitos}. Omitidos o con error: {res_errores}.")
                    st.rerun()
                else:
                    st.error(f"Error al procesar la importación: {res_exitos}")
        except Exception as e:
            st.error(f"No se pudo leer el archivo Excel: {e}")
