import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
import gspread
from google.oauth2.service_account import Credentials

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

SHEET_ID = "1TJAoGBPhpxKvzLR9iza1vCgFcBb8rq7EDNz8Fl7knCA"
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

@st.cache_resource
def conectar_gsheets():
    try:
        if "gcp_service_account" in st.secrets:
            secrets_dict = dict(st.secrets["gcp_service_account"])
        else:
            secrets_dict = dict(st.secrets[list(st.secrets.keys())[0]])

        # Corrección robusta para transformar los \n de texto en saltos de línea reales de criptografía
        if "private_key" in secrets_dict:
            pk = secrets_dict["private_key"]
            pk = pk.replace("\\n", "\n")
            secrets_dict["private_key"] = pk

        creds = Credentials.from_service_account_info(secrets_dict, scopes=scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID).sheet1
        return sheet
    except Exception as e:
        st.error(f"⚠️ Error de conexión con Google Sheets: {e}")
        return None

sheet_ws = conectar_gsheets()

tab_dashboard, tab_formulario = st.tabs(["📊 Panel Gerencial (Dashboard)", "📝 Postularme al Roster"])

with tab_dashboard:
    count = st_autorefresh(interval=5000, limit=None, key="scarlet_autorefresh")
    st.title("🔥 POSTULACIONES SCARLET VALORANT")
    
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

    @st.cache_data(ttl=2)
    def load_data():
        try:
            return pd.read_csv(url)
        except Exception:
            return pd.DataFrame()

    df = load_data()
    if df.empty:
        st.warning("⚠️ No se pudieron cargar los datos o la hoja está vacía.")
    else:
        df.columns = [str(c).strip() for c in df.columns]
        total_postulantes = len(df.dropna(subset=['Nombre Real'])) if 'Nombre Real' in df.columns else len(df)
        st.metric("Postulantes Totales", total_postulantes)
        st.dataframe(df, use_container_width=True)

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
                current_sheet = sheet_ws
                if not current_sheet:
                    current_sheet = conectar_gsheets()
                
                if not current_sheet:
                    st.error("⚠️ Error crítico: No se pudo conectar con Google Sheets.")
                else:
                    try:
                        data_rows = current_sheet.get_all_values()
                        nuevo_id = len(data_rows)
                        nueva_fila = [str(nuevo_id), nombre_real, riot_id, rol_principal, rol_secundario, rango_actual, peak_elo, baneos, horario, "Nuevo", notas]
                        
                        current_sheet.append_row(nueva_fila)
                        st.success("🎉 ¡Postulación enviada y guardada en Google Sheets con éxito!")
                    except Exception as e:
                        st.error(f"Error al registrar los datos: {e}")
