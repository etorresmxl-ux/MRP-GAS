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
                # Usar formato entero con separador de miles estándar de Streamlit
                column_config[col] = st.column_config.NumberColumn(col, format="%d")
        else:
            column_config[col] = st.column_config.TextColumn(col)

    return column_config
