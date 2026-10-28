import streamlit as st
import pandas as pd
from datetime import date, timedelta
import database as db
from servicios import calculos

def formatear_fecha_corta(fecha):
    """
    Devuelve la fecha en el formato pedido: 'ddd, - dd-mmm' (p. ej. 'lun, - 28-oct').
    """
    dias_semana = {0: "lun", 1: "mar", 2: "mié", 3: "jue", 4: "vie", 5: "sáb", 6: "dom"}
    meses = {
        1: "ene", 2: "feb", 3: "mar", 4: "abr", 5: "may", 6: "jun",
        7: "jul", 8: "ago", 9: "sep", 10: "oct", 11: "nov", 12: "dic"
    }
    dia_str = dias_semana[fecha.weekday()]
    mes_str = meses[fecha.month]
    return f"{dia_str}, - {fecha.day:02d}-{mes_str}"


def mostrar_proyecciones():
    st.header("📈 Proyección e Integridad de Inventarios (14 Días)")

    # 1. Obtener datos de estaciones
    datos_estaciones = db.obtener_estaciones()
    if not datos_estaciones:
        st.warning("No hay estaciones registradas en la base de datos.")
        return

    df_estaciones = pd.DataFrame(datos_estaciones)

    # 2. Filtros de Plaza y Estación
    col_plaza, col_estacion = st.columns(2)

    with col_plaza:
        plazas_disponibles = sorted(list(df_estaciones["plaza"].unique()))
        plaza_seleccionada = st.selectbox(
            "Selecciona la Plaza:",
            options=plazas_disponibles,
            key="filtro_plaza_proyecciones"
        )

    # Filtrar estaciones por la plaza seleccionada
    df_estaciones_plaza = df_estaciones[df_estaciones["plaza"] == plaza_seleccionada]
    
    with col_estacion:
        estaciones_dict = dict(zip(df_estaciones_plaza["id_estacion"], df_estaciones_plaza["nombre"]))
        id_estacion_sel = st.selectbox(
            "Selecciona la Estación:",
            options=list(estaciones_dict.keys()),
            format_func=lambda x: f"{x} - {estaciones_dict[x]}",
            key="filtro_estacion_proyecciones"
        )

    if not id_estacion_sel:
        st.info("Por favor selecciona una estación.")
        return

    # 3. Obtener Inventario Inicial del día de hoy desde la BD
    fecha_hoy = date.today()
    datos_inventarios = db.obtener_inventarios()
    df_inv_hoy = pd.DataFrame()
    
    if datos_inventarios:
        df_inv = pd.DataFrame(datos_inventarios)
        if "fecha" in df_inv.columns:
            df_inv["fecha"] = pd.to_datetime(df_inv["fecha"]).dt.date
            df_inv_hoy = df_inv[
                (df_inv["id_estacion"] == id_estacion_sel) & 
                (df_inv["fecha"] == fecha_hoy)
            ]

    # Obtener modelo/promedio de venta proyectada por día del servicio de cálculos
    try:
        df_vdp_diarios = calculos.obtener_vdp_diario_12w()
        if not df_vdp_diarios.empty and "fecha" in df_vdp_diarios.columns:
            df_vdp_diarios["fecha_dt"] = pd.to_datetime(df_vdp_diarios["fecha"]).dt.date
        else:
            df_vdp_diarios = pd.DataFrame()
    except Exception:
        df_vdp_diarios = pd.DataFrame()

    productos = ["Regular", "Premium", "Diesel"]

    # Estilos CSS para centrar títulos de encabezado en st.dataframe
    st.markdown("""
        <style>
        [data-testid="stHeaderCell"] {
            text-align: center !important;
        }
        [data-testid="stHeaderCell"] > div {
            justify-content: center !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # 4. Generar tabla de proyecciones por cada producto
    for producto in productos:
        st.subheader(f"⛽ Producto: {producto}")

        # Obtener inventario registrado hoy para el producto
        inv_inicial_hoy = 0
        if not df_inv_hoy.empty and "producto" in df_inv_hoy.columns:
            match_prod = df_inv_hoy[df_inv_hoy["producto"].str.capitalize() == producto]
            if not match_prod.empty:
                inv_inicial_hoy = int(match_prod["volumen"].values[0])

        filas = []
        inv_actual = inv_inicial_hoy

        # Iterar 14 días (Hoy + 13 días proyectados)
        for i in range(14):
            fecha_dia = fecha_hoy + timedelta(days=i)
            fecha_fmt = formatear_fecha_corta(fecha_dia)

            # Consultar Venta Estimada (VDP) para este producto y fecha de forma segura
            venta_est = 0
            if not df_vdp_diarios.empty and "fecha_dt" in df_vdp_diarios.columns:
                vdp_match = df_vdp_diarios[
                    (df_vdp_diarios["id_estacion"] == id_estacion_sel) &
                    (df_vdp_diarios["producto"].str.capitalize() == producto) &
                    (df_vdp_diarios["fecha_dt"] == fecha_dia)
                ]
                if not vdp_match.empty:
                    venta_est = int(vdp_match["volumen"].values[0])
            
            # CÁLCULOS PRINCIPALES
            inv_inicial = inv_actual
            inv_final = inv_inicial - venta_est
            
            # Cálculo D/S (Días de Inventario según el inventario y la venta del día)
            ds = int(inv_final / venta_est) if venta_est > 0 else 0

            filas.append({
                "Fecha": fecha_fmt,
                "Inventario Inicial": int(inv_inicial),
                "Venta Estimada": int(venta_est),
                "Inventario Final": int(inv_final),
                "D/S": int(ds)
            })

            # El inventario final del día actual se vuelve el inicial del día siguiente
            inv_actual = inv_final

        df_proyeccion = pd.DataFrame(filas)

        # Configuración y renderizado del DataFrame con Streamlit
        st.dataframe(
            df_proyeccion,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Fecha": st.column_config.TextColumn("Fecha", help="ddd, - dd-mmm"),
                "Inventario Inicial": st.column_config.NumberColumn(
                    "Inventario Inicial",
                    format="%d",
                    help="Inventario registrado o proyectado al inicio del día"
                ),
                "Venta Estimada": st.column_config.NumberColumn(
                    "Venta Estimada",
                    format="%d",
                    help="Venta proyectada según el día"
                ),
                "Inventario Final": st.column_config.NumberColumn(
                    "Inventario Final",
                    format="%d",
                    help="Inicial - Venta Estimada"
                ),
                "D/S": st.column_config.NumberColumn(
                    "D/S",
                    format="%d",
                    help="Días de inventario disponibles"
                ),
            }
        )
