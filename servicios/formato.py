import streamlit as st
import pandas as pd


def aplicar_estilos_tabla():
    """
    Inyecta estilos generales para centrar encabezados y contenido
    de las tablas de Streamlit sin depender de selectores CSS no soportados.
    """
    st.markdown(
        """
        <style>
        div[data-testid="stDataFrame"] thead th {
            text-align: center !important;
            justify-content: center !important;
            font-weight: 600 !important;
        }

        div[data-testid="stDataFrame"] tbody td {
            text-align: center !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def generar_column_config(df, excepciones_decimales=None, columnas_texto=None):
    """
    Genera automáticamente el diccionario column_config para st.dataframe:
    - Las columnas de texto se configuran como TextColumn.
    - Las columnas numéricas se configuran con separador de miles (%d o '%,d').
    """
    if excepciones_decimales is None:
        excepciones_decimales = []
    if columnas_texto is None:
        columnas_texto = ["Concepto", "id_estacion", "nombre", "plaza", "tad", "producto", "fecha"]

    column_config = {}
    for col in df.columns:
        if col in columnas_texto:
            column_config[col] = st.column_config.TextColumn(col)
        elif pd.api.types.is_numeric_dtype(df[col]):
            if col in excepciones_decimales:
                column_config[col] = st.column_config.NumberColumn(col, format="%.1f")
            else:
                column_config[col] = st.column_config.NumberColumn(col)
        else:
            column_config[col] = st.column_config.TextColumn(col)

    return column_config


def formatear_dataframe_numero(df, columnas=None):
    """
    Devuelve un Styler con miles separados para columnas numéricas.
    Esto es más fiable que depender solo de NumberColumn en Streamlit.
    """
    if columnas is None:
        columnas = ["Regular", "Premium", "Diesel"]

    columnas = [c for c in columnas if c in df.columns]
    if not columnas:
        return df

    styler = df.style.format({col: "{:,.0f}" for col in columnas})
    return styler
