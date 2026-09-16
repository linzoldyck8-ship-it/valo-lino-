import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# Configuración de la página web con tu imagen de ícono personalizada
st.set_page_config(
    page_title="Scarlet Valorant - Reclutamiento",
    page_icon="SCARLET.png",  # <--- Reemplaza "logo.png" por el nombre exacto de tu archivo de ícono
    layout="wide"
)

# --- ESTILOS CSS AVANZADOS: FONDO CON IMAGEN, FUENTE AGDASIMA Y NEÓN SCARLET ---
st.markdown("""
    <style>
    /* Importar tipografía Agdasima desde Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Agdasima:wght@400;700&display=swap');

    /* Aplicar Agdasima a toda la aplicación */
    html, body, [class*="css"] {
        font-family: 'Agdasima', sans-serif !important;
    }

    /* Fondo de la página web con tu imagen personalizada y capa oscura neón */
    .stApp {
        background-image: linear-gradient(rgba(11, 13, 18, 0.88), rgba(11, 13, 18, 0.92)), url("fondoweb.png"); /* <--- Reemplaza "fondo.jpg" por el nombre de tu imagen de fondo */
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: #f0f2f6;
    }
    
    /* Barra lateral separada por una línea visible de neón escarlata */
    [data-testid="stSidebar"] {
        background-color: #12161f;
        border-right: 2px solid #ff4655;
        box-shadow: 4px 0px 15px rgba(255, 70, 85, 0.2);
    }
    
    /* Métricas / Tarjetas superiores con borde neón sutil */
    [data-testid="stMetric"] {
        background-color: rgba(22, 27, 34, 0.85);
        border: 1px solid rgba(255, 70, 85, 0.4);
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(255, 70, 85, 0.15);
    }
    
    [data-testid="stMetricLabel"] {
        color: #8b949e;
        font-size: 1.2rem !important;
        font-weight: 600;
    }
    
    [data-testid="stMetricValue"] {
        color: #ff4655 !important;
        text-shadow: 0 0 8px rgba(255, 70, 85, 0.4);
        font-size: 2.2rem !important;
    }

    /* Títulos principales con efecto neón */
    h1, h2, h3 {
        font-family: 'Agdasima', sans-serif !important;
        letter-spacing: 1px;
    }
    
    h1 {
        color: #ffffff;
        text-shadow: 0 0 12px rgba(255, 70, 85, 0.6);
    }

    /* Botones con estilo escarlata neón */
    .stButton>button {
        background-color: #ff4655;
        color: white;
        border-radius: 6px;
        border: 1px solid #ff6b78;
        font-weight: bold;
        font-family: 'Agdasima', sans-serif;
        font-size: 1.1rem;
        box-shadow: 0 0 10px rgba(255, 70, 85, 0.4);
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #fa5c68;
        box-shadow: 0 0 18px rgba(255, 70, 85, 0.8);
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- AUTORREFRESCO CADA 5 SEGUNDOS ---
count = st_autorefresh(interval=5000, limit=None, key="scarlet_autorefresh")

# Título Principal
st.title("🔥 POSTULACIONES SCARLET VALORANT")
st.markdown("Panel de control ejecutivo y monitoreo en tiempo real del roster competitivo.")

# ID de tu Google Sheet
SHEET_ID = "1TJAoGBPhpxKvzLR9iza1vCgFcBb8rq7EDNz8Fl7knCA"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# Controles en la barra lateral
st.sidebar.markdown("## ⚙️ Panel de Control")
if st.sidebar.button("🔄 Sincronizar Datos"):
    st.cache_data.clear()
    st.success("¡Sincronizado correctamente!")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Filtros de Búsqueda")

@st.cache_data(ttl=2)
def load_data():
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Error al cargar Google Sheets: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("⚠️ No se pudieron cargar los datos. Verifica que el Google Sheet sea público.")
else:
    df.columns = [str(c).strip() for c in df.columns]

    # --- CÁLCULOS DE KPIS ---
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
    col1.metric("Postulantes Totales", total_postulantes)
    col2.metric("Pruebas Activas", tryouts_activos, delta="En proceso")
    col3.metric("Plantel Aceptado", aceptados)
    col4.metric("Alertas de Baneos", baneos_alerta, delta_color="inverse" if baneos_alerta > 0 else "normal")

    st.markdown("---")

    # --- 2. FILTROS EN LA BARRA LATERAL ---
    rol_opciones = ["Todos"]
    if 'Rol Principal' in df.columns:
        rol_opciones += list(df['Rol Principal'].dropna().unique())
    rol_filtro = st.sidebar.selectbox("Rol Principal", rol_opciones)
    
    estado_opciones = ["Todos"]
    if 'Estado' in df.columns:
        estado_opciones += list(df['Estado'].dropna().unique())
    estado_filtro = st.sidebar.selectbox("Estado del Proceso", estado_opciones)

    df_filtered = df.copy()
    if rol_filtro != "Todos" and 'Rol Principal' in df.columns:
        df_filtered = df_filtered[df_filtered['Rol Principal'] == rol_filtro]
    if estado_filtro != "Todos" and 'Estado' in df.columns:
        df_filtered = df_filtered[df_filtered['Estado'] == estado_filtro]

    # --- 3. GRÁFICOS ---
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.subheader("📊 Distribución por Estado")
        if 'Estado' in df.columns and not df['Estado'].dropna().empty:
            fig_estado = px.pie(df, names='Estado', hole=0.5, color_discrete_sequence=px.colors.sequential.Reds)
            fig_estado.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#f0f2f6')
            st.plotly_chart(fig_estado, use_container_width=True)
        else:
            st.info("Sin datos para graficar estado.")

    with col_g2:
        st.subheader("⚔️ Demanda por Rol")
        if 'Rol Principal' in df.columns and not df['Rol Principal'].dropna().empty:
            rol_counts = df['Rol Principal'].value_counts().reset_index()
            rol_counts.columns = ['Rol', 'Cantidad']
            fig_roles = px.bar(rol_counts, x='Rol', y='Cantidad', 
                               color='Rol', color_discrete_sequence=['#ff4655', '#e94560', '#ff6b6b', '#c70039', '#900c3f'])
            fig_roles.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#f0f2f6', showlegend=False)
            st.plotly_chart(fig_roles, use_container_width=True)
        else:
            st.info("Sin datos para graficar roles.")

    # --- 4. TABLA ---
    st.subheader("📋 Registro Detallado de Postulantes")
    possible_cols = ['Nº', 'Nombre Real', 'Riot ID (#TAG)', 'Rol Principal', 'Rango Actual', 'Peak Elo', 'Baneos / Toxicidad', 'Estado']
    cols_to_show = [c for c in possible_cols if c in df_filtered.columns]
    if not cols_to_show:
        cols_to_show = df_filtered.columns
    st.dataframe(df_filtered[cols_to_show], use_container_width=True)