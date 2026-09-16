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

@st.cache_data(ttl=60) # Actualiza datos cada 60 segundos
def load_data():
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos de Google Sheets: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("⚠️ No se pudieron cargar los datos. Asegúrate de que tu Google Sheet sea público (Cualquier usuario con el enlace puede ser Lector).")
else:
    # Limpieza básica de espacios en los nombres de columnas
    df.columns = [c.strip() for c in df.columns]

    # --- 1. BLOQUE DE KPIS SUPERIORES ---
    total_postulantes = len(df.dropna(subset=['Nombre Real'])) if 'Nombre Real' in df.columns else len(df)
    tryouts_activos = len(df[df['Estado'] == 'Tryout']) if 'Estado' in df.columns else 0
    aceptados = len(df[df['Estado'] == 'Aceptado']) if 'Estado' in df.columns else 0
    
    # Manejo seguro de la columna de baneos
    if 'Baneos / Toxicidad' in df.columns:
        baneados_alerta = len(df[df['Baneos / Toxicidad'].isin(['Chat Ban', 'Ranked Ban', 'Permanente/HWID'])])
    else:
        baneados_alerta = 0

    # Definimos exactamente 4 columnas para evitar el error de NameError
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Postulantes totales", total_postulantes)
    col2.metric("Pruebas Activos", tryouts_activos, delta="En proceso")
    col3.metric("Plantel Aceptado", aceptados)
    col4.metric("Alertas de Baneos", baneos_alerta, delta_color="inverse" if baneos_alerta > 0 else "normal")

    st.markdown("---")

    # --- 2. FILTROS LATERALES PARA JEFES ---
    st.sidebar.header("Filtros de Búsqueda")
    
    rol_opciones = ["Todos"] + list(df['Rol Principal'].dropna().unique()) if 'Rol Principal' in df.columns else ["Todos"]
    rol_filtro = st.sidebar.selectbox("Filtrar por Rol Principal", rol_opciones)
    
    estado_opciones = ["Todos"] + list(df['Estado'].dropna().unique()) if 'Estado' in df.columns else ["Todos"]
    estado_filtro = st.sidebar.selectbox("Filtrar por Estado", estado_opciones)

    df_filtered = df.copy()
    if rol_filtro != "Todos":
        df_filtered = df_filtered[df_filtered['Rol Principal'] == rol_filtro]
    if estado_filtro != "Todos":
        df_filtered = df_filtered[df_filtered['Estado'] == estado_filtro]

    # --- 3. GRÁFICOS INTERACTIVOS (Plotly) ---
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

    # --- 4. TABLA DE DETALLE INTERACTIVA ---
    st.subheader("📋 Detalle de Postulantes Filtrados")
    cols_to_show = [c for c in ['Nº', 'Nombre Real', 'Riot ID (#TAG)', 'Rol Principal', 'Rango Actual', 'Peak Elo', 'Baneos / Toxicidad', 'Estado'] if c in df_filtered.columns]
    st.dataframe(df_filtered[cols_to_show], use_container_width=True)
