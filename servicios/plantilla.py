import streamlit as st

def aplicar_estilos_globales():
    """
    Inyecta la paleta de colores con fondo oscuro en toda la aplicación y aplica
    los estilos CSS para tablas, métricas, botones, reducción de márgenes superiores
    y barra lateral Slim interactiva.
    """
    st.markdown(
        """
        <style>
        /* Color general de fondo y texto principal */
        .stApp {
            background-color: #012538 !important;
            color: #FCEFEF !important;
        }

        /* Reducción del espacio libre superior al mínimo sin causar cortes de texto */
        .block-container, [data-testid="stMainBlockContainer"] {
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
        }

        /* Encabezados compactos y reducción de espacio entre saltos de línea */
        h1, h2, h3, h4, h5, h6 {
            color: #FB9833 !important;
            font-weight: 600 !important;
            margin-top: 0.2rem !important;
            margin-bottom: 0.4rem !important;
            line-height: 1.15 !important;
        }

        /* Reducción de espacio y altura de línea en párrafos e interlineado general */
        p, div, span {
            line-height: 1.25 !important;
        }

        /* ========================================================= */
        /* BARRA LATERAL SLIM Y EFECTO HOVER PARA OPTION_MENU        */
        /* ========================================================= */
        
        /* Forzar ancho estrecho y permitir desbordamiento del tooltip */
        [data-testid="stSidebar"] {
            background-color: #4D555B !important;
            min-width: 80px !important;
            max-width: 80px !important;
            width: 80px !important;
        }

        [data-testid="stSidebar"] > div:first-child {
            overflow: visible !important;
        }

        /* Ocultar botón por defecto de colapsar sidebar */
        [data-testid="stSidebarCollapseButton"] {
            display: none !important;
        }

        /* Ocultar completamente el texto de option_menu por defecto */
        [data-testid="stSidebar"] .nav-link-text {
            display: none !important;
        }
        
        [data-testid="stSidebar"] .nav-link span {
            display: none !important;
        }

        /* Centrar íconos y preparar contenedor del enlace */
        [data-testid="stSidebar"] .nav-link {
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            padding: 12px 0px !important;
            border-radius: 8px !important;
            position: relative !important;
            width: 60px !important;
            margin: 0 auto !important;
        }

        /* Efecto Hover: Mostrar el texto flotante hacia la derecha al pasar el cursor */
        [data-testid="stSidebar"] .nav-link:hover::after {
            content: attr(data-bs-original-title);
            display: inline-block !important;
            position: absolute !important;
            left: 70px !important;
            background-color: #012538 !important;
            color: #FB9833 !important;
            padding: 6px 12px !important;
            border-radius: 6px !important;
            font-weight: bold !important;
            white-space: nowrap !important;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.5) !important;
            z-index: 99999 !important;
            border: 1px solid #1B768E !important;
        }

        [data-testid="stSidebar"] .nav-link:hover span {
            display: inline-block !important;
            position: absolute !important;
            left: 70px !important;
            background-color: #012538 !important;
            color: #FB9833 !important;
            padding: 6px 12px !important;
            border-radius: 6px !important;
            font-weight: bold !important;
            white-space: nowrap !important;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.5) !important;
            z-index: 99999 !important;
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
