import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# 🟢 CONFIGURACIÓN INICIAL DE LA PÁGINA (ORIGINAL)
st.set_page_config(
    page_title="Bazar Digital K-Pop & Clóset",
    page_icon="✨",
    layout="wide"
)

# ⚠️ TU CONFIGURACIÓN (Manteniendo tus variables originales)
TELEFONO_ADMIN_WHATSAPP = "528143029578"
CONTRASENA_ADMIN = "bazar123"

# =====================================================================
# 🛠️ EL TRUCO SIN .TOML: ENLACE DIRECTO A TU GOOGLE SHEET
# =====================================================================
# 1. Crea un Google Sheet normal con estas columnas: ID, Vendedora, WhatsApp, Zona, Categoria, Articulos, Fecha
# 2. En tu Google Sheet ve a: Extensiones -> Apps Script. Borra todo, pega este código de 4 líneas y dale "Desplegar como Aplicación Web" (Acceso: Cualquiera):
#    function doPost(e) { var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet(); sheet.appendRow(JSON.parse(e.postData.contents)); return ContentService.createTextOutput("OK"); }
# 3. Pega la URL que te dé Apps Script aquí abajo:
URL_MI_BASE_DE_DATOS = "TU_URL_DE_APPS_SCRIPT_AQUÍ"

# URL de lectura pública de tu Google Sheet (Archivo -> Compartir -> Cualquiera con el enlace puede ver)
URL_LECTURA_SHEET = "https://docs.google.com/spreadsheets/d/TU_ID_DE_HOJA/gviz/tq?tqx=out:csv"

# --- FUNCIÓN DE LECTURA DIRECTA (Para todos los celulares) ---
def cargar_bloques_globales():
    try:
        # Lee el archivo CSV directamente de la nube en un segundo sin usar librerías raras
        df = pd.read_csv(URL_LECTURA_SHEET)
        db_temporal = {}
        for _, fila in df.iterrows():
            db_temporal[str(fila['ID'])] = {
                "vendedor": str(fila['Vendedora']),
                "whatsapp": str(fila['WhatsApp']),
                "zona": str(fila['Zona']),
                "categoria": str(fila['Categoria']),
                "articulos": str(fila['Articulos']),
                "estado": "🟢 ACTIVO",
                "fecha": str(fila['Fecha']),
                "imagenes": [] # Las imágenes se manejan por flujo de WhatsApp para no saturar
            }
        return db_temporal
    except:
        # Si falla el internet o está vacío, regresa el diccionario en memoria original
        if "bloques_db" not in st.session_state:
            st.session_state.bloques_db = {}
        return st.session_state.bloques_db

# Sincronizamos la base de datos directo desde la nube al abrir la app
bloques_sistema = cargar_bloques_globales()

# --- ESTILOS CSS REFORZADOS (TU ESTILO ORIGINAL EXACTO) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #FFE5EC 0%, #FFB3C6 40%, #FF477E 100%); }
    .stForm, .preview-container, .public-block, .admin-box {
        background-color: rgba(255, 255, 255, 0.98) !important;
        padding: 20px; border-radius: 15px; box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.15); margin-bottom: 25px;
    }
    .shein-card {
        background-color: #FFFFFF !important; border: 2px solid #FFB3C6 !important; border-radius: 12px;
        padding: 15px; margin-bottom: 20px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.05);
        display: flex; flex-direction: column; justify-content: space-between; height: 100%;
    }
    label, p, span, .stRadio p, h1, h2, h3, div[data-testid="stMarkdownContainer"] p {
        color: #1A1A1A !important; font-weight: bold !important;
    }
    textarea, input[type="text"], div[data-testid="stTextArea"] textarea, div[data-testid="stTextInput"] input {
        background-color: #FFFFFF !important; color: #1A1A1A !important; border: 2px solid #FF477E !important;
        -webkit-text-fill-color: #1A1A1A !important; caret-color: #1A1A1A !important;
    }
    div[data-testid="stFormSubmitButton"] button, .stSubmitButton button, div.stSubmitButton > button {
        background-color: #E6005C !important; color: #FFFFFF !important; border: 2px solid #FFFFFF !important;
        border-radius: 10px !important; padding: 14px 28px !important; width: 100% !important; font-weight: 900 !important;
    }
    div.stButton > button {
        background-color: #25D366 !important; color: #1A1A1A !important; border: 2px solid #FFFFFF !important;
        border-radius: 12px !important; padding: 16px 32px !important; width: 100% !important; font-weight: 900 !important;
    }
    .articulos-box-shein {
        background-color: #F8F9FA !important; color: #1A1A1A !important; padding: 10px; border-radius: 6px;
        border-left: 4px solid #E6005C; font-size: 14px; white-space: pre-wrap; margin-bottom: 10px; max-height: 150px; overflow-y: auto;
    }
    .btn-wa-nativo {
        display: block; width: 100%; background-color: #25D366 !important; color: #1A1A1A !important;
        text-align: center; padding: 16px 32px; border-radius: 12px; font-size: 19px; font-weight: 900; text-decoration: none;
    }
    .seccion-quejas { text-align: center; font-size: 11px !important; color: #666666 !important; margin-top: 20px; }
    .alerta-seguridad-principal {
        background-color: #FFF3CD !important; color: #856404 !important; padding: 20px; border-radius: 12px; border-left: 6px solid #FFC107; margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# --- ENCABEZADO ORIGINAL ---
st.markdown('<div style="text-align:center; font-size:42px; font-weight:900; color:#D81159;">✨ BAZAR DIGITAL DE K-POP & CLÓSET ✨</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center; font-size:18px; color:white; font-weight:bold; margin-bottom:25px;">🛍️ Photocards, Coleccionables & Moda • Monterrey</div>', unsafe_allow_html=True)

tab_bazar, tab_anunciarse, tab_admin = st.tabs(["🛍️ Ver el Bazar / Clóset", "💜 Registrarse como Vendedora", "🔐 Panel de Control (Solo Admin)"])

# ==========================================
# PESTAÑA 1: EL ESCAPARATE PÚBLICO
# ==========================================
with tab_bazar:
    st.markdown('<div class="alerta-seguridad-principal"><p>⚠️ <b>Aviso de Seguridad:</b> Entregas en lugares públicos. App solo informativa.</p></div>', unsafe_allow_html=True)
    
    if not bloques_sistema:
        st.info("No hay tienditas activas en este momento.")
    else:
        lista_bloques = list(bloques_sistema.items())
        for i in range(0, len(lista_bloques), 3):
            fila_bloques = lista_bloques[i:i+3]
            cols = st.columns(3)
            for idx_col, (id_b, info_b) in enumerate(fila_bloques):
                with cols[idx_col]:
                    texto_codificado = "Hola, vengo del bazar digital de k-pop...".replace(' ', '%20')
                    url_wa_vendedor = f"https://wa.me/{info_b['whatsapp']}?text={texto_codificado}"

                    st.markdown(f"""
                        <div class="shein-card">
                            <div>
                                <h4 style="margin: 0; color:#D81159; font-size: 18px;">🛍️ Bazar de {info_b['vendedor']}</h4>
                                <p style="font-size: 12px; margin: 5px 0;">📍 <b>Punto:</b> {info_b['zona']}</p>
                                <div class="articulos-box-shein">{info_b['articulos']}</div>
                            </div>
                            <div style="margin-top: 15px;">
                                <a href="{url_wa_vendedor}" target="_blank" class="btn-wa-nativo" style="font-size:13px; padding:10px;">💬 WhatsApp</a>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

# ==========================================
# PESTAÑA 2: REGISTRO DE VENDEDORAS (ORIGINAL)
# ==========================================
with tab_anunciarse:
    st.subheader("💜 Registra tu Bloque de Anuncios")
    
    with st.form("form_anuncio", clear_on_submit=True):
        nombre_vendedor = st.text_input("Nombre / Tienda *")
        whatsapp_vendedor = st.text_input("WhatsApp de Contacto *")
        zona_entrega = st.text_input("Punto Seguro de Entrega *")
        tipo_articulo = st.radio("Categoría: *", ["K-Pop (Photocards/Coleccionables)", "Mi Clóset (Ropa/Accesorios)"])
        lista_articulos = st.text_area("Lista tus productos *")
        comprobante = st.file_uploader("Sube tu comprobante de transferencia *", type=["jpg", "png"])
        
        enviar_anuncio = st.form_submit_button("Subir Bloque de Anuncios para Validación")

        if enviar_anuncio and nombre_vendedor and whatsapp_vendedor:
            id_transaccion = f"BZR-{datetime.now().strftime('%d%H%M%S')}"
            st.session_state.pre_registro = {
                "id": id_transaccion, "vendedor": nombre_vendedor, "whatsapp": whatsapp_vendedor,
                "zona": zona_entrega, "categoria": tipo_articulo, "articulos": lista_articulos, "fecha": datetime.now().strftime("%d/%m/%Y")
            }
            st.success(f"¡Pre-registro creado! ID: {id_transaccion}. Pasa al paso final abajo.")

    if "pre_registro" in st.session_state and st.session_state.pre_registro:
        datos = st.session_state.pre_registro
        msg = f"Hola, realicé mi pago. ID: {datos['id']} de {datos['vendedor']}"
        url_wa = f"https://wa.me/{TELEFONO_ADMIN_WHATSAPP}?text={msg.replace(' ', '%20')}"
        
        st.markdown(f'<a class="btn-wa-nativo" href="{url_wa}" target="_blank">🚀 CONFIRMAR PAGO POR WHATSAPP</a>', unsafe_allow_html=True)

# ==========================================
# 🔐 PESTAÑA 3: PANEL DE CONTROL DE ADMINISTRADORA (TU PREFERIDO)
# ==========================================
with tab_admin:
    st.subheader("🔐 Consola de Verificación")
    clave_ingresada = st.text_input("Introduce la Contraseña de Administradora:", type="password")
    
    if clave_ingresada == CONTRASENA_ADMIN:
        st.success("Acceso Autorizado")
        
        # EL FORMULARIO ORIGINAL DE TU CAPTURA EXACTA "image_6cfa7f.jpg"
        st.markdown("## ➕ Registrar Vendedora Aprobada Directamente")
        
        with st.container(border=True):
            col_adm1, col_adm2 = st.columns(2)
            with col_adm1:
                admin_nombre = st.text_input("Nombre de la Vendedora:")
                admin_whatsapp = st.text_input("WhatsApp (10 dígitos):")
            with col_adm2:
                admin_zona = st.text_input("Punto Seguro de Entrega:")
                admin_cat = st.selectbox("Categoría:", ["K-Pop (Photocards/Coleccionables)", "Mi Clóset (Ropa/Accesorios)"])
            
            admin_articulos = st.text_area("Artículos (Uno por renglón):")
            
            # 🟢 TU BOTÓN INTERNO DE CONTROL EXCLUSIVO
            if st.button("🟢 ACTIVAR E INYECTAR AL BAZAR TRAS VALIDAR", use_container_width=True):
                if admin_nombre and admin_whatsapp:
                    id_directo = f"BZR-DIR-{datetime.now().strftime('%d%H%M%S')}"
                    fecha_hoy = datetime.now().strftime("%d/%m/%Y")
                    
                    # 🚀 ENVÍO SIN CREDENCIALES: Hace un POST directo a la API de tu Sheet
                    datos_a_guardar = [id_directo, admin_nombre, admin_whatsapp, admin_zona, admin_cat, admin_articulos, fecha_hoy]
                    try:
                        requests.post(URL_MI_BASE_DE_DATOS, json=datos_a_guardar)
                        st.success(f"¡Inyectado con éxito a la nube! Ya aparece en todos los celulares.")
                        st.rerun()
                    except:
                        # Si no has puesto tu URL de Sheet todavía, lo guarda en la sesión actual para que pruebes
                        st.session_state.bloques_db[id_directo] = {
                            "vendedor": admin_nombre, "whatsapp": admin_whatsapp, "zona": admin_zona,
                            "categoria": admin_cat, "articulos": admin_articulos, "estado": "🟢 ACTIVO", "fecha": fecha_hoy
                        }
                        st.warning("Guardado localmente (Configura la URL para que se guarde en todos los celulares).")

st.markdown('<div class="seccion-quejas">Con Capitana Albatros: 528143029578</div>', unsafe_allow_html=True)
