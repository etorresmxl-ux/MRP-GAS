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

    # Obtener la venta proyectada y factores de estacionalidad desde calculos.py
    try:
        df_factores = calculos.obtener_factores_estacionalidad_dia()
        if not df_factores.empty and "fecha" in df_factores.columns:
            df_factores["fecha_dt"] = pd.to_datetime(df_factores["fecha"]).dt.date
        else:
            df_factores = pd.DataFrame()
    except Exception:
        df_factores = pd.DataFrame()

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

    # 4. Generar tabla horizontal de proyecciones por cada producto
    for producto in productos:
        st.subheader(f"⛽ Producto: {producto}")

        # Obtener inventario registrado hoy para el producto
        inv_inicial_hoy = 0
        if not df_inv_hoy.empty and "producto" in df_inv_hoy.columns:
            match_prod = df_inv_hoy[df_inv_hoy["producto"].str.capitalize() == producto]
            if not match_prod.empty:
                inv_inicial_hoy = int(match_prod["volumen"].values[0])

        fechas_cols = []
        inv_iniciales = []
        ventas_est = []
        inv_finales = []
        dias_inventario = []

        inv_actual = inv_inicial_hoy

        # Iterar 14 días (Hoy + 13 días proyectados)
        for i in range(14):
            fecha_dia = fecha_hoy + timedelta(days=i)
            fecha_fmt = formatear_fecha_corta(fecha_dia)
            fechas_cols.append(fecha_fmt)

            # Consultar Venta Estimada (Venta Proyectada del Día) desde calculos.py de forma segura
            venta_est = 0
            if not df_factores.empty:
                # Intentamos buscar por fecha exacta si la vista la provee
                if "fecha_dt" in df_factores.columns:
                    match_venta = df_factores[
                        (df_factores["id_estacion"] == id_estacion_sel) &
                        (df_factores["producto"].str.capitalize() == producto) &
                        (df_factores["fecha_dt"] == fecha_dia)
                    ]
                    if not match_venta.empty and "venta_proyectada_dia" in match_venta.columns:
                        venta_est = int(match_venta["venta_proyectada_dia"].values[0])
                
                # Si no hay coincidencia exacta por fecha pero sí por día de la semana o VDP ponderada general
                if venta_est == 0 and "vdp_ponderada" in df_factores.columns:
                    match_vdp = df_factores[
                        (df_factores["id_estacion"] == id_estacion_sel) &
                        (df_factores["producto"].str.capitalize() == producto)
                    ]
                    if not match_vdp.empty:
                        # Si cuenta con venta_proyectada_dia general, la tomamos como estimación base
                        if "venta_proyectada_dia" in match_vdp.columns:
                            venta_est = int(match_vdp["venta_proyectada_dia"].values[0])
                        elif "vdp_ponderada" in match_vdp.columns:
                            venta_est = int(match_vdp["vdp_ponderada"].values[0])

            # CÁLCULOS PRINCIPALES
            inv_inicial = inv_actual
            inv_final = inv_inicial - venta_est
            
            # Cálculo D/S (Días de Inventario según el inventario final y la venta estimada)
            ds = int(inv_final / venta_est) if venta_est > 0 else 0

            inv_iniciales.append(int(inv_inicial))
            ventas_est.append(int(venta_est))
            inv_finales.append(int(inv_final))
            dias_inventario.append(int(ds))

            # El inventario final del día actual se vuelve el inicial del día siguiente
            inv_actual = inv_final

        # Construir estructura horizontal (Concepto en vertical, fechas en columnas)
        data_dict = {
            "Concepto": ["Inventario Inicial", "Venta Estimada", "Inventario Final", "D/S"]
        }
        for idx, fecha_fmt in enumerate(fechas_cols):
            data_dict[fecha_fmt] = [
                inv_iniciales[idx],
                ventas_est[idx],
                inv_finales[idx],
                dias_inventario[idx]
            ]

        df_proyeccion = pd.DataFrame(data_dict)

        # Configuración de columnas dinámicas
        column_config = {
            "Concepto": st.column_config.TextColumn("Concepto", width="medium")
        }
        for fecha_fmt in fechas_cols:
            column_config[fecha_fmt] = st.column_config.NumberColumn(
                fecha_fmt,
                format="%d"
            )

        # Renderizado del DataFrame con Streamlit en formato horizontal
        st.dataframe(
            df_proyeccion,
            use_container_width=True,
            hide_index=True,
            column_config=column_config
        )
