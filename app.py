import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
from streamlit_gsheets import GSheetsConnection

st.set_page_config(
    page_title="Scarlet Valorant - Reclutamiento",
    page_icon="🔥",
    layout="wide"
)

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Agdasima:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Agdasima', sans-serif !important; }
    .stApp {
        background-color: #0b0d12;
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(255, 70, 85, 0.08) 0%, transparent 40%),
            radial-gradient(circle at 90% 80%, rgba(255, 70, 85, 0.06) 0%, transparent 40%);
        color: #f0f2f6;
    }
    [data-testid="stSidebar"] { background-color: #12161f; border-right: 2px solid #ff4655; }
    [data-testid="stMetric"] { background-color: #161b22; border: 1px solid rgba(255, 70, 85, 0.3); padding: 15px; border-radius: 8px; }
    [data-testid="stMetricValue"] { color: #ff4655 !important; font-size: 2.2rem !important; }
    .stButton>button {
        background-color: #ff4655; color: white; border-radius: 6px; font-weight: bold; font-size: 1.1rem;
    }
    .stButton>button:hover { background-color: #fa5c68; color: white; }
    </style>
""", unsafe_allow_html=True)

# Establecer la conexión usando st-gsheets
@st.cache_resource
def conectar_gsheets():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        return conn
    except Exception as e:
        st.error(f"Error conectando a Google Sheets: {e}")
        return None

conn = conectar_gsheets()

tab_dashboard, tab_formulario = st.tabs(["📊 Panel Gerencial (Dashboard)", "📝 Postularme al Roster"])

with tab_dashboard:
    count = st_autorefresh(interval=5000, limit=None, key="scarlet_autorefresh")
    st.title("🔥 POSTULACIONES SCARLET VALORANT")
    
    try:
        df_postulaciones = conn.read(worksheet="Hoja 1", ttl=2)
    except Exception:
        df_postulaciones = pd.DataFrame()

    if df_postulaciones.empty:
        st.warning("⚠️ No se pudieron cargar los datos o la hoja está vacía.")
    else:
        df_postulaciones.columns = [str(c).strip() for c in df_postulaciones.columns]
        total_postulantes = len(df_postulaciones.dropna(subset=['Nombre Real'])) if 'Nombre Real' in df_postulaciones.columns else len(df_postulaciones)
        st.metric("Postulantes Totales", total_postulantes)
        st.dataframe(df_postulaciones, use_container_width=True)

with tab_formulario:
    st.title("📝 Formulario de Postulación - Scarlet Valorant")
    st.markdown("Completa tus datos correctamente para postularte. Tu información se registrará en Google Sheets de forma automática.")
    
    with st.form("form_postulacion", clear_on_submit=True):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            nombre_real = st.text_input("Nombre Real")
            riot_id = st.text_input("Riot ID (Ej: Scarlet#NA1)")
            rol_principal = st.selectbox("Rol Principal", ["Duelista", "Iniciador", "Controlador", "Centinela", "Flex"])
            rol_secundario = st.selectbox("Rol Secundario", ["Duelista", "Iniciador", "Controlador", "Centinela", "Flex"])
            rango_actual = st.selectbox("Rango Actual", ["Hierro-Plata", "Oro", "Platino", "Diamante", "Ascendente", "Inmortal 1", "Inmortal 2", "Inmortal 3", "Radiante"])
        with col_f2:
            peak_elo = st.selectbox("Peak Elo (Máximo Rango Histórico)", ["Hierro-Plata", "Oro", "Platino", "Diamante", "Ascendente", "Inmortal 1", "Inmortal 2", "Inmortal 3", "Radiante"])
            baneos = st.selectbox("Historial de Baneos / Toxicidad", ["Limpio", "Advertencia", "Chat Ban", "Ranked Ban", "Permanente/HWID"])
            horario = st.selectbox("Horario Disponible", ["Mañana", "Tarde", "Noche", "Madrugada", "Flexible"])
            notas = st.text_input("Link de Tracker.gg o VLR.gg / Notes")

        submitted = st.form_submit_button("🚀 Enviar Postulación")

        if submitted:
            if not nombre_real or not riot_id:
                st.error("⚠️ Completa al menos tu Nombre Real y tu Riot ID.")
            else:
                try:
                    # Cargamos datos actuales para calcular la siguiente fila
                    df_actual = conn.read(worksheet="Hoja 1", ttl=0)
                    nuevo_id = len(df_actual.dropna(subset=['Nº'])) + 1
                    
                    nueva_fila = pd.DataFrame([{
                        "Nº": nuevo_id,
                        "Nombre Real": nombre_real,
                        "Riot ID (#TAG)": riot_id,
                        "Rol Principal": rol_principal,
                        "Rol Secundario": rol_secundario,
                        "Rango Actual": rango_actual,
                        "Peak Elo": peak_elo,
                        "Baneos / Toxicidad": baneos,
                        "Horario": horario,
                        "Estado": "Nuevo",
                        "Notas / Tracker": notas
                    }])
                    
                    df_actual = pd.concat([df_actual, nueva_fila], ignore_index=True)
                    conn.update(worksheet="Hoja 1", data=df_actual)
                    st.success("🎉 ¡Postulación enviada y guardada en Google Sheets con éxito!")
                except Exception as e:
                    st.error(f"Error al registrar los datos: {e}")
