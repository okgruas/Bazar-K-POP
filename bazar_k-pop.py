import streamlit as st
from datetime import datetime
import shelve
import base64
import os

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Bazar Nocturnal Goth", page_icon="🌙", layout="wide")

CONTRASENA_ADMIN = "bazar123"

# --- 2. PERSISTENCIA ---
def cargar_datos_disco():
    with shelve.open("bazar_goth_db") as db:
        return dict(db.get("bloques_db", {}))

def guardar_datos_disco(datos):
    with shelve.open("bazar_goth_db", writeback=True) as db:
        db["bloques_db"] = datos

if "bloques_db" not in st.session_state:
    st.session_state.bloques_db = cargar_datos_disco()

# --- 3. CARGA DE IMÁGENES (GitHub/Local) ---
def get_img_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return None

img_portada = get_img_b64("portada1.png")
img_perfil = get_img_b64("portada2.png")

# --- 4. CSS (Tu esencia) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at center, #2a0845 0%, #050505 70%) !important; color: #d1d1d1 !important; }
    .fb-header { position: relative; background: rgba(0,0,0,0.6); border-radius: 20px; padding: 0; overflow: hidden; margin-bottom: 30px; border: 2px solid #5d0f75; }
    .portada { width: 100%; height: 200px; object-fit: cover; }
    .perfil { width: 120px; height: 120px; border-radius: 50%; border: 5px solid #050505; margin: -60px 0 0 30px; }
    .header-text { padding: 10px 30px; color: #b39ddb; }
    .card { background: rgba(10, 10, 10, 0.8); border: 1px solid #4a0072; border-radius: 15px; padding: 15px; margin-bottom: 15px; }
    h1, h2, h3 { color: #b39ddb !important; }
    </style>
""", unsafe_allow_html=True)

# --- 5. ENCABEZADO ---
st.markdown(f"""
    <div class="fb-header">
        <img src="{img_portada}" class="portada">
        <img src="{img_perfil}" class="perfil">
        <div class="header-text">
            <h1>🌙 BAZAR NOCTURNAL GOTH</h1>
            <p>Tu estilo, nuestra esencia</p>
        </div>
    </div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🛍️ Catálogo", "💜 Registro", "🔐 Admin"])

# --- CATALOGO ---
with tab1:
    bloques = {k: v for k, v in st.session_state.bloques_db.items() if v['estado'] == "🟢 ACTIVO"}
    cols = st.columns(3)
    for i, (id_b, b) in enumerate(bloques.items()):
        with cols[i % 3]:
            st.markdown(f"""
                <div class="card">
                    <h3>{b['vendedor']}</h3>
                    <p>📍 {b['zona']}</p>
                    <p>🛍️ {b['articulos']}</p>
                </div>
            """, unsafe_allow_html=True)

# --- REGISTRO ---
with tab2:
    with st.form("registro", clear_on_submit=True):
        col1, col2 = st.columns(2)
        vendedor = col1.text_input("Nombre de la Tienda *")
        zona = col2.text_input("Zona de entrega *")
        wapp = col1.text_input("WhatsApp *")
        costo = col2.text_input("Costo del Bloque (Ej: $25) *")
        articulos = st.text_area("Artículos y Precios *")
        fotos = st.file_uploader("Fotos de artículos", accept_multiple_files=True)
        pago = st.file_uploader("Comprobante de pago *")
        
        if st.form_submit_button("Subir Bloque"):
            id_b = f"GOTH-{datetime.now().strftime('%M%S')}"
            st.session_state.bloques_db[id_b] = {
                "vendedor": vendedor, "zona": zona, "articulos": articulos, 
                "estado": "⏳ En espera"
            }
            guardar_datos_disco(st.session_state.bloques_db)
            st.success("¡Enviado, Capitana!")

# --- ADMIN ---
with tab3:
    if st.text_input("Clave", type="password") == CONTRASENA_ADMIN:
        for id_b, b in st.session_state.bloques_db.items():
            if st.button(f"Activar {b['vendedor']}", key=id_b):
                st.session_state.bloques_db[id_b]['estado'] = "🟢 ACTIVO"
                guardar_datos_disco(st.session_state.bloques_db)
                st.rerun()
