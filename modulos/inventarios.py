import streamlit as st
import pandas as pd
from datetime import date
import database as db
from servicios import formato, plantilla


def mostrar_inventarios():
    st.header("📋 Consulta y Actualización de Inventarios")

    # 1. Obtener información de la base de datos
    datos_estaciones_usuario = db.obtener_estaciones_usuario()
    datos_inventarios = db.obtener_inventarios()

    if not datos_estaciones_usuario:
        st.warning("No hay asignaciones de estaciones y usuarios registradas en la base de datos.")
        return

    df_est_usu = pd.DataFrame(datos_estaciones_usuario)

    # 2. Filtros principales: Fecha y Usuario
    col_fecha, col_usuario = st.columns(2)

    with col_fecha:
        fecha_seleccionada = st.date_input(
            "Selecciona la fecha:",
            value=date.today(),
            key="filtro_fecha_inventarios"
        )

    with col_usuario:
        usuarios_disponibles = sorted(list(df_est_usu["usuario"].unique()))
        usuario_seleccionado = st.selectbox(
            "Selecciona el usuario:",
            options=usuarios_disponibles,
            key="filtro_usuario_inventarios"
        )

    # 3. Filtrar estaciones según el usuario seleccionado
    df_estaciones_filtradas = df_est_usu[df_est_usu["usuario"] == usuario_seleccionado].copy()

    if df_estaciones_filtradas.empty:
        st.info("No hay estaciones registradas para el usuario seleccionado.")
        return

    # Normalizar campos de estaciones si vienen anidados desde la relación de Supabase
    if "estaciones" in df_estaciones_filtradas.columns:
        df_estaciones_filtradas["nombre"] = df_estaciones_filtradas["estaciones"].apply(
            lambda x: x.get("nombre") if isinstance(x, dict) else ""
        )
        df_estaciones_filtradas["plaza"] = df_estaciones_filtradas["estaciones"].apply(
            lambda x: x.get("plaza") if isinstance(x, dict) else ""
        )

    # 4. Procesar y filtrar datos de inventario si existen
    if datos_inventarios:
        df_inventarios = pd.DataFrame(datos_inventarios)
        df_inventarios["fecha"] = pd.to_datetime(df_inventarios["fecha"]).dt.date
        df_inv_filtrado = df_inventarios[df_inventarios["fecha"] == fecha_seleccionada]

        if not df_inv_filtrado.empty:
            df_pivot = df_inv_filtrado.pivot_table(
                index="id_estacion",
                columns="producto",
                values="volumen",
                aggfunc="sum",
                fill_value=0
            ).reset_index()

            df_resultado = pd.merge(
                df_estaciones_filtradas[["id_estacion", "nombre", "plaza"]],
                df_pivot,
                on="id_estacion",
                how="left"
            ).fillna(0)
        else:
            df_resultado = df_estaciones_filtradas[["id_estacion", "nombre", "plaza"]].copy()
            df_resultado["Regular"] = 0
            df_resultado["Premium"] = 0
            df_resultado["Diesel"] = 0
    else:
        df_resultado = df_estaciones_filtradas[["id_estacion", "nombre", "plaza"]].copy()
        df_resultado["Regular"] = 0
        df_resultado["Premium"] = 0
        df_resultado["Diesel"] = 0

    for col in ["Regular", "Premium", "Diesel"]:
        if col not in df_resultado.columns:
            df_resultado[col] = 0

    df_resultado = df_resultado[["id_estacion", "nombre", "plaza", "Regular", "Premium", "Diesel"]]

    df_resultado["Regular"] = df_resultado["Regular"].astype(int)
    df_resultado["Premium"] = df_resultado["Premium"].astype(int)
    df_resultado["Diesel"] = df_resultado["Diesel"].astype(int)

    formato.aplicar_estilos_tabla()
    plantilla.aplicar_estilos_tablas(max_rows=50)

    column_config = {
        "id_estacion": st.column_config.TextColumn("ID", width="small", disabled=True),
        "nombre": st.column_config.TextColumn("Estación", width="medium", disabled=True),
        "plaza": st.column_config.TextColumn("Plaza", width="medium", disabled=True),
        "Regular": st.column_config.NumberColumn("Regular", format="%d"),
        "Premium": st.column_config.NumberColumn("Premium", format="%d"),
        "Diesel": st.column_config.NumberColumn("Diesel", format="%d")
    }

    # Limitar a 50 filas máximo para mantener la vista completa sin scroll vertical
    altura_tabla = min((len(df_resultado) * 26) + 40, (50 * 26) + 40)

    # 5. Mostrar la tabla interactiva con st.data_editor
    df_editado = st.data_editor(
        df_resultado,
        use_container_width=True,
        hide_index=True,
        column_config=column_config,
        height=altura_tabla,
        key="editor_inventarios"
    )

    # 6. Botón para guardar o actualizar datos en la base de datos
    if st.button("💾 Guardar / Actualizar Inventarios", type="primary"):
        with st.spinner("Guardando cambios..."):
            try:
                productos = ["Regular", "Premium", "Diesel"]
                
                for _, row in df_editado.iterrows():
                    id_estacion = row["id_estacion"]
                    for producto in productos:
                        volumen = float(row[producto])
                        db.insertar_inventario(
                            id_estacion=id_estacion,
                            fecha=fecha_seleccionada,
                            producto=producto,
                            volumen=volumen
                        )
                
                st.success("¡Inventarios guardados y actualizados correctamente en la base de datos!")
                st.rerun()
            except Exception as e:
                st.error(f"Ocurrió un error al guardar los datos: {e}")
