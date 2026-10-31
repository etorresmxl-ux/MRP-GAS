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
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# ESTILOS CSS PERSONALIZADOS (Sidebar Flotante y Hover Automático)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* 1. Ancho base colapsado (solo muestra íconos) y transición fluida */
    [data-testid="stSidebar"] {
        transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 85px !important;
        min-width: 85px !important;
        background-color: transparent !important;
    }

    /* 2. Al colocar el cursor (hover), se expande al ancho completo */
    [data-testid="stSidebar"]:hover {
        width: 260px !important;
        min-width: 260px !important;
    }

    /* 3. Comportamiento de los textos: ocultos por defecto, visibles en hover */
    [data-testid="stSidebar"] .sidebar-text,
    [data-testid="stSidebar"] span:not(.icon-fixed),
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] .nav-link-text {
        opacity: 0;
        transition: opacity 0.2s ease-in-out;
        white-space: nowrap;
        pointer-events: none;
    }

    /* Revelar textos y elementos al hacer hover sobre la barra lateral */
    [data-testid="stSidebar"]:hover .sidebar-text,
    [data-testid="stSidebar"]:hover span:not(.icon-fixed),
    [data-testid="stSidebar"]:hover p,
    [data-testid="stSidebar"]:hover div[data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"]:hover .nav-link-text {
        opacity: 1;
        pointer-events: auto;
    }

    /* Contenedor interno con diseño flotante oscuro moderno */
    [data-testid="stSidebarContent"] {
        background-color: #16181d;
        border-radius: 20px;
        margin: 10px;
        padding: 16px 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        overflow-x: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# MENÚ LATERAL DE NAVEGACIÓN
# ---------------------------------------------------------
with st.sidebar:
    # Cabecera del Sidebar
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 14px; padding: 6px 4px; margin-bottom: 24px;">
            <div style="background: #ffffff; border-radius: 14px; width: 42px; height: 42px; display: flex; align-items: center; justify-content: center; color: #000; font-weight: bold; flex-shrink: 0;">⛽</div>
            <span class="sidebar-text" style="font-weight: 700; font-size: 16px; color: #fff;">MRP Gas</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="sidebar-text" style="color: #6b7280; font-size: 11px; font-weight: 600; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 0.5px;">Menú Principal</p>', unsafe_allow_html=True)

    # Menú interactivo con soporte de íconos y textos colapsables
    menu = option_menu(
        menu_title=None,
        options=["Inventarios", "Proyecciones", "Ventas", "Importador"],
        icons=["clipboard-data", "graph-up", "bar-chart", "upload"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#9ca3af", "font-size": "18px"},
            "nav-link": {
                "font-size": "14px",
                "text-align": "left",
                "margin": "4px 0px",
                "color": "#9ca3af",
                "border-radius": "10px",
                "padding": "10px 12px",
                "font-weight": "500",
            },
            "nav-link-selected": {
                "background-color": "#23262e",
                "color": "#ffffff",
                "font-weight": "600",
            },
        }
    )

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
