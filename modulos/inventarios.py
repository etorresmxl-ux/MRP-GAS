import streamlit as st
import pandas as pd
from datetime import date
import database as db

def mostrar_inventarios():
    st.header("📋 Consulta de Inventarios")

    # 1. Obtener información de la base de datos
    datos_estaciones = db.obtener_estaciones()
    datos_inventarios = db.obtener_inventarios()

    if not datos_estaciones:
        st.warning("No hay estaciones registradas en la base de datos.")
        return

    df_estaciones = pd.DataFrame(datos_estaciones)

    # 2. Filtros principales: Fecha y Plaza
    col_fecha, col_plaza = st.columns(2)

    with col_fecha:
        fecha_seleccionada = st.date_input(
            "Selecciona la fecha:",
            value=date.today(),
            key="filtro_fecha_inventarios"
        )

    with col_plaza:
        plazas_disponibles = ["Todas"] + sorted(list(df_estaciones["plaza"].unique()))
        plaza_seleccionada = st.selectbox(
            "Selecciona la plaza:",
            options=plazas_disponibles,
            key="filtro_plaza_inventarios"
        )

    # 3. Filtrar estaciones según la plaza seleccionada
    if plaza_seleccionada != "Todas":
        df_estaciones_filtradas = df_estaciones[df_estaciones["plaza"] == plaza_seleccionada]
    else:
        df_estaciones_filtradas = df_estaciones.copy()

    if df_estaciones_filtradas.empty:
        st.info("No hay estaciones registradas para la plaza seleccionada.")
        return

    # 4. Procesar y filtrar datos de inventario si existen
    if datos_inventarios:
        df_inventarios = pd.DataFrame(datos_inventarios)
        
        # Asegurar formato correcto de fecha para el filtro
        df_inventarios["fecha"] = pd.to_datetime(df_inventarios["fecha"]).dt.date

        # Filtrar inventarios por fecha
        df_inv_filtrado = df_inventarios[df_inventarios["fecha"] == fecha_seleccionada]

        if not df_inv_filtrado.empty:
            # Pivotar el producto en columnas (Regular, Premium, Diesel)
            df_pivot = df_inv_filtrado.pivot_table(
                index="id_estacion",
                columns="producto",
                values="volumen",
                aggfunc="sum",
                fill_value=0
            ).reset_index()
            
            # Unir las estaciones filtradas por plaza con el inventario
            df_resultado = pd.merge(
                df_estaciones_filtradas[["id_estacion", "nombre", "plaza"]],
                df_pivot,
                on="id_estacion",
                how="left"
            ).fillna(0)
        else:
            # Si no hay registros en la fecha seleccionada, mostrar inventarios en 0
            df_resultado = df_estaciones_filtradas[["id_estacion", "nombre", "plaza"]].copy()
            df_resultado["Regular"] = 0
            df_resultado["Premium"] = 0
            df_resultado["Diesel"] = 0
    else:
        # Si la tabla de inventarios está completamente vacía
        df_resultado = df_estaciones_filtradas[["id_estacion", "nombre", "plaza"]].copy()
        df_resultado["Regular"] = 0
        df_resultado["Premium"] = 0
        df_resultado["Diesel"] = 0

    # Asegurar que existan las columnas de combustible requeridas
    for col in ["Regular", "Premium", "Diesel"]:
        if col not in df_resultado.columns:
            df_resultado[col] = 0

    # Reordenar columnas exactas requeridas
    df_resultado = df_resultado[["id_estacion", "nombre", "plaza", "Regular", "Premium", "Diesel"]]

    # Convertir volúmenes a enteros
    df_resultado["Regular"] = df_resultado["Regular"].astype(int)
    df_resultado["Premium"] = df_resultado["Premium"].astype(int)
    df_resultado["Diesel"] = df_resultado["Diesel"].astype(int)

    # Estilo CSS para centrar títulos de columnas
    st.markdown("""
        <style>
        [data-testid="stHeaderCell"] {
            text-align: center !important;
        }
        [data-testid="stHeaderCell"] > div {
            justify-content: center !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # 5. Renderizado de la tabla con configuración de columnas
    st.dataframe(
        df_resultado,
        use_container_width=True,
        hide_index=True,
        column_config={
            "id_estacion": st.column_config.TextColumn("ID"),
            "nombre": st.column_config.TextColumn("Estacion"),
            "plaza": st.column_config.TextColumn("Plaza"),
            "Regular": st.column_config.NumberColumn(
                "Regular",
                format="%d",
                help="Volumen Regular en Litros"
            ),
            "Premium": st.column_config.NumberColumn(
                "Premium",
                format="%d",
                help="Volumen Premium en Litros"
            ),
            "Diesel": st.column_config.NumberColumn(
                "Diesel",
                format="%d",
                help="Volumen Diesel en Litros"
            ),
        }
    )
