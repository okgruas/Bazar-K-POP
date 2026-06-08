import streamlit as st
from datetime import datetime
import shelve  # Base de datos física para que no se borre al dormirse la app

# Configuración de la página
st.set_page_config(
    page_title="Bazar Digital K-Pop & Clóset",
    page_icon="✨",
    layout="wide"
)

# ⚠️ CONFIGURACIÓN DE ADMINISTRADOR ⚠️
TELEFONO_ADMIN_WHATSAPP = "528143029578"
CONTRASENA_ADMIN = "bazar123"  # Puedes cambiarla aquí cuando quieras sin perder datos

# --- PERSISTENCIA REAL EN DISCO ---
def cargar_datos_disco():
    with shelve.open("bazar_permanente_db") as db:
        return dict(db.get("bloques_db", {}))

def guardar_datos_disco(datos):
    with shelve.open("bazar_permanente_db") as db:
        db["bloques_db"] = datos

# Inicializar st.session_state leyendo directamente del disco permanente
if "bloques_db" not in st.session_state:
    st.session_state.bloques_db = cargar_datos_disco()

# ==========================================
# 🖼️ COLOQUE AQUÍ SUS LINKS REALES DE PORTADA
# ==========================================
# Tip: Sube tus imágenes a un servidor como Imgur o Postimages y pega el link directo aquí.
# Si dejas estos de Unsplash, se usará el fondo de muestra de forma sutil.
URL_PORTADA_FONDO = "https://images.unsplash.com/photo-1517841905240-472988babdf9?q=80&w=1000" 
URL_PORTADA_LATERAL = "https://images.unsplash.com/photo-1529139574466-a303027c1d8b?q=80&w=1000"

# --- ESTILOS CSS CON EFECTO TENUE CORREGIDO ---
st.markdown(f"""
    <style>
    /* Fondo general: Mantiene tu degradado rosa vibrante de base */
    .stApp {{
        background: linear-gradient(135deg, #FFE5EC 0%, #FFB3C6 40%, #FF477E 100%) !important;
        position: relative;
    }}
    
    /* Capa intermedia para la Portada 1 tenue y difuminada */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: url('{URL_PORTADA_FONDO}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        opacity: 0.08; /* Bajado a 8% para que sea ultra sutil y no tape nada */
        filter: blur(6px); /* Desenfoque elegante */
        z-index: -1;
    }}
    
    /* Contenedor de la Portada Lateral (Estilo Facebook) */
    .portada-lateral-container {{
        text-align: center;
        margin-bottom: 20px;
        border-radius: 12px;
        overflow: hidden;
        border: 3px solid #FF477E;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
    }}
    
    /* Forzar que las tarjetas y bloques SE VEAN BLANCOS SÓLIDOS y no transparentes */
    .stForm, .preview-container, .public-block, .admin-box, div[data-testid="stVerticalBlock"] > div {{
        background-color: #FFFFFF !important;
        padding: 25px;
        border-radius: 16px;
        box-shadow: 0px 6px 22px rgba(0, 0, 0, 0.12);
        margin-bottom: 25px;
    }}
    
    /* Tarjeta de productos estilo Shein */
    .shein-card {{
        background-color: #FFFFFF !important;
        border: 2px solid #FFB3C6 !important;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 20px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.06);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }}
    
    /* Asegurar visibilidad de textos en Monterrey */
    label, p, span, .stRadio p, h1, h2, h3, h4, div[data-testid="stMarkdownContainer"] p {{
        color: #1A1A1A !important;
        font-weight: bold !important;
    }}
    
    /* Campos de texto */
    textarea, input[type="text"], div[data-testid="stTextArea"] textarea, div[data-testid="stTextInput"] input {{
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        border: 2px solid #FF477E !important;
        caret-color: #1A1A1A !important;
    }}
    
    /* Botones de acción principales */
    div[data-testid="stFormSubmitButton"] button, .stSubmitButton button, div.stSubmitButton > button {{
        background-color: #E6005C !important;
        color: #FFFFFF !important;
        border: 2px solid #FFFFFF !important;
        border-radius: 10px !important;
        padding: 14px 28px !important;
        width: 100% !important;
        box-shadow: 0px 6px 15px rgba(230, 0, 92, 0.4) !important;
    }}
    
    /* Botón verde de WhatsApp / Validación */
    div.stButton > button, .btn-wa-nativo {{
        background-color: #25D366 !important;
        color: #1A1A1A !important;
        border: 2px solid #FFFFFF !important;
        border-radius: 12px !important;
        padding: 16px 32px !important;
        width: 100% !important;
        font-weight: 900 !important;
        font-size: 19px !important;
        box-shadow: 0px 6px 18px rgba(37, 211, 102, 0.4) !important;
    }}
    
    /* Caja interna de artículos */
    .articulos-box-shein {{
        background-color: #F8F9FA !important;
        color: #1A1A1A !important;
        padding: 12px;
        border-radius: 8px;
        border-left: 5px solid #E6005C;
        font-size: 14px;
        white-space: pre-wrap;
    }}

    .badge-activo-shein {{
        background-color: #D4EDDA; color: #155724; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: bold;
    }}
    
    .seccion-quejas {{
        text-align: center;
        font-size: 12px !important;
        color: #FFFFFF !important;
        margin-top: 30px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }}

    /* Estilos móviles */
    @media (max-width: 768px) {{
        div[data-testid="stHorizontalBlock"] {{
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: wrap !important;
            gap: 10px !important;
        }}
        div[data-testid="column"] {{
            flex: 1 1 45% !important;
            min-width: 45% !important;
        }}
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 💾 MENÚ LATERAL ESTILO FACEBOOK (IZQUIERDA)
# ==========================================
with st.sidebar:
    st.markdown(f"""
        <div class="portada-lateral-container">
            <img src="{URL_PORTADA_LATERAL}" style="width: 100%; height: auto; display: block;">
        </div>
    """, unsafe_allow_html=True)
    
    st.title("📌 Navegación")
    seccion_seleccionada = st.radio(
        "Ir a:",
        ["🛍️ Ver el Bazar / Clóset", "💜 Registrarse como Vendedora", "🔐 Panel Admin"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown('<div style="text-align: center; font-size: 12px; color: #FFFFFF;">Bazar v2.0 • Monterrey</div>', unsafe_allow_html=True)

# --- ENCABEZADO PRINCIPAL (COLUMNA DERECHA) ---
st.markdown('<div style="text-align:center; font-size:42px; font-weight:900; color:#FFFFFF; text-shadow:
