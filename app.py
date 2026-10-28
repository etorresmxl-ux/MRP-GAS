import streamlit as st
import database as db
from servicios import calculos, formato
from modulos import inventarios, proyecciones, importador

# Configuración inicial de la página
st.set_page_config(
    page_title="Gestión de Combustibles",
    page_icon="⛽",
    layout="wide"
)

# ---------------------------------------------------------
# CARGA GLOBAL AL INICIAR LA PÁGINA (Evita redundancias)
# ---------------------------------------------------------
with st.spinner("Cargando y procesando modelos de consumo..."):
    df_ponderados = calculos.obtener_calculos_combustible()
    df_diarios = calculos.obtener_vdp_diario_12w()

# 1. Título en la barra lateral
st.sidebar.title("⛽ Gestión de Combustible")

# Menú lateral de navegación reordenado
menu = st.sidebar.radio(
    "Selecciona una sección",
    ["Inventarios", "Ventas", "Proyecciones", "Importador", "Indicadores"],
    label_visibility="collapsed"
)

# ---------------------------------------------------------
# SECCIÓN 1: INVENTARIOS
# ---------------------------------------------------------
if menu == "Inventarios":
    inventarios.mostrar_inventarios()

# ---------------------------------------------------------
# SECCIÓN 2: VENTAS
# ---------------------------------------------------------
elif menu == "Ventas":
    st.header("📊 Módulo de Ventas")
    st.info("Sección en desarrollo.")

# ---------------------------------------------------------
# SECCIÓN 3: PROYECCIONES
# ---------------------------------------------------------
elif menu == "Proyecciones":
    proyecciones.mostrar_proyecciones()

# ---------------------------------------------------------
# SECCIÓN 4: IMPORTADOR
# ---------------------------------------------------------
elif menu == "Importador":
    importador.mostrar_importador()

# ---------------------------------------------------------
# SECCIÓN 5: INDICADORES
# ---------------------------------------------------------
elif menu == "Indicadores":
    st.header("📈 Indicadores Ponderados (Servicio Centralizado)")
    st.write("Estos datos se cargan una sola vez al abrir la aplicación y están listos para cualquier módulo.")
    
    if not df_ponderados.empty:
        st.subheader("VSP y VDP Ponderada por Estación y Producto")
        
        # Aplicar el servicio global de formato de tablas
        formato.aplicar_estilos_tabla()
        column_config = formato.generar_column_config(df_ponderados)
        
        st.dataframe(
            df_ponderados, 
            use_container_width=True, 
            hide_index=True,
            column_config=column_config
        )
    else:
        st.info("No hay suficientes datos históricos para calcular las 12 semanas.")
