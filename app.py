import streamlit as st
import pandas as pd
from datetime import date
import database as db
from modulos import importador, inventarios, proyecciones
from servicios import calculos, plantilla, validacion

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

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        width: 90px !important;
        min-width: 90px !important;
        max-width: 90px !important;
    }
    [data-testid="stSidebar"] .stRadio {
        width: 100%;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] {
        display: flex !important;
        flex-direction: column !important;
        gap: 0.45rem !important;
    }
    [data-testid="stSidebar"] label {
        justify-content: center !important;
        text-align: center !important;
        padding: 0.5rem 0.2rem !important;
        border-radius: 10px !important;
        min-height: 2.6rem !important;
        font-size: 0.72rem !important;
        line-height: 1.1 !important;
    }
    [data-testid="stSidebar"] label > div:first-child {
        display: none !important;
    }
    [data-testid="stSidebar"] label > span:last-child {
        white-space: normal !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# MENÚ LATERAL DE NAVEGACIÓN
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/gas-station.png", width=60)
    st.title("MRP Gas")

    menu = st.radio(
        " ",
        ["Inventarios", "Proyecciones", "Ventas", "Importador"],
        index=0,
        label_visibility="collapsed",
        key="sidebar_menu"
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
