import streamlit as st

def aplicar_estilos_globales():
    """
    Inyecta la paleta de colores con fondo oscuro en toda la aplicación y aplica
    los estilos CSS para tablas, métricas, botones y barra lateral Slim interactiva.
    """
    st.markdown(
        """
        <style>
        /* Color general de fondo y texto principal */
        .stApp {
            background-color: #012538 !important;
            color: #FCEFEF !important;
        }

        /* Encabezados */
        h1, h2, h3, h4, h5, h6 {
            color: #FB9833 !important;
            font-weight: 600 !important;
        }

        /* ========================================================= */
        /* BARRA LATERAL SLIM Y EFECTO HOVER PARA OPTION_MENU        */
        /* ========================================================= */
        
        [data-testid="stSidebar"] {
            background-color: #4D555B !important;
            min-width: 80px !important;
            max-width: 80px !important;
            transition: width 0.3s ease;
        }

        /* Ocultar botón por defecto de colapsar sidebar */
        [data-testid="stSidebarCollapseButton"] {
            display: none !important;
        }

        /* Ocultar texto por defecto de las opciones */
        [data-testid="stSidebar"] .nav-link span {
            display: none !important;
        }

        /* Centrar íconos */
        [data-testid="stSidebar"] .nav-link {
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            padding: 12px 0px !important;
            border-radius: 8px !important;
            position: relative !important;
        }

        /* Mostrar etiqueta con el nombre del módulo al pasar el cursor (Hover) */
        [data-testid="stSidebar"] .nav-link:hover span {
            display: inline-block !important;
            position: absolute !important;
            left: 75px !important;
            background-color: #012538 !important;
            color: #FB9833 !important;
            padding: 6px 12px !important;
            border-radius: 6px !important;
            font-weight: bold !important;
            white-space: nowrap !important;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.4) !important;
            z-index: 9999 !important;
            border: 1px solid #1B768E !important;
        }

        /* Botones principales */
        .stButton > button {
            background-color: #FB9833 !important;
            color: #012538 !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: bold !important;
            transition: 0.3s ease;
        }
        
        .stButton > button:hover {
            background-color: #1B768E !important;
            color: #FCEFEF !important;
        }

        /* Tarjetas de métricas (st.metric) */
        [data-testid="stMetric"] {
            background-color: #012538 !important;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            border-left: 5px solid #FB9833 !important;
            border-top: 1px solid #1B768E;
            border-right: 1px solid #1B768E;
            border-bottom: 1px solid #1B768E;
        }

        [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
            color: #FCEFEF !important;
        }

        /* Estilos de tablas y DataFrames */
        div[data-testid="stDataFrame"] thead th {
            background-color: #1B768E !important;
            color: #FCEFEF !important;
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

def aplicar_paleta_global():
    """Compatibilidad con código legado."""
    aplicar_estilos_globales()

def aplicar_estilos_tabla():
    """Inyecta estilos generales para centrar encabezados y contenido."""
    aplicar_estilos_globales()
