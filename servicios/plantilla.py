import streamlit as st


def obtener_tema_streamlit():
    """Obtiene la paleta del tema configurada en .streamlit/config.toml."""
    return {
        "primary": st.get_option("theme.primaryColor") or "#FB9833",
        "background": st.get_option("theme.backgroundColor") or "#012538",
        "secondary_background": st.get_option("theme.secondaryBackgroundColor") or "#4D555B",
        "text": st.get_option("theme.textColor") or "#FCEFEF",
    }


def aplicar_estilos_globales():
    """
    Inyecta la paleta de colores con fondo oscuro en toda la aplicación y aplica
    los estilos CSS para tablas, métricas, botones y barra lateral Slim interactiva.
    """
    tema = obtener_tema_streamlit()

    st.markdown(
        f"""
        <style>
        :root {{
            --primary: {tema['primary']};
            --bg: {tema['background']};
            --sidebar: {tema['secondary_background']};
            --text: {tema['text']};
        }}

        /* Color general de fondo y texto principal */
        .stApp {{
            background-color: var(--bg) !important;
            color: var(--text) !important;
        }}

        /* Encabezados */
        h1, h2, h3, h4, h5, h6 {{
            color: var(--primary) !important;
            font-weight: 600 !important;
        }}

        /* ========================================================= */
        /* BARRA LATERAL SLIM Y EFECTO HOVER PARA OPTION_MENU        */
        /* ========================================================= */

        /* Forzar ancho estrecho y permitir desbordamiento del tooltip */
        [data-testid="stSidebar"] {{
            background-color: var(--sidebar) !important;
            min-width: 80px !important;
            max-width: 80px !important;
            width: 80px !important;
        }}

        [data-testid="stSidebar"] > div:first-child {{
            overflow: visible !important;
        }}

        /* Ocultar botón por defecto de colapsar sidebar */
        [data-testid="stSidebarCollapseButton"] {{
            display: none !important;
        }}

        /* Ocultar completamente el texto de option_menu por defecto */
        [data-testid="stSidebar"] .nav-link-text {{
            display: none !important;
        }}

        [data-testid="stSidebar"] .nav-link span {{
            display: none !important;
        }}

        /* Centrar íconos y preparar contenedor del enlace */
        [data-testid="stSidebar"] .nav-link {{
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            padding: 12px 0px !important;
            border-radius: 8px !important;
            position: relative !important;
            width: 60px !important;
            margin: 0 auto !important;
        }}

        /* Efecto Hover: Mostrar el texto flotante hacia la derecha al pasar el cursor */
        [data-testid="stSidebar"] .nav-link:hover::after {{
            content: attr(data-bs-original-title);
            display: inline-block !important;
            position: absolute !important;
            left: 70px !important;
            background-color: var(--bg) !important;
            color: var(--primary) !important;
            padding: 6px 12px !important;
            border-radius: 6px !important;
            font-weight: bold !important;
            white-space: nowrap !important;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.5) !important;
            z-index: 99999 !important;
            border: 1px solid #1B768E !important;
        }}

        [data-testid="stSidebar"] .nav-link:hover span {{
            display: inline-block !important;
            position: absolute !important;
            left: 70px !important;
            background-color: var(--bg) !important;
            color: var(--primary) !important;
            padding: 6px 12px !important;
            border-radius: 6px !important;
            font-weight: bold !important;
            white-space: nowrap !important;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.5) !important;
            z-index: 99999 !important;
            border: 1px solid #1B768E !important;
        }}

        /* Botones principales */
        .stButton > button {{
            background-color: var(--primary) !important;
            color: var(--bg) !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: bold !important;
            transition: 0.3s ease;
        }}

        .stButton > button:hover {{
            background-color: #1B768E !important;
            color: #FCEFEF !important;
        }}

        /* Tarjetas de métricas (st.metric) */
        [data-testid="stMetric"] {{
            background-color: var(--bg) !important;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            border-left: 5px solid var(--primary) !important;
            border-top: 1px solid #1B768E;
            border-right: 1px solid #1B768E;
            border-bottom: 1px solid #1B768E;
        }}

        [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {{
            color: var(--text) !important;
        }}

        /* Estilos de tablas y DataFrames */
        div[data-testid="stDataFrame"] thead th {{
            background-color: #1B768E !important;
            color: #FCEFEF !important;
            text-align: center !important;
            justify-content: center !important;
            font-weight: 600 !important;
        }}

        div[data-testid="stDataFrame"] tbody td {{
            text-align: center !important;
        }}
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
