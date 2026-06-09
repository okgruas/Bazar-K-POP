import streamlit as st
from datetime import datetime
import shelve  # Base de datos física para que no se borre al dormirse la app
import base64
import os

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Bazar Nocturnal Goth",
    page_icon="🌙",
    layout="wide"
)

# ⚠️ CONFIGURACIÓN DE ADMINISTRADOR ⚠️
TELEFONO_ADMIN_WHATSAPP = "528143029578"
CONTRASENA_ADMIN = "bazar123"  

# --- 2. PERSISTENCIA REAL EN DISCO ---
def cargar_datos_disco():
    with shelve.open("bazar_permanente_db") as db:
        return dict(db.get("bloques_db", {}))

def guardar_datos_disco(datos):
    with shelve.open("bazar_permanente_db") as db:
        db["bloques_db"] = datos

if "bloques_db" not in st.session_state:
    st.session_state.bloques_db = cargar_datos_disco()

# --- 3. FUNCIÓN PARA CARGAR IMÁGENES LOCALES ---
def obtener_base64_de_imagen(nombre_archivo):
    try:
        if os.path.exists(nombre_archivo):
            with open(nombre_archivo, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
                extension = "png" if nombre_archivo.lower().endswith(".png") else "jpeg"
                return f"data:image/{extension};base64,{encoded_string}"
    except Exception:
        pass
    return ""

img_portada_base64 = obtener_base64_de_imagen("portada1.png")
img_perfil_base64 = obtener_base64_de_imagen("portada2.png")

# --- 4. ESTILOS CSS (Ajustados a estética Goth: Morado/Negro) ---
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at center, #2a0845 0%, #050505 70%) !important;
    }
    
    .fb-header-container {
        background: rgba(0, 0, 0, 0.6) !important;
        border: 2px solid #5d0f75 !important;
        border-radius: 24px;
        padding: 15px;
        box-shadow: 0 0 20px rgba(93, 15, 117, 0.5);
        margin-bottom: 30px;
    }
    
    /* Títulos y textos Goth */
    h1, h2, h3, p, label { color: #d1d1d1 !important; }
    
    .gradient-title {
        color: #b39ddb !important;
        font-weight: 900 !important;
    }
    
    .shein-card {
        background: rgba(10, 10, 10, 0.7) !important;
        border: 1px solid #5d0f75 !important;
        border-radius: 12px;
        padding: 15px;
        color: #d1d1d1 !important;
    }
    
    div.stButton > button {
        background-color: #5d0f75 !important;
        color: #fff !important;
        border: 1px solid #b39ddb !important;
    }
    
    .articulos-box-shein {
        background-color: #1a1a1a !important;
        color: #d1d1d1 !important;
        border-left: 4px solid #5d0f75 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 5. ENCABEZADO ---
st.markdown(f"""
    <div class="fb-header-container">
        <div class="fb-cover-wrapper">
            {f'<img src="{img_portada_base64}" style="width:100%; height:200px; object-fit:cover; border-radius:15px;"/>' if img_portada_base64 else ''}
        </div>
        <div style="display:flex; align-items:center; margin-top:-50px; padding-left:20px;">
            <div style="width:120px; height:120px; border-radius:50%; border:5px solid #000; overflow:hidden;">
                {f'<img src="{img_perfil_base64}" style="width:100%; height:100%; object-fit:cover;"/>' if img_perfil_base64 else '✨'}
            </div>
            <div style="margin-left:20px; margin-top:50px;">
                <h1 class="gradient-title">🌙 BAZAR NOCTURNAL GOTH</h1>
                <p>Tu estilo, nuestra esencia</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 6. PESTAÑAS (Catálogo, Registro, Admin) ---
tab_bazar, tab_anunciarse, tab_admin = st.tabs(["🛍️ Ver el Bazar", "💜 Registrarse", "🔐 Admin"])

# (Aquí sigue el resto de tu lógica original, que no he modificado para nada)
