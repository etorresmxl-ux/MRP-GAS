import streamlit as st
import pandas as pd
from datetime import date
import database as db
from modulos import importador, inventarios, proyecciones
from servicios import calculos, plantilla
from streamlit_option_menu import option_menu

##### Configuración inicial de la página
st.set_page_config(
    page_title="Gestión de Combustibles",
    page_icon="⛽",
    layout="wide"
)

##### ---------------------------------------------------------
##### APLICAR ESTILOS Y PALETA DE COLORES GLOBAL (plantilla.py)
##### ---------------------------------------------------------
plantilla.aplicar_paleta_global()

##### ---------------------------------------------------------
##### MENÚ LATERAL SLIM CON ÍCONOS Y SIN TÍTULO
##### ---------------------------------------------------------
st.markdown(
    """
    <style>
    section[data-testid="stSidebar"] {
        width: 92px !important;
        min-width: 92px !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] .nav-section-title {
        display: none !important;
    }

    div[data-testid="stSidebarNav"] a {
        justify-content: center !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        margin: 6px 0px !important;
    }

    div[data-testid="stSidebarNav"] a > span:last-child {
        display: none !important;
    }

    div[data-testid="stSidebarNav"] a > span:first-child {
        margin-right: 0 !important;
        font-size: 1.4rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    menu = option_menu(
        menu_title="",
        options=["Inventarios", "Proyecciones", "Ventas", "Importador", "Indicadores (Prueba)"],
        icons=["clipboard-data", "graph-up", "bar-chart", "cloud-upload", "cpu"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"font-size": "22px"},
            "nav-link": {
                "margin": "8px 0px",
                "transition": "0.2s",
                "font-size": "0px",
                "text-align": "center",
            },
            "nav-link-selected": {"background-color": "#FB9833", "color": "#012538"},
        }
    )

##### ---------------------------------------------------------
##### CARGA GLOBAL AL INICIAR LA PÁGINA
##### ---------------------------------------------------------
with st.spinner("Cargando y procesando modelos de consumo (12 semanas)..."):
    df_ponderados = calculos.obtener_calculos_combustible()
    df_diarios = calculos.obtener_vdp_diario_12w()

##### ---------------------------------------------------------
##### SECCIÓN 1: INVENTARIOS
##### ---------------------------------------------------------
if menu == "Inventarios":
    inventarios.mostrar_inventarios()

##### ---------------------------------------------------------
##### SECCIÓN 2: PROYECCIONES
##### ---------------------------------------------------------
elif menu == "Proyecciones":
    proyecciones.mostrar_proyecciones()

##### ---------------------------------------------------------
##### SECCIÓN 3: VENTAS
##### ---------------------------------------------------------
elif menu == "Ventas":
    st.header("📊 Módulo de Ventas")
    st.info("Sección en desarrollo.")

##### ---------------------------------------------------------
##### SECCIÓN 4: IMPORTADOR
##### ---------------------------------------------------------
elif menu == "Importador":
    importador.mostrar_importador()

##### ---------------------------------------------------------
##### SECCIÓN DE PRUEBA DE INDICADORES CARGADOS EN EL SERVICIO
##### ---------------------------------------------------------
elif menu == "Indicadores (Prueba)":
    st.header("📈 Indicadores Ponderados (Servicio Centralizado)")
    st.write("Estos datos se cargan una sola vez al abrir la aplicación y están listos para cualquier módulo.")
    
    if not df_ponderados.empty:
        st.subheader("VSP y VDP Ponderada por Estación y Producto")
        st.dataframe(df_ponderados, use_container_width=True)
    else:
        st.info("No hay suficientes datos históricos para calcular las 12 semanas.")
