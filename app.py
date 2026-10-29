import streamlit as st
import pandas as pd
from datetime import date
import database as db
from modulos import importador, inventarios, proyecciones
from servicios import calculos, plantilla  # <-- Importar el servicio de estilos globales
from streamlit_option_menu import option_menu

### Configuración inicial de la página
st.set_page_config(
    page_title="Gestión de Combustibles",
    page_icon="⛽",
    layout="wide"
)

### ---------------------------------------------------------
### APLICAR ESTILOS Y PALETA DE COLORES GLOBAL (plantilla.py)
### ---------------------------------------------------------
plantilla.aplicar_paleta_global()

st.title("⛽ Sistema de Gestión de Combustible")

### ---------------------------------------------------------
### CARGA GLOBAL AL INICIAR LA PÁGINA
### ---------------------------------------------------------
with st.spinner("Cargando y procesando modelos de consumo (12 semanas)..."):
    df_ponderados = calculos.obtener_calculos_combustible()
    df_diarios = calculos.obtener_vdp_diario_12w()

### ---------------------------------------------------------
### MENÚ LATERAL SLIM DE ICONOS CUADRADOS CON EFECTO HOVER
### ---------------------------------------------------------
with st.sidebar:
    menu = option_menu(
        menu_title="Navegación",
        options=["Inventarios", "Proyecciones", "Ventas", "Importador", "Indicadores (Prueba)"],
        icons=["clipboard-data", "graph-up", "bar-chart", "cloud-upload", "cpu"],
        menu_icon="fuel-pump",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#329D9C", "font-size": "20px"},
            "nav-link": {
                "font-size": "14px",
                "text-align": "left",
                "margin": "4px 0px",
                "transition": "0.3s",
                "--hover-color": "#E1F7E7",
            },
            "nav-link-selected": {"background-color": "#329D9C", "color": "white"},
        }
    )

### ---------------------------------------------------------
### SECCIÓN 1: INVENTARIOS
### ---------------------------------------------------------
if menu == "Inventarios":
    inventarios.mostrar_inventarios()

### ---------------------------------------------------------
### SECCIÓN 2: PROYECCIONES
### ---------------------------------------------------------
elif menu == "Proyecciones":
    proyecciones.mostrar_proyecciones()

### ---------------------------------------------------------
### SECCIÓN 3: VENTAS
### ---------------------------------------------------------
elif menu == "Ventas":
    st.header("📊 Módulo de Ventas")
    st.info("Sección en desarrollo.")

### ---------------------------------------------------------
### SECCIÓN 4: IMPORTADOR
### ---------------------------------------------------------
elif menu == "Importador":
    importador.mostrar_importador()

### ---------------------------------------------------------
### SECCIÓN DE PRUEBA DE INDICADORES CARGADOS EN EL SERVICIO
### ---------------------------------------------------------
elif menu == "Indicadores (Prueba)":
    st.header("📈 Indicadores Ponderados (Servicio Centralizado)")
    st.write("Estos datos se cargan una sola vez al abrir la aplicación y están listos para cualquier módulo.")
    
    if not df_ponderados.empty:
        st.subheader("VSP y VDP Ponderada por Estación y Producto")
        st.dataframe(df_ponderados, use_container_width=True)
    else:
        st.info("No hay suficientes datos históricos para calcular las 12 semanas.")
