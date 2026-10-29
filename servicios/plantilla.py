import streamlit as st

def aplicar_paleta_global():
    st.markdown(
        """
        <style>
        /* Estilos generales para encabezados */
        h1, h2, h3 {
            color: #205072 !important;
        }

        /* Personalización de la barra lateral (Sidebar) */
        [data-testid="stSidebar"] {
            background-color: #E1F7E7 !important;
        }

        /* Botones principales de la aplicación */
        .stButton > button {
            background-color: #329D9C !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: 600 !important;
        }
        
        .stButton > button:hover {
            background-color: #205072 !important;
            color: white !important;
        }

        /* Tarjetas de métricas (st.metric) */
        [data-testid="stMetric"] {
            background-color: #FFFFFF;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            border-left: 5px solid #329D9C;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
