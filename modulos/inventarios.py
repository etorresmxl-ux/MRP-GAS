import streamlit as st
import pandas as pd
from datetime import date
import database as db
from servicios import formato


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
        df_inventarios["fecha"] = pd.to_datetime(df_inventarios["fecha"]).dt.date
        df_inv_filtrado = df_inventarios[df_inventarios["fecha"] == fecha_seleccionada]

        if not df_inv_filtrado.empty:
            df_pivot = df_inv_filtrado.pivot_table(
                index="id_estacion",
                columns="producto",
                values="volumen",
                aggfunc="sum",
                fill_value=0
            ).reset_index()

            df_resultado = pd.merge(
                df_estaciones_filtradas[["id_estacion", "nombre", "plaza"]],
                df_pivot,
                on="id_estacion",
                how="left"
            ).fillna(0)
        else:
            df_resultado = df_estaciones_filtradas[["id_estacion", "nombre", "plaza"]].copy()
            df_resultado["Regular"] = 0
            df_resultado["Premium"] = 0
            df_resultado["Diesel"] = 0
    else:
        df_resultado = df_estaciones_filtradas[["id_estacion", "nombre", "plaza"]].copy()
        df_resultado["Regular"] = 0
        df_resultado["Premium"] = 0
        df_resultado["Diesel"] = 0

    for col in ["Regular", "Premium", "Diesel"]:
        if col not in df_resultado.columns:
            df_resultado[col] = 0

    df_resultado = df_resultado[["id_estacion", "nombre", "plaza", "Regular", "Premium", "Diesel"]]

    df_resultado["Regular"] = df_resultado["Regular"].astype(int)
    df_resultado["Premium"] = df_resultado["Premium"].astype(int)
    df_resultado["Diesel"] = df_resultado["Diesel"].astype(int)

    formato.aplicar_estilos_tabla()

    st.markdown(
        """
        <style>
        div[data-testid="stDataFrame"] thead th:nth-child(4) {
            color: #2e7d32 !important;
            font-weight: 700 !important;
        }
        div[data-testid="stDataFrame"] thead th:nth-child(5) {
            color: #b85c00 !important;
            font-weight: 700 !important;
        }
        div[data-testid="stDataFrame"] thead th:nth-child(6) {
            color: #4b4b4b !important;
            font-weight: 700 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    columnas_texto = ["id_estacion", "nombre", "plaza"]
    column_config = formato.generar_column_config(df_resultado, columnas_texto=columnas_texto)

    column_config["id_estacion"] = st.column_config.TextColumn("ID", width="small")
    column_config["nombre"] = st.column_config.TextColumn("Estación", width="medium")
    column_config["plaza"] = st.column_config.TextColumn("Plaza", width="medium")

    # En Streamlit, NumberColumn con format no fuerza separador de miles como se espera;
    # por eso se aplica el formato directamente con Pandas Styler.
    df_formateado = formato.formatear_dataframe_numero(df_resultado, ["Regular", "Premium", "Diesel"])

    st.dataframe(
        df_formateado,
        use_container_width=True,
        hide_index=True,
        column_config=column_config
    )
