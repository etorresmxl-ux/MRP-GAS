import streamlit as st
import pandas as pd
import database as db
from servicios import formato

def mostrar_inventarios():
    st.header("📋 Consulta de Inventarios")

    # 1. Obtener datos de inventarios y estaciones desde la BD
    datos_inventarios = db.obtener_inventarios()
    datos_estaciones = db.obtener_estaciones()

    if not datos_inventarios:
        st.info("No hay registros de inventario disponibles en la base de datos.")
        return

    df_inv = pd.DataFrame(datos_inventarios)
    
    # Asegurar formato de fecha legible si existe
    if "fecha" in df_inv.columns:
        df_inv["fecha"] = pd.to_datetime(df_inv["fecha"]).dt.strftime("%Y-%m-%d")

    # 2. Filtros opcionales por Estación / Plaza si se cuenta con el catálogo de estaciones
    if datos_estaciones:
        df_estaciones = pd.DataFrame(datos_estaciones)
        
        # Merge para enriquecer con nombre de estación o plaza si es necesario
        if "id_estacion" in df_inv.columns and "id_estacion" in df_estaciones.columns:
            df_inv = pd.merge(df_inv, df_estaciones[["id_estacion", "nombre", "plaza"]], on="id_estacion", how="left")

        col1, col2 = st.columns(2)
        with col1:
            plazas = ["Todas"] + sorted(list(df_inv["plaza"].dropna().unique())) if "plaza" in df_inv.columns else ["Todas"]
            plaza_sel = st.selectbox("Filtrar por Plaza:", options=plazas, key="filtro_plaza_inv")
            if plaza_sel != "Todas" and "plaza" in df_inv.columns:
                df_inv = df_inv[df_inv["plaza"] == plaza_sel]

        with col2:
            productos = ["Todos"] + sorted(list(df_inv["producto"].dropna().unique())) if "producto" in df_inv.columns else ["Todos"]
            prod_sel = st.selectbox("Filtrar por Producto:", options=productos, key="filtro_prod_inv")
            if prod_sel != "Todos" and "producto" in df_inv.columns:
                df_inv = df_inv[df_inv["producto"].str.capitalize() == prod_sel.capitalize()]

    # 3. Aplicar el servicio centralizado de formato
    formato.aplicar_estilos_tabla()
    
    # Generar configuración de columnas (si el volumen requiere decimales, se puede agregar a excepciones_decimales)
    column_config = formato.generar_column_config(
        df_inv, 
        excepciones_decimales=["volumen"] # Permite que el volumen muestre decimales o formato numérico adecuado
    )

    # 4. Renderizar tabla con diseño limpio y centralizado
    st.dataframe(
        df_inv,
        use_container_width=True,
        hide_index=True,
        column_config=column_config
    )
