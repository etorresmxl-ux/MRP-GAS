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
    """Inyecta el tema visual global en la aplicación."""
    tema = obtener_tema_streamlit()
    accent = "#1B768E"

    st.markdown(
        f"""
        <style>
        :root {{
            --primary: {tema['primary']};
            --bg: {tema['background']};
            --sidebar: {tema['secondary_background']};
            --text: {tema['text']};
            --accent: {accent};
        }}

        html, body, [data-testid="stAppViewContainer"], .stApp {{
            background: var(--bg) !important;
            color: var(--text) !important;
        }}

        .main .block-container {{
            padding-top: 0.35rem !important;
            padding-bottom: 0.15rem !important;
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
            margin-top: 0 !important;
            max-width: 100% !important;
        }}

        header[data-testid="stHeader"] {{
            background: transparent !important;
            box-shadow: none !important;
        }}

        footer {{
            visibility: hidden !important;
        }}

        #MainMenu {{
            display: none !important;
        }}

        div[data-testid="stVerticalBlock"] > div {{
            gap: 0.15rem !important;
        }}

        h1, h2, h3, h4, h5, h6 {{
            color: var(--primary) !important;
            font-weight: 600 !important;
            margin-top: 0.15rem !important;
            margin-bottom: 0.25rem !important;
            line-height: 1.15 !important;
        }}

        [data-testid="stSidebar"] {{
            background-color: var(--sidebar) !important;
            min-width: 66px !important;
            max-width: 66px !important;
            width: 66px !important;
            border: none !important;
            box-shadow: none !important;
        }}

        [data-testid="stSidebar"] > div:first-child {{
            overflow: visible !important;
            padding-top: 0.2rem !important;
        }}

        [data-testid="stSidebarCollapseButton"] {{
            display: none !important;
        }}

        [data-testid="stSidebar"] .nav-link-text,
        [data-testid="stSidebar"] .nav-link span {{
            display: none !important;
        }}

        [data-testid="stSidebar"] .nav-link {{
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            padding: 8px 0 !important;
            border-radius: 8px !important;
            position: relative !important;
            width: 52px !important;
            margin: 0 auto !important;
            border: none !important;
        }}

        [data-testid="stSidebar"] .nav-link:hover::after,
        [data-testid="stSidebar"] .nav-link:hover span {{
            content: attr(data-bs-original-title);
            display: inline-block !important;
            position: absolute !important;
            left: 60px !important;
            background-color: var(--bg) !important;
            color: var(--primary) !important;
            padding: 5px 10px !important;
            border-radius: 6px !important;
            font-weight: bold !important;
            white-space: nowrap !important;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.35) !important;
            z-index: 99999 !important;
            border: 1px solid var(--accent) !important;
        }}

        .stButton > button {{
            background-color: var(--primary) !important;
            color: var(--bg) !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: 700 !important;
            transition: 0.2s ease;
            margin-top: 0.05rem !important;
            margin-bottom: 0.05rem !important;
            padding: 0.35rem 0.75rem !important;
            min-height: 2.1rem !important;
        }}

        .stButton > button:hover {{
            background-color: var(--accent) !important;
            color: var(--text) !important;
        }}

        [data-testid="stMetric"] {{
            background-color: var(--bg) !important;
            padding: 10px 12px !important;
            border-radius: 10px;
            box-shadow: none !important;
            border-left: 4px solid var(--primary) !important;
            border-top: 1px solid var(--accent) !important;
            border-right: 1px solid var(--accent) !important;
            border-bottom: 1px solid var(--accent) !important;
        }}

        [data-testid="stMetricLabel"],
        [data-testid="stMetricValue"] {{
            color: var(--text) !important;
        }}

        div[data-testid="stDataFrame"] thead th {{
            background-color: var(--accent) !important;
            color: var(--text) !important;
            text-align: center !important;
            font-weight: 600 !important;
            border: none !important;
        }}

        div[data-testid="stDataFrame"] tbody td {{
            text-align: center !important;
            border: none !important;
        }}

        div[data-testid="stDataFrame"] {{
            border: none !important;
            box-shadow: none !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def aplicar_paleta_global():
    """Compatibilidad con código legado."""
    aplicar_estilos_globales()


def aplicar_estilos_tabla():
    """Compatibilidad con código legado para estilos de tabla."""
    aplicar_estilos_globales()
