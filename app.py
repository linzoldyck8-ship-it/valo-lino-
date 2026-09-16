import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página web
st.set_page_config(
    page_title="Dashboard Valorant - Reclutamiento",
    page_icon="🎯",
    layout="wide"
)

# Título Principal
st.title("🎯 Dashboard de Reclutamiento - Lista de valorantes")
st.markdown("Panel de control ejecutivo para la visualización de postulantes, estados y análisis de riesgos en tiempo real.")

# ID de tu Google Sheet
SHEET_ID = "1TJAoGBPhpxKvzLR9iza1vCgFcBb8rq7EDNz8Fl7knCA"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos de Google Sheets: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("⚠️ No se pudieron cargar los datos. Asegúrate de que tu Google Sheet sea público.")
else:
    df.columns = [str(c).strip() for c in df.columns]

    # --- INICIALIZAR VARIABLES DE FORMA SEGURA ---
    total_postulantes = len(df.dropna(subset=['Nombre Real'])) if 'Nombre Real' in df.columns else len(df)
    
    tryouts_activos = 0
    if 'Estado' in df.columns:
        tryouts_activos = len(df[df['Estado'].astype(str).str.strip() == 'Tryout'])

    aceptados = 0
    if 'Estado' in df.columns:
        aceptados = len(df[df['Estado'].astype(str).str.strip() == 'Aceptado'])

    baneos_alerta = 0
    col_baneos = None
    for c in df.columns:
        if 'bano' in c.lower() or 'baneo' in c.lower() or 'toxicidad' in c.lower():
            col_baneos = c
            break

    if col_baneos:
        baneos_alerta = len(df[df[col_baneos].astype(str).str.strip().isin(['Chat Ban', 'Ranked Ban', 'Permanente/HWID'])])

    # --- 1. BLOQUE DE KPIS SUPERIORES ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Postulantes totales", total_postulantes)
    col2.metric("Pruebas Activos", tryouts_activos, delta="En proceso")
    col3.metric("Plantel Aceptado", aceptados)
    col4.metric("Alertas de Baneos", baneos_alerta, delta_color="inverse" if baneos_alerta > 0 else "normal")

    st.markdown("---")

    # --- 2. FILTROS LATERALES ---
    st.sidebar.header("Filtros de Búsqueda")
    
    rol_opciones = ["Todos"]
    if 'Rol Principal' in df.columns:
        rol_opciones += list(df['Rol Principal'].dropna().unique())
    rol_filtro = st.sidebar.selectbox("Filtrar por Rol Principal", rol_opciones)
    
    estado_opciones = ["Todos"]
    if 'Estado' in df.columns:
        estado_opciones += list(df['Estado'].dropna().unique())
    estado_filtro = st.sidebar.selectbox("Filtrar por Estado", estado_opciones)

    df_filtered = df.copy()
    if rol_filtro != "Todos" and 'Rol Principal' in df.columns:
        df_filtered = df_filtered[df_filtered['Rol Principal'] == rol_filtro]
    if estado_filtro != "Todos" and 'Estado' in df.columns:
        df_filtered = df_filtered[df_filtered['Estado'] == estado_filtro]

    # --- 3. GRÁFICOS ---
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.subheader("📊 Distribución por Estado del Proceso")
        if 'Estado' in df.columns and not df['Estado'].dropna().empty:
            fig_estado = px.pie(df, names='Estado', hole=0.4, color_discrete_sequence=px.colors.sequential.Reds)
            st.plotly_chart(fig_estado, use_container_width=True)
        else:
            st.info("No hay datos suficientes de Estado para graficar.")

    with col_g2:
        st.subheader("⚔️ Demanda por Rol Principal")
        if 'Rol Principal' in df.columns and not df['Rol Principal'].dropna().empty:
            rol_counts = df['Rol Principal'].value_counts().reset_index()
            rol_counts.columns = ['Rol', 'Cantidad']
            fig_roles = px.bar(rol_counts, x='Rol', y='Cantidad', 
                               color='Rol', color_discrete_sequence=px.colors.sequential.Darkmint)
            st.plotly_chart(fig_roles, use_container_width=True)
        else:
            st.info("No hay datos suficientes de Roles para graficar.")

    # --- 4. TABLA ---
    st.subheader("📋 Detalle de Postulantes Filtrados")
    possible_cols = ['Nº', 'Nombre Real', 'Riot ID (#TAG)', 'Rol Principal', 'Rango Actual', 'Peak Elo', 'Baneos / Toxicidad', 'Estado']
    cols_to_show = [c for c in possible_cols if c in df_filtered.columns]
    if not cols_to_show:
        cols_to_show = df_filtered.columns
    st.dataframe(df_filtered[cols_to_show], use_container_width=True)
