import streamlit as str
import pandas as pd
import database as db

def mostrar_estaciones():
    """Muestra la interfaz para registrar y visualizar las estaciones registradas."""
    st.header("📍 Gestión de Estaciones")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Registrar Nueva Estación")
        with st.form("form_estaciones", clear_on_submit=True):
            id_estacion = st.text_input("ID Estación (único)*", placeholder="ej. EST-001")
            nombre = st.text_input("Nombre de la Estación*")
            plaza = st.text_input("Plaza")
            tad = st.text_input("TAD")
            
            submitted = st.form_submit_button("Guardar Estación")
            if submitted:
                if id_estacion and nombre:
                    try:
                        db.insertar_estacion(id_estacion, nombre, plaza, tad)
                        st.success(f"Estación '{nombre}' registrada con éxito.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al guardar: {e}")
                else:
                    st.warning("El ID y el Nombre son obligatorios.")

    with col2:
        st.subheader("Estaciones Registradas")
        estaciones_data = db.obtener_estaciones()
        if estaciones_data:
            df_estaciones = pd.DataFrame(estaciones_data)
            st.dataframe(df_estaciones, use_container_width=True)
        else:
            st.info("No hay estaciones registradas aún.")
