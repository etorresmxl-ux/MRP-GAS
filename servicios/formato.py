import streamlit as st
import pandas as pd

def aplicar_estilos_tabla():
    """
    Inyecta el CSS global para centrar los títulos y aplicar colores específicos 
    a los encabezados de Regular (verde), Premium (naranja obscuro) y Diesel (gris obscuro).
    """
    st.markdown("""
        <style>
        /* Centrar todos los encabezados de tabla */
        [data-testid="stHeaderCell"] {
            text-align: center !important;
        }
        [data-testid="stHeaderCell"] > div {
            justify-content: center !important;
        }
        
        /* Colores personalizados para los títulos de combustibles en los encabezados */
        [data-testid="stHeaderCell"] div[data-testid="stMarkdownContainer"] p:has-text("Regular"),
        [data-testid="stHeaderCell"]:has(div:contains("Regular")) span,
        [data-testid="stHeaderCell"]:has(div:contains("Regular")) div {
            color: #2e7d32 !important;
        }
        
        [data-testid="stHeaderCell"]:has(div:contains("Premium")) span,
        [data-testid="stHeaderCell"]:has(div:contains("Premium")) div {
            color: #d84315 !important;
        }
        
        [data-testid="stHeaderCell"]:has(div:contains("Diesel")) span,
        [data-testid="stHeaderCell"]:has(div:contains("Diesel")) div {
            color: #424242 !important;
        }
        </style>
    """, unsafe_allow_html=True)

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
