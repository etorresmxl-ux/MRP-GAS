import streamlit as st
import pandas as pd

def aplicar_estilos_tabla():
    """
    Inyecta el CSS global para centrar los títulos de los encabezados en todas las tablas (st.dataframe).
    """
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

def generar_column_config(df, excepciones_decimales=None, columnas_texto=None):
    """
    Genera automáticamente el diccionario column_config para st.dataframe:
    - Las columnas de texto se configuran como TextColumn.
    - Las columnas numéricas se configuran como enteros (%d).
    - Aplica excepciones con decimales (ej. 'D/S' con '%.1f').
    """
    if excepciones_decimales is None:
        excepciones_decimales = []
    if columnas_texto is None:
        columnas_texto = ["Concepto", "id_estacion", "nombre", "plaza", "tad", "producto", "fecha"]

    column_config = {}
    
    for col in df.columns:
        # Si la columna es de texto o identificadores conocidos
        if col in columnas_texto or col.lower() in [c.lower() for c in columnas_texto]:
            column_config[col] = st.column_config.TextColumn(col)
        elif pd.api.types.is_numeric_dtype(df[col]):
            # Validar si esta columna específica es una excepción que requiere decimales
            if col in excepciones_decimales:
                column_config[col] = st.column_config.NumberColumn(
                    col,
                    format="%.1f"
                )
            else:
                # Formato numérico estándar para enteros
                column_config[col] = st.column_config.NumberColumn(
                    col,
                    format="%d"
                )
        else:
            column_config[col] = st.column_config.TextColumn(col)
            
    return column_config
