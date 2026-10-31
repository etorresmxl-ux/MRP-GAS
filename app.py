import streamlit as st
import pandas as pd
from datetime import date
import database as db
from modulos import importador, inventarios, proyecciones
from servicios import calculos
from streamlit_option_menu import option_menu

# Configuración inicial de la página
st.set_page_config(
    page_title="Gestión de Combustibles",
    page_icon="⛽",
    layout="wide"
)

# ---------------------------------------------------------
# MENÚ LATERAL DE NAVEGACIÓN (SLIM / SOLO ÍCONOS)
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/gas-station.png", width=50)
    
    # Menú slim configurado sin texto en las opciones
    menu_index = option_menu(
        menu_title=None,
        options=["", "", "", ""],
        icons=["clipboard-data", "graph-up", "bar-chart", "upload"],
        default_index=0,
        styles={
            "container": {"padding": "0!important"},
            "nav-link": {"justify-content": "center", "padding": "12px 0px", "font-size": "18px"},
            "nav-link-selected": {"background-color": "#5B7470"},
        }
    )

    # Mapeo del índice devuelto (0 a 3) a las secciones correspondientes
    secciones = ["Inventarios", "Proyecciones", "Ventas", "Importador"]
    menu = secciones[menu_index]

# ---------------------------------------------------------
# CARGA GLOBAL AL INICIAR LA PÁGINA
# ---------------------------------------------------------
with st.spinner("Cargando y procesando modelos de consumo (12 semanas)..."):
    df_ponderados = calculos.obtener_calculos_combustible()

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
