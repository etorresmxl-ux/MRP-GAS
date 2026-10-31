import streamlit as st
from streamlit_option_menu import option_menu

# Configuración de página
st.set_page_config(
    page_title="Gestión de Combustibles",
    page_icon="⛽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# ESTILOS CSS PERSONALIZADOS (Estilo Modern Dark Glass/Floating)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Estilo del contenedor principal de la barra lateral */
    [data-testid="stSidebar"] {
        background-color: transparent !important;
        padding: 10px;
    }
    
    [data-testid="stSidebarContent"] {
        background: #1e1f25;
        border-radius: 24px;
        margin: 10px;
        padding: 20px 14px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Avatar y Sección de Perfil del Usuario */
    .profile-card {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 24px;
        padding: 6px 8px;
    }
    .profile-img {
        width: 42px;
        height: 42px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #323543;
    }
    .profile-info {
        display: flex;
        flex-direction: column;
    }
    .profile-greeting {
        font-size: 11px;
        color: #8c8f9a;
        margin: 0;
    }
    .profile-name {
        font-size: 15px;
        font-weight: 600;
        color: #ffffff;
        margin: 0;
    }

    /* Títulos de sección (Menu: 6, Service: 3, etc.) */
    .menu-header {
        font-size: 11px;
        font-weight: 600;
        color: #6b6e7b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 16px 0 8px 12px;
    }

    /* Estilo del botón flotante inferior de Acción (Create new task) */
    .floating-btn-container {
        background: linear-gradient(135deg, #2a2d3a 0%, #1a1b22 100%);
        border-radius: 18px;
        padding: 18px;
        text-align: center;
        margin-top: 25px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .action-circle-btn {
        background: #3b82f6;
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 10px auto;
        font-size: 20px;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    .action-title {
        color: #ffffff;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .action-subtitle {
        color: #717585;
        font-size: 11px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# CONTENIDO DE LA BARRA LATERAL (SIDEBAR)
# ---------------------------------------------------------
with st.sidebar:
    # 1. Cabecera del Usuario / Perfil
    st.markdown("""
        <div class="profile-card">
            <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80" class="profile-img"/>
            <div class="profile-info">
                <span class="profile-greeting">Good Day 👋</span>
                <span class="profile-name">Vitaliy D.</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 2. Título de Sección
    st.markdown('<div class="menu-header">Menu: 4</div>', unsafe_allow_html=True)
    
    # 3. Menú Principal utilizando streamlit_option_menu
    menu = option_menu(
        menu_title=None,
        options=["Dashboard", "Proyecciones", "Inventarios", "Importador"],
        icons=["grid-1x2-fill", "kanban", "calendar-event", "cloud-upload"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#8c8f9a", "font-size": "15px"},
            "nav-link": {
                "font-size": "13px",
                "text-align": "left",
                "margin": "4px 0px",
                "color": "#a0a5b5",
                "border-radius": "12px",
                "padding": "10px 14px",
                "font-weight": "500",
            },
            "nav-link-selected": {
                "background-color": "#2c2d38",
                "color": "#ffffff",
                "font-weight": "600",
            },
        }
    )

    # 4. Tarjeta Flotante Inferior de Acción Rápida
    st.markdown("""
        <div class="floating-btn-container">
            <div class="action-circle-btn">+</div>
            <div class="action-title">Create new task</div>
            <div class="action-subtitle">Or use invite link</div>
        </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# LÓGICA DE NAVEGACIÓN Y CONTENIDO
# ---------------------------------------------------------
if menu == "Dashboard":
    st.title("📊 Dashboard")
    st.write("Bienvenido al panel principal.")
elif menu == "Proyecciones":
    st.title("📈 Proyecciones")
    st.write("Vista de proyecciones y estimaciones.")
elif menu == "Inventarios":
    st.title("📦 Inventarios")
    st.write("Gestión de inventario de combustibles.")
elif menu == "Importador":
    st.title("📥 Importador")
    st.write("Módulo de carga e importación de datos.")
