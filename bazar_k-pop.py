import streamlit as st
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests

# Configuración de la página
st.set_page_config(
    page_title="Bazar Digital K-Pop & Clóset",
    page_icon="✨",
    layout="wide"
)

# ⚠️ CONFIGURACIÓN CLAVE ⚠️
TELEFONO_ADMIN_WHATSAPP = "528143029578"
CONTRASENA_ADMIN = "bazar123"
URL_HOJA_CALCULO = "https://docs.google.com/spreadsheets/d/1uj8Vkw3uQn5GYy7LD7ADwXH3mtpvpZu2vQtiZ33yCXQ/edit?usp=sharing"

# 🔥 TU LLAVE DE IMGBB INTEGRADA 🔥
IMGBB_API_KEY = "c72da82c65cce967aac091defc1f41dd"

# --- CONEXIÓN DE GOOGLE SHEETS ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_sheets = conn.read(spreadsheet=URL_HOJA_CALCULO, ttl="2s").dropna(how="all")
except Exception as e:
    df_sheets = pd.DataFrame(columns=["id", "vendedor", "whatsapp", "zona", "categoria", "articulos", "estado", "fecha", "fotos_links", "comprobante_link"])

# --- FUNCIÓN INVISIBLE IMGBB ---
def subir_a_imgbb(archivo_imagen):
    if archivo_imagen is None:
        return None
    try:
        url = "https://api.imgbb.com/1/upload"
        payload = {"key": IMGBB_API_KEY}
        files = {"image": archivo_imagen.getvalue()}
        response = requests.post(url, payload, files=files)
        data = response.json()
        if data["status"] == 200:
            return data["data"]["url"]
    except:
        pass
    return None

# --- SINCRO DE BASE DE DATOS ---
if "bloques_db" not in st.session_state:
    st.session_state.bloques_db = {}

for _, row in df_sheets.iterrows():
    b_id = str(row["id"])
    links_fotos = str(row.get("fotos_links", "")).split(",") if pd.notna(row.get("fotos_links", "")) else []
    links_fotos = [l for l in links_fotos if l.strip()]
    
    st.session_state.bloques_db[b_id] = {
        "vendedor": str(row["vendedor"]),
        "whatsapp": str(row["whatsapp"]),
        "zona": str(row["zona"]),
        "categoria": str(row["categoria"]),
        "articulos": str(row["articulos"]),
        "estado": str(row["estado"]),
        "fecha": str(row["fecha"]),
        "imagenes_links": links_fotos,
        "comprobante_link": str(row.get("comprobante_link", ""))
    }

def guardar_en_sheets(id_b, info_b):
    try:
        df_actual = conn.read(spreadsheet=URL_HOJA_CALCULO, ttl=0).dropna(how="all")
        df_actual = df_actual[df_actual["id"].astype(str) != str(id_b)]
        nuevo_registro = pd.DataFrame([{
            "id": str(id_b),
            "vendedor": str(info_b["vendedor"]),
            "whatsapp": str(info_b["whatsapp"]),
            "zona": str(info_b["zona"]),
            "categoria": str(info_b["categoria"]),
            "articulos": str(info_b["articulos"]),
            "estado": str(info_b["estado"]),
            "fecha": str(info_b["fecha"]),
            "fotos_links": ",".join(info_b.get("imagenes_links", [])),
            "comprobante_link": str(info_b.get("comprobante_link", ""))
        }])
        df_actual = pd.concat([df_actual, nuevo_registro], ignore_index=True)
        conn.update(spreadsheet=URL_HOJA_CALCULO, data=df_actual)
    except:
        pass

# --- TU DISEÑO ORIGINAL Y ESTILOS CSS REFORZADOS ---
st.markdown("""
    <style>
    /* Tu fondo rosa degradado completo */
    .stApp {
        background: linear-gradient(135deg, #FFE5EC 0%, #FFB3C6 40%, #FF477E 100%) !important;
    }
    /* Estilos de tus tarjetas blancas de productos */
    .shein-card {
        background-color: #FFFFFF !important;
        border: 2px solid #FFB3C6 !important;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.05);
    }
    /* Tu caja de texto de seguridad amarilla idéntica */
    .alerta-amarilla {
        background-color: #FFF8E7 !important;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #FFC107;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }
    .alerta-amarilla p {
        color: #1A1A1A !important;
        font-size: 14px !important;
        line-height: 1.6 !important;
        margin: 0 !important;
    }
    /* Arreglo para que se lea perfecto la cuenta NU */
    .tarjeta-nu {
        background-color: #5F259F !important; /* Morado Nu profesional */
        color: #FFFFFF !important;
        padding: 18px;
        border-radius: 12px;
        margin-bottom: 20px;
        border: 2px solid #FFFFFF;
    }
    .tarjeta-nu b, .tarjeta-nu div {
        color: #FFFFFF !important;
    }
    /* Tus botones verdes nativos de confirmación final */
    .btn-verde-wa {
        display: block; width: 100%; background-color: #25D366 !important; color: #1A1A1A !important;
        text-align: center; padding: 14px; border-radius: 10px; font-size: 16px; font-weight: bold;
        text-decoration: none; border: 2px solid #FFFFFF; margin-bottom: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    .btn-limpiar {
        display: block; width: 100%; background-color: #25D366 !important; color: #1A1A1A !important;
        text-align: center; padding: 12px; border-radius: 10px; font-size: 15px; font-weight: bold;
        text-decoration: none; border: 2px solid #FFFFFF; margin-top: 15px;
    }
    .texto-instruccion {
        background-color: rgba(255,255,255,0.2); padding: 12px; border-radius: 8px; text-align: center; margin-bottom: 15px;
    }
    .articulos-box {
        background-color: #F8F9FA !important; color: #1A1A1A !important; padding: 10px; border-radius: 6px;
        border-left: 4px solid #E6005C; font-size: 14px; white-space: pre-wrap;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezados originales
st.markdown('<div style="text-align:center; font-size:46px; font-weight:900; color:#E6005C; font-family:sans-serif; margin-bottom:0;">CLÓSET ✨</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center; font-size:18px; color:white; font-weight:bold; margin-bottom:25px;">🛍️ Photocards, Coleccionables & Moda • Monterrey</div>', unsafe_allow_html=True)

tab_bazar, tab_anunciarse, tab_admin = st.tabs(["🛍️ Ver el Bazar / Clóset", "💜 Registrarse como Vendedora", "🔐 Panel de Control"])

# ==========================================
# TAB 1: ESCAPARATE PÚBLICO
# ==========================================
with tab_bazar:
    # Tu texto de aviso de seguridad exacto
    st.markdown("""
        <div class="alerta-amarilla">
            ⚠️ <b>Aviso de Seguridad:</b> Recuerda realizar tus entregas únicamente en lugares públicos y concurridos. 
            <b>Cada vendedora se hace completamente responsable de sus artículos, precios, acuerdos de entrega y citas correspondientes.</b> 
            Este espacio funciona únicamente como catálogo digital, por lo que toda transacción y trato es totalmente ajeno a la aplicación.
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="font-size:28px; font-weight:bold; margin-bottom:15px;">🛒 Clósets y Productos Disponibles</div>', unsafe_allow_html=True)
    
    bloques_activos = {k: v for k, v in st.session_state.bloques_db.items() if "ACTIVO" in str(v['estado'])}
    
    if not bloques_activos:
        st.info("No hay tienditas activas en este momento. Las publicaciones aprobadas aparecerán aquí.")
    else:
        cols = st.columns(3)
        for idx, (id_b, info_b) in enumerate(bloques_activos.items()):
            with cols[idx % 3]:
                url_wa_vendedor = f"https://wa.me/{info_b['whatsapp']}?text=Hola,%20vengo%20del%20bazar%20digital,%20me%20interesó%20tu%20anuncio!%20✨"
                st.markdown(f"""
                    <div class="shein-card">
                        <div style="display: flex; justify-content: space-between; font-size: 11px; color: #666666;">
                            <span>🟢 ACTIVO</span><span>📅 {info_b['fecha']}</span>
                        </div>
                        <h3 style="color:#D81159; margin-top:5px; margin-bottom:5px;">🛍️ {info_b['vendedor']}</h3>
                        <p style="font-size:13px; margin:2px 0;">📂 <b>Categoría:</b> {info_b['categoria']}</p>
                        <p style="font-size:13px; margin:2px 0; margin-bottom:8px;">📍 <b>Punto:</b> {info_b['zona']}</p>
                        <div class="articulos-box">{info_b['articulos']}</div>
                """, unsafe_allow_html=True)
                
                if info_b.get("imagenes_links"):
                    st.markdown("<br>", unsafe_allow_html=True)
                    cols_img = st.columns(4)
                    for idx_img, link_url in enumerate(info_b["imagenes_links"][:4]):
                        with cols_img[idx_img % 4]:
                            st.image(link_url, use_container_width=True)
                
                st.markdown(f"""
                        <div style="margin-top: 15px;">
                            <a href="{url_wa_vendedor}" target="_blank"><button style="background-color:#E6005C; color:white; border:none; padding:10px; border-radius:8px; width:100%; font-weight:bold; cursor:pointer;">💬 Ver el Bazar / Clóset</button></a>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

# ==========================================
# TAB 2: REGISTRO DE VENDEDORAS
# ==========================================
with tab_anunciarse:
    st.markdown('<div style="font-size:24px; font-weight:bold; margin-bottom:15px;">💜 Ingresa tus datos aquí abajo:</div>', unsafe_allow_html=True)
    
    if "registro_guardado" not in st.session_state:
        st.session_state.registro_guardado = None

    if st.session_state.registro_guardado is None:
        with st.form("form_registro"):
            nombre = st.text_input("Nombre de tu Tienda / Vendedora *")
            whatsapp = st.text_input("WhatsApp (10 dígitos sin espacios) *")
            zona = st.text_input("Punto Seguro de Entrega en Monterrey *")
            cat = st.radio("Categoría principal: *", ["K-Pop (Photocards/Coleccionables)", "Mi Clóset (Ropa/Accesorios)"])
            articulos = st.text_area("Tus productos y precios (Uno por renglón) *")
            fotos = st.file_uploader("Fotos de tus artículos (Sube varias a la vez):", type=["jpg","png","jpeg"], accept_multiple_files=True)
            
            st.markdown("### 💳 Validación Obligatoria ($25 MXN)")
            st.markdown("""
                <div class="tarjeta-nu">
                    <b>🏛 Imos: NU MÉXICO</b><br>
                    🔑 CLABE INTERBANCARIA: <code>0123 4567 8901 2345 67</code><br>
                    👤 TITULAR DE LA CUENTA: YAJAIRA LEIJA
                </div>
            """, unsafe_allow_html=True)
            
            comprobante = st.file_uploader("Sube la captura de tu comprobante de pago *", type=["jpg","png","jpeg"])
            
            enviar = st.form_submit_button("Subir Bloque de Anuncios")
            
            if enviar:
                if not (nombre and whatsapp and zona and articulos and comprobante):
                    st.error("Rellena todos los campos obligatorios (*).")
                else:
                    with st.spinner("Subiendo de forma segura... ✨"):
                        links_fotos = [subir_a_imgbb(f) for f in fotos] if fotos else []
                        links_fotos = [l for l in links_fotos if l ]
                        url_comp = subir_a_imgbb(comprobante)
                        
                        id_t = f"BZR-{datetime.now().strftime('%d%H%M%S')}"
                        info_b = {
                            "vendedor": nombre, "whatsapp": whatsapp, "zona": zona,
                            "categoria": cat, "articulos": articulos, "estado": "⏳ En espera",
                            "fecha": datetime.now().strftime("%d/%m/%Y"),
                            "imagenes_links": links_fotos, "comprobante_link": url_comp if url_comp else ""
                        }
                        
                        st.session_state.bloques_db[id_t] = info_b
                        guardar_en_sheets(id_t, info_b)
                        st.session_state.registro_guardado = id_t
                        st.rerun()
    else:
        id_actual = st.session_state.registro_guardado
        datos_b = st.session_state.bloques_db.get(id_actual, {})
        
        st.markdown('<div style="font-size:28px; font-weight:900; margin-bottom:15px;">📲 ¡Paso Final Obligatorio!</div>', unsafe_allow_html=True)
        st.success("✅ ¡Datos registrados con éxito en el panel de administración!")
        
        msg_wa = f"Hola, mandé registro de Bazar.\n👤 Vendedora: {datos_b.get('vendedor')}\n🆔 ID: {id_actual}"
        url_wa = f"https://wa.me/528143029578?text={msg_wa.replace(' ', '%20')}"
        
        st.markdown(f'<a class="btn-verde-wa" href="{url_wa}" target="_blank">🚀 ¡TODO LISTO! CLIC AQUÍ PARA CONFIRMAR TU PAGO VÍA WHATSAPP</a>', unsafe_allow_html=True)
        st.markdown('<div class="texto-instruccion"><p style="margin:0; color:#1A1A1A;">Al dar clic arriba se abrirá el chat. No olvides adjuntar foto del comprobante.</p></div>', unsafe_allow_html=True)
        
        if st.button("🧹 Limpiar historial y registrar nueva tiendita"):
            st.session_state.registro_guardado = None
            st.rerun()

# ==========================================
# TAB 3: PANEL DE CONTROL
# ==========================================
with tab_admin:
    clave = st.text_input("Contraseña de Administradora:", type="password")
    if clave == CONTRASENA_ADMIN:
        st.success("Acceso Autorizado")
        for b_id in list(st.session_state.bloques_db.keys()):
            b_info = st.session_state.bloques_db[b_id]
            st.write(f"🆔 **ID:** `{b_id}` | 👤 **Vendedora:** {b_info['vendedor']} | Estado: `{b_info['estado']}`")
            
            if b_info.get("comprobante_link"):
                st.markdown(f"[👁️ Ver Comprobante de Pago]({b_info['comprobante_link']})")
            
            col_a1, col_a2 = st.columns(2)
            with col_a1:
                if "espera" in str(b_info['estado']).lower():
                    if st.button("🟢 Aprobar", key=f"ap_{b_id}"):
                        st.session_state.bloques_db[b_id]['estado'] = "🟢 ACTIVO"
                        guardar_en_sheets(b_id, st.session_state.bloques_db[b_id])
                        st.rerun()
            with col_a2:
                if st.button("🗑️ Eliminar", key=f"dl_{b_id}"):
                    if b_id in st.session_state.bloques_db: del st.session_state.bloques_db[b_id]
                    try:
                        df_actual = conn.read(spreadsheet=URL_HOJA_CALCULO, ttl=0).dropna(how="all")
                        df_actual = df_actual[df_actual["id"].astype(str) != str(b_id)]
                        conn.update(spreadsheet=URL_HOJA_CALCULO, data=df_actual)
                    except: pass
                    st.rerun()
            st.markdown("<hr>", unsafe_allow_html=True)

st.markdown('<div style="text-align:center; font-size:11px; color:#666666; margin-top:30px;">Quejas, sugerencias y aclaraciones, con Capitana Albatros: 8143029578</div>', unsafe_allow_html=True)
