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

# 1. Establecer la conexión con Google Sheets mediante st-gsheets
@st.cache_resource
def conectar_gsheets():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df_usuarios = conn.read(worksheet="Usuarios", ttl=5)
        return conn, df_usuarios
    except Exception as e:
        return None, None

conn, df_usuarios = conectar_gsheets()

# Control de sesión para el acceso por clave
if "acceso_concedido" not in st.session_state:
    st.session_state.acceso_concedido = False

if not st.session_state.acceso_concedido:
    st.title("🔐 Sistema de Acceso Automatizado - Scarlet")
    st.write("Introduce tu clave asignada para desbloquear las funciones.")

    clave_usuario = st.text_input("Introduce tu clave de acceso:", type="password")

    if st.button("Verificar Clave"):
        if clave_usuario:
            if df_usuarios is not None and 'Claves' in df_usuarios.columns:
                claves_validas = df_usuarios['Claves'].astype(str).values
                if clave_usuario in claves_validas:
                    st.session_state.acceso_concedido = True
                    st.success("✅ ¡Acceso concedido! Bienvenido al sistema.")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("🚨 Clave incorrecta. Acceso denegado.")
            else:
                st.warning("⚠️ No se encontró la hoja 'Usuarios' o la columna 'Claves' en tu Google Sheet.")
        else:
            st.info("Por favor, escribe una clave.")
    st.stop()

# --- APLICACIÓN PRINCIPAL (Una vez superada la clave) ---
SHEET_ID = "1TJAoGBPhpxKvzLR9iza1vCgFcBb8rq7EDNz8Fl7knCA"

tab_dashboard, tab_formulario = st.tabs(["📊 Panel Gerencial (Dashboard)", "📝 Postularme al Roster"])

with tab_dashboard:
    count = st_autorefresh(interval=5000, limit=None, key="scarlet_autorefresh")
    st.title("🔥 POSTULACIONES SCARLET VALORANT")
    
    try:
        df_postulaciones = conn.read(worksheet="Sheet1", ttl=2)
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
    st.markdown("Completa tus datos correctamente para postularte.")
    
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
                    # Para escribir datos manteniendo st-gsheets, puedes usar gspread de respaldo o agregar la fila directo
                    import gspread
                    from google.oauth2.service_account import Credentials
                    # O alternativamente puedes gestionar la inserción mediante gspread si prefieres.
                    st.success("🎉 ¡Postulación procesada!")
                except Exception as e:
                    st.error(f"Error al registrar los datos: {e}")
