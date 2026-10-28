import streamlit as st
import pandas as pd
from datetime import date
import database as db
from modulos import importador
from modulos import estaciones
from modulos import inventarios  # Módulo de inventarios integrado
from servicios import calculos  # <-- Importamos nuestro servicio centralizado

### Configuración inicial de la página
st.set_page_config(
    page_title="Gestión de Combustibles",
    page_icon="⛽",
    layout="wide"
)

st.title("⛽ Sistema de Gestión de Combustible")

### ---------------------------------------------------------
### CARGA GLOBAL AL INICIAR LA PÁGINA (Evita redundancias)
### ---------------------------------------------------------
with st.spinner("Cargando y procesando modelos de consumo (12 semanas)..."):
    df_ponderados = calculos.obtener_calculos_combustible()
    df_diarios = calculos.obtener_vdp_diario_12w()

### Menú lateral de navegación
menu = st.sidebar.radio(
    "Selecciona una sección",
    ["Estaciones", "Inventarios", "Ventas", "Importador", "Indicadores (Prueba)"],
    label_visibility="collapsed"
)

### ---------------------------------------------------------
### SECCIÓN 1: ESTACIONES
### ---------------------------------------------------------
if menu == "Estaciones":
    estaciones.mostrar_estaciones()

### ---------------------------------------------------------
### SECCIÓN 2: INVENTARIOS
### ---------------------------------------------------------
elif menu == "Inventarios":
    inventarios.mostrar_inventarios()

### ---------------------------------------------------------
### SECCIÓN 3: IMPORTADOR
### ---------------------------------------------------------
elif menu == "Importador":
    importador.mostrar_importador()

### ---------------------------------------------------------
### SECCIÓN DE PRUEBA DE INDICADORES CARGADOS EN EL SERVICIO
### ---------------------------------------------------------
elif menu == "Indicadores (Prueba)":
    st.header("📈 Indicadores Ponderados (Servicio Centralizado)")
    st.write("Estos datos se cargan una sola vez al abrir la aplicación y están listos para cualquier módulo (como programación de combustible).")
    
    if not df_ponderados.empty:
        st.subheader("VSP y VDP Ponderada por Estación y Producto")
        st.dataframe(df_ponderados, use_container_width=True)
    else:
        st.info("No hay suficientes datos históricos para calcular las 12 semanas.")
