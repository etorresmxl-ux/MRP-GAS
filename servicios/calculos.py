import pandas as pd
import streamlit as st
import database as db

# Usamos st.cache_data para que los cálculos se realicen una sola vez al cargar o refrescar 
# y no consuman recursos innecesarios al cambiar de módulo.
@st.cache_data
def obtener_calculos_combustible():
    """
    Servicio centralizado que obtiene la venta semanal de las últimas 12 semanas,
    calcula la VSP ponderada y la VDP ponderada por estación y producto.
    """
    # 1. Obtener datos de la vista de Supabase creada previamente
    data = db.obtener_venta_semanal_promedio_12w()
    df = pd.DataFrame(data)
    
    if df.empty:
        return pd.DataFrame()
    
    # 2. Ordenar de la semana más reciente a la más antigua por estación y producto
    df = df.sort_values(by=['id_estacion', 'producto', 'semana'], ascending=[True, True, False])
    
    # 3. Asignar un ranking de recencia (1 = la más reciente, 12 = la más antigua)
    df['ranking_semana'] = df.groupby(['id_estacion', 'producto']).cumcount() + 1
    
    # 4. Asignar pesos según los bloques requeridos:
    # - Semanas 1 y 2: 50% de peso total (0.25 c/u)
    # - Semanas 3 a 8: 30% de peso total (0.05 c/u)
    # - Semanas 9 a 12: 20% de peso total (0.05 c/u)
    def asignar_peso(row):
        r = row['ranking_semana']
        if r in [1, 2]:
            return 0.50 / 2
        elif 3 <= r <= 8:
            return 0.30 / 6
        elif 9 <= r <= 12:
            return 0.20 / 4
        return 0.0

    df['peso'] = df.apply(asignar_peso, axis=1)
    
    # 5. Calcular la Venta Semanal Ponderada (vsp_ponderada)
    df['volumen_ponderado'] = df['volumen'] * df['peso']
    
    df_resultado = df.groupby(['id_estacion', 'producto']).agg(
        vsp_ponderada=('volumen_ponderado', 'sum')
    ).reset_index()
    
    # 6. Calcular la Venta Diaria Ponderada (vdp_ponderada) dividiendo entre 7
    df_resultado['vdp_ponderada'] = df_resultado['vsp_ponderada'] / 7.0
    
    return df_resultado


@st.cache_data
def obtener_vdp_diario_12w():
    """
    Obtiene el promedio por día de la semana (Lunes, Martes, etc.) 
    de las últimas 12 semanas directamente desde la vista de Supabase.
    """
    data = db.obtener_venta_promedio_dia_semana_12w()
    return pd.DataFrame(data)
