import streamlit as st
from datetime import datetime
import shelve  # Base de datos física para que no se borre al dormirse la app
import base64
import os

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Bazar Digital K-Pop & Clóset",
    page_icon="✨",
    layout="wide"
)

# ⚠️ CONFIGURACIÓN DE ADMINISTRADOR ⚠️
TELEFONO_ADMIN_WHATSAPP = "528143029578"
CONTRASENA_ADMIN = "bazar123"  # Puedes cambiarla aquí cuando quieras sin perder datos

# --- 2. PERSISTENCIA REAL EN DISCO ---
def cargar_datos_disco():
    with shelve.open("bazar_permanente_db") as db:
        return dict(db.get("bloques_db", {}))

def guardar_datos_disco(datos):
    with shelve.open("bazar_permanente_db") as db:
        db["bloques_db"] = datos

# Inicializar st.session_state leyendo directamente del disco permanente
if "bloques_db" not in st.session_state:
    st.session_state.bloques_db = cargar_datos_disco()

# --- 3. FUNCIÓN ULTRA-SEGURA PARA CARGAR IMÁGENES LOCALES (EVITA PANTALLA NEGRA) ---
def obtener_base64_de_imagen(nombre_archivo):
    try:
        rutas_a_probar = [
            nombre_archivo,
            os.path.join("static", nombre_archivo),
            os.path.join("app", "static", nombre_archivo),
            nombre_archivo.replace(".png", ".jpg"),
            nombre_archivo.replace(".png", ".jpeg"),
            nombre_archivo.upper(),
        ]
        
        for ruta in rutas_a_probar:
            if os.path.exists(ruta):
                with open(ruta, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode()
                    extension = "png" if ruta.lower().endswith(".png") else "jpeg"
                    return f"data:image/{extension};base64,{encoded_string}"
    except Exception:
        pass
    return ""

# Cargar imágenes locales de forma segura
img_portada_base64 = obtener_base64_de_imagen("portada1.png")
img_perfil_base64 = obtener_base64_de_imagen("portada2.png")

# --- 4. ESTILOS CSS CON EFECTO GLASSMORPHISM ROSA/MORADO DEGRADADO ---
st.markdown("""
    <style>
    /* Fondo general de la App */
    .stApp {
        background: linear-gradient(135deg, #FFE5EC 0%, #FFB3C6 40%, #FF477E 100%) !important;
    }
    
    /* ========================================================
       ✨ CONTENEDOR DE PERFIL ESTILO FACEBOOK (GLASSMORPHISM MEJORADO)
       ======================================================== */
    .fb-header-container {
        position: relative;
        width: 100%;
        /* Degradado Glassmorphic translúcido de Rosa a Morado con opacidad del 35% */
        background: linear-gradient(135deg, rgba(255, 179, 198, 0.35), rgba(187, 134, 252, 0.35)) !important;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 24px;
        padding: 15px;
        box-shadow: 0 10px 32px 0 rgba(0, 0, 0, 0.12);
        margin-bottom: 30px;
        overflow: hidden;
    }
    
    /* Foto de portada con esquinas redondeadas */
    .fb-cover-wrapper {
        width: 100%;
        height: 280px;
        border-radius: 18px;
        overflow: hidden;
        position: relative;
    }
    .fb-cover-wrapper img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    /* Zona inferior del encabezado: Perfil y Títulos abajo de la foto */
    .fb-profile-row {
        display: flex;
        align-items: center;
        margin-top: -45px; /* Sube lo justo para la foto de perfil */
        padding: 0 40px 15px 40px;
        position: relative;
        z-index: 5;
    }
    
    /* Foto de Perfil Redonda con borde grueso blanco */
    .fb-profile-avatar {
        width: 140px;
        height: 140px;
        border-radius: 50%;
        border: 5px solid #FFFFFF;
        box-shadow: 0px 6px 16px rgba(0,0,0,0.15);
        overflow: hidden;
        flex-shrink: 0;
        background-color: #FFFFFF;
    }
    .fb-profile-avatar img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    /* Textos alineados abajo para que NUNCA tapen la portada en Computadora */
    .fb-profile-info {
        margin-left: 25px;
        margin-top: 50px; /* Empuja los textos hacia abajo fuera de la foto de portada */
    }
    
    /* ✨ TÍTULO CON DEGRADADO ROSA Y MORADO ✨ */
    .gradient-title {
        font-size: 34px !important;
        font-weight: 900 !important;
        background: linear-gradient(45deg, #FF1493, #9400D3) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        display: inline-block !important;
        margin: 0 !important;
        filter: drop-shadow(1px 1px 1px rgba(255, 255, 255, 0.8));
    }
    
    /* 🔮 SUBTÍTULO CON EL MISMO DEGRADADO ROSA Y MORADO 🔮 */
    .gradient-subtitle {
        font-size: 17px !important;
        font-weight: 800 !important;
        background: linear-gradient(45deg, #FF1493, #9400D3) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        display: inline-block !important;
        margin: 6px 0 0 0 !important;
        filter: drop-shadow(1px 1px 1px rgba(255, 255, 255, 0.8));
    }
    
    /* Ajustes adaptables perfectos para Celulares */
    @media (max-width: 768px) {
        .fb-cover-wrapper { height: 150px; }
        .fb-profile-row {
            flex-direction: column;
            align-items: center;
            margin-top: -55px;
            padding: 0 10px 10px 10px;
            text-align: center;
        }
        .fb-profile-avatar { width: 110px; height: 110px; border-width: 4px; }
        .fb-profile-info { margin-left: 0; margin-top: 15px; }
        .gradient-title { font-size: 24px !important; }
        .gradient-subtitle { font-size: 14px !important; }
    }
    
    /* ========================================================
       TARJETAS Y CONTENIDOS (ESTILO SHEIN / HIGHLIGHTS)
       ======================================================== */
    .stForm, .preview-container, .public-block, .admin-box {
        background-color: rgba(255, 255, 255, 0.98) !important;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.15);
        margin-bottom: 25px;
    }
    
    .shein-card {
        background-color: #FFFFFF !important;
        border: 2px solid #FFB3C6 !important;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.05);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
    }
    
    label, p, span, .stRadio p, h1, h2, h3, div[data-testid="stMarkdownContainer"] p {
        color: #1A1A1A !important;
        font-weight: bold !important;
    }
    
    textarea, input[type="text"], div[data-testid="stTextArea"] textarea, div[data-testid="stTextInput"] input {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        border: 2px solid #FF477E !important;
        -webkit-text-fill-color: #1A1A1A !important;
        caret-color: #1A1A1A !important;
    }
    
    textarea::placeholder, div[data-testid="stTextArea"] textarea::placeholder {
        color: #888888 !important;
        -webkit-text-fill-color: #888888 !important;
        font-weight: normal !important;
        opacity: 0.7 !important;
    }
    
    div[data-testid="stFileUploader"] section {
        background-color: #FFF0F5 !important;
        border: 2px dashed #E6005C !important;
        border-radius: 10px !important;
    }
    div[data-testid="stFileUploader"] section * { color: #1A1A1A !important; }
    div[data-testid="stFileUploader"] button { background-color: #E6005C !important; color: #FFFFFF !important; }
    
    div[data-testid="stFormSubmitButton"] button, .stSubmitButton button, div.stSubmitButton > button {
        background-color: #E6005C !important;
        color: #FFFFFF !important;
        border: 2px solid #FFFFFF !important;
        border-radius: 10px !important;
        padding: 14px 28px !important;
        width: 100% !important;
        box-shadow: 0px 6px 15px rgba(230, 0, 92, 0.4) !important;
    }
    div[data-testid="stFormSubmitButton"] button *, .stSubmitButton button *, div.stSubmitButton > button * {
        color: #FFFFFF !important;
        font-size: 20px !important;
        font-weight: 900 !important;
    }
    
    div[data-testid="stHorizontalBlock"] button, div[data-testid="element-container"] button {
        background-color: #E6005C !important;
        color: #FFFFFF !important;
        border: 1px solid #FFFFFF !important;
        border-radius: 8px !important;
    }
    div[data-testid="stHorizontalBlock"] button *, div[data-testid="element-container"] button * { color: #FFFFFF !important; }

    div.stButton > button {
        background-color: #25D366 !important;
        color: #1A1A1A !important;
        border: 2px solid #FFFFFF !important;
        border-radius: 12px !important;
        padding: 16px 32px !important;
        width: 100% !important;
        box-shadow: 0px 6px 18px rgba(37, 211, 102, 0.4) !important;
    }
    div.stButton > button * { color: #1A1A1A !important; font-size: 19px !important; font-weight: 900 !important; }
    
    .mini-foto img {
        max-height: 100px !important;
        object-fit: contain !important;
        border-radius: 6px;
        border: 1px solid #FFB3C6;
    }
    
    .articulos-box-shein {
        background-color: #F8F9FA !important;
        color: #1A1A1A !important;
        padding: 10px;
        border-radius: 6px;
        border-left: 4px solid #E6005C;
        font-size: 14px;
        white-space: pre-wrap;
        margin-bottom: 10px;
        max-height: 150px;
        overflow-y: auto;
    }
    
    .badge-activo-shein {
        background-color: #D4EDDA; color: #155724; padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; display: inline-block;
    }
    
    .btn-wa-nativo {
        display: block;
        width: 100%;
        background-color: #25D366 !important;
        color: #1A1A1A !important;
        text-align: center;
        padding: 16px 32px;
        border-radius: 12px;
        font-size: 19px;
        font-weight: 900;
        text-decoration: none;
        border: 2px solid #FFFFFF;
        box-shadow: 0px 6px 18px rgba(37, 211, 102, 0.4);
        margin-top: 10px;
    }

    .seccion-quejas {
        text-align: center;
        font-size: 11px !important;
        color: #666666 !important;
        margin-top: 20px;
        font-weight: normal !important;
    }

    /* ✨ MEJORA: Aviso de seguridad tenue con Glassmorphism Rosa Pastel ✨ */
    .alerta-seguridad-principal {
        background-color: rgba(255, 240, 245, 0.45) !important;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 16px;
        border-left: 5px solid #FF477E;
        border-top: 1px solid rgba(255, 255, 255, 0.4);
        border-right: 1px solid rgba(255, 255, 255, 0.4);
        border-bottom: 1px solid rgba(255, 255, 255, 0.4);
        margin-bottom: 25px;
        box-shadow: 0 8px 20px 0 rgba(230, 0, 92, 0.05);
    }
    .alerta-seguridad-principal p { 
        color: #4A0E17 !important; 
        font-size: 14.5px !important; 
        font-weight: 500 !important; 
        margin: 0 !important; 
        line-height: 1.5;
    }

    @media (max-width: 768px) {
        div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: wrap !important; gap: 10px !important; }
        div[data-testid="column"] { flex: 1 1 45% !important; min-width: 45% !important; }
        .shein-card { padding: 8px !important; margin-bottom: 10px !important; }
        .shein-card h4 { font-size: 13px !important; }
        .shein-card p, .articulos-box-shein { font-size: 11px !important; max-height: 90px !important; }
        div[data-testid="column"] div[data-testid="column"] { flex: 1 1 20% !important; min-width: 20% !important; }
        .mini-foto img { max-height: 45px !important; object-fit: cover !important; }
        .shein-card button { font-size: 11px !important; padding: 6px 4px !important; }
    }
    </style>
""", unsafe_allow_html=True)

# --- 5. ENRENDERIZADO DEL ENCABEZADO MEJORADO CORREGIDO ---
fondo_portada_fallback = img_portada_base64 if img_portada_base64 else "linear-gradient(90deg, #FFB3C6, #FF8FAB)"
fondo_perfil_fallback = img_perfil_base64 if img_perfil_base64 else "linear-gradient(135deg, #FF477E, #FF8FAB)"

st.markdown(f"""
    <div class="fb-header-container">
        <div class="fb-cover-wrapper" style="background: {fondo_portada_fallback if not img_portada_base64 else 'none'};">
            {f'<img src="{img_portada_base64}" />' if img_portada_base64 else ''}
        </div>
        <div class="fb-profile-row">
            <div class="fb-profile-avatar" style="background: {fondo_perfil_fallback if not img_perfil_base64 else '#FFFFFF'}; display: flex; align-items: center; justify-content: center;">
                {f'<img src="{img_perfil_base64}" />' if img_perfil_base64 else '<span style="font-size:35px;">✨</span>'}
            </div>
            <div class="fb-profile-info">
                <h1 class="gradient-title">✨ BAZAR DIGITAL DE K-POP & CLÓSET ✨</h1>
                <p class="gradient-subtitle">🛍️ Photocards, Coleccionables & Moda • Monterrey</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)


# --- 6. PESTAÑAS PRINCIPALES DE LA APLICACIÓN ---
tab_bazar, tab_anunciarse, tab_admin = st.tabs(["🛍️ Ver el Bazar / Clóset", "💜 Registrarse como Vendedora", "🔐 Panel Admin"])

# ==========================================
# PESTAÑA 1: EL ESCAPARATE PÚBLICO
# ==========================================
with tab_bazar:
    st.markdown("""
        <div class="alerta-seguridad-principal">
            <p>
                💓 <b>Aviso de Seguridad Importante:</b> Recuerda realizar tus entregas únicamente en <b>lugares públicos y concurridos</b>. 
                Cada vendedora se hace completamente responsable de sus artículos, precios, acuerdos de entrega y citas correspondientes. 
                Este espacio funciona únicamente como catálogo digital, por lo que toda transacción y trato es totalmente ajeno a la aplicación.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("🛒 Clósets y Productos Disponibles")
    bloques_activos = {k: v for k, v in st.session_state.bloques_db.items() if v['estado'] == "🟢 ACTIVO"}
    
    if not bloques_activos:
        st.info("No hay tienditas activas en este momento. Las publicaciones aprobadas aparecerán aquí de inmediato.")
    else:
        lista_bloques = list(bloques_activos.items())
        
        hora_actual = datetime.now().hour
        desplazamiento = hora_actual % len(lista_bloques)
        lista_rotada = lista_bloques[desplazamiento:] + lista_bloques[:desplazamiento]
        
        columnas_por_fila = 3
        
        for i in range(0, len(lista_rotada), columnas_por_fila):
            fila_bloques = lista_rotada[i:i+columnas_por_fila]
