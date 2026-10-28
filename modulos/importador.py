# ---------------------------------------------------------
# SECCIÓN 4: IMPORTADOR MASIVO
# ---------------------------------------------------------
elif menu == "Importador":
    st.header("📁 Módulo de Importación Masiva")
    st.write("Sube tus archivos de Excel (`.xlsx`) para verificar los datos antes de guardarlos en Supabase.")
    
    tab_estaciones, tab_inventarios, tab_ventas = st.tabs(["📍 Estaciones", "📦 Inventarios", "💰 Ventas"])
    
    # Pestaña Estaciones
    with tab_estaciones:
        st.subheader("Importador de Estaciones")
        archivo_est = st.file_uploader("Subir Excel de Estaciones", type=["xlsx"], key="up_estaciones")
        if archivo_est is not None:
            try:
                df_limpio = importador.limpiar_y_normalizar_estaciones(pd.read_excel(archivo_est))
                st.metric("Total Registros Únicos", len(df_limpio))
                st.dataframe(df_limpio, use_container_width=True)
                
                if st.button("Confirmar y Guardar Estaciones", key="btn_estaciones"):
                    exito, res_exitos, res_errores, _ = importador.procesar_importacion_estaciones(archivo_est)
                    if exito:
                        st.success(f"¡Éxito! Registros guardados: {res_exitos}. Errores/Omitidos: {res_errores}")
                        st.rerun()
                    else:
                        st.error(f"Error al procesar: {res_exitos}")
            except Exception as e:
                st.error(f"Error en la estructura del Excel: {e}")

    # Pestaña Inventarios
    with tab_inventarios:
        st.subheader("Importador de Inventarios")
        archivo_inv = st.file_uploader("Subir Excel de Inventarios", type=["xlsx"], key="up_inventarios")
        if archivo_inv is not None:
            try:
                df_limpio = importador.limpiar_y_normalizar_inventarios(pd.read_excel(archivo_inv))
                st.metric("Total Registros", len(df_limpio))
                st.dataframe(df_limpio, use_container_width=True)
                
                if st.button("Confirmar y Guardar Inventarios", key="btn_inventarios"):
                    exito, res_exitos, res_errores, _ = importador.procesar_importacion_inventarios(archivo_inv)
                    if exito:
                        st.success(f"¡Éxito! Registros guardados: {res_exitos}. Errores/Omitidos: {res_errores}")
                        st.rerun()
                    else:
                        st.error(f"Error al procesar: {res_exitos}")
            except Exception as e:
                st.error(f"Error en la estructura del Excel: {e}")

    # Pestaña Ventas
    with tab_ventas:
        st.subheader("Importador de Ventas")
        archivo_ven = st.file_uploader("Subir Excel de Ventas", type=["xlsx"], key="up_ventas")
        if archivo_ven is not None:
            try:
                df_limpio = importador.limpiar_y_normalizar_ventas(pd.read_excel(archivo_ven))
                st.metric("Total Registros", len(df_limpio))
                st.dataframe(df_limpio, use_container_width=True)
                
                if st.button("Confirmar y Guardar Ventas", key="btn_ventas"):
                    exito, res_exitos, res_errores, _ = importador.procesar_importacion_ventas(archivo_ven)
                    if exito:
                        st.success(f"¡Éxito! Registros guardados: {res_exitos}. Errores/Omitidos: {res_errores}")
                        st.rerun()
                    else:
                        st.error(f"Error al procesar: {res_exitos}")
            except Exception as e:
                st.error(f"Error en la estructura del Excel: {e}")
