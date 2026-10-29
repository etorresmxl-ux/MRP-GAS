import streamlit as st
import pandas as pd
from datetime import date
import database as db
from modulos import importador, inventarios, proyecciones
from servicios import calculos, plantilla, validacion
from streamlit_option_menu import option_menu

# Configuración inicial de la página
st.set_page_config(
    page_title="Gestión de Combustibles",
    page_icon="⛽",
    layout="wide"
)

# ---------------------------------------------------------
# APLICAR ESTILOS Y PALETA DE COLORES GLOBAL (plantilla.py)
# ---------------------------------------------------------
plantilla.aplicar_estilos_globales()

# ---------------------------------------------------------
# MENÚ LATERAL DE NAVEGACIÓN
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/gas-station.png", width=80)
    st.title("MRP Gas")
    
    menu = option_menu(
        menu_title="Menú Principal",
        options=["Inventarios", "Proyecciones", "Ventas", "Importador"],
        icons=["clipboard-data", "graph-up", "bar-chart", "upload"],
        default_index=0,
    )

# ---------------------------------------------------------
# CARGA GLOBAL AL INICIAR LA PÁGINA
# ---------------------------------------------------------
with st.spinner("Cargando y procesando modelos de consumo (12 semanas)..."):
    df_ponderados = calculos.obtener_calculos_combustible()
    df_diarios = calculos.obtener_vdp_diario_12w()

# ---------------------------------------------------------
# SECCIÓN 1: INVENTARIOS
# ---------------------------------------------------------
if menu == "Inventarios":
    inventarios.mostrar_inventarios()

# ---------------------------------------------------------
# SECCIÓN 2: PROYECCIONES
# ---------------------------------------------------------
elif menu == "Proyecciones":
    proyecciones.mostrar_proyecciones()

# ---------------------------------------------------------
# SECCIÓN 3: VENTAS
# ---------------------------------------------------------
elif menu == "Ventas":
    st.header("📊 Módulo de Ventas")
    st.info("Sección en desarrollo.")

# ---------------------------------------------------------
# SECCIÓN 4: IMPORTADOR
# ---------------------------------------------------------
elif menu == "Importador":
    importador.mostrar_importador()
