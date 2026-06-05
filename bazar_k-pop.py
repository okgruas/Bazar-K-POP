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

# ⚠️ CONFIGURACIÓN DE ADMINISTRADOR & LLAVES ⚠️
TELEFONO_ADMIN_WHATSAPP = "528143029578"
CONTRASENA_ADMIN = "bazar123"
URL_HOJA_CALCULO = "https://docs.google.com/spreadsheets/d/1uj8Vkw3uQn5GYy7LD7ADwXH3mtpvpZu2vQtiZ33yCXQ/edit?usp=sharing"

# 🔥 PEGA AQUÍ TU LLAVE DE IMGBB QUE COPIASTE EN EL PASO 1 🔥
IMGBB_API_KEY = "TU_LLAVE_DE_IMGBB_AQUÍ" 

# --- CONEXIÓN DE GOOGLE SHEETS ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_sheets = conn.read(spreadsheet=URL_HOJA_CALCULO, ttl="2s")
    df_sheets = df_sheets.dropna(how="all")
except Exception as e:
    df_sheets = pd.DataFrame(columns=["id", "vendedor", "whatsapp", "zona", "categoria", "articulos", "estado", "fecha", "fotos_links", "comprobante_link"])

# --- FUNCIÓN PARA SUBIR IMÁGENES A LA NUBE GRATIS (IMGBB) ---
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
            return data["data"]["url"] # Nos da el link directo de internet
    except Exception as e:
        st.error(f"Error al subir imagen a la nube: {e}")
    return None

# --- BASE DE DATOS LOCAL SINCRO ---
if "bloques_db" not in st.session_state:
    st.session_state.bloques_db = {}

# Cargar los datos desde Sheets de vuelta a la app
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

# --- FUNCIÓN PARA GUARDAR TODO EN GOOGLE SHEETS ---
def guardar_en_sheets(id_b, info_b):
    try:
        try:
            df_actual = conn.read(spreadsheet=URL_HOJA_CALCULO, ttl=0).dropna(how="all")
        except:
            df_actual = pd.DataFrame(columns=["id", "vendedor", "whatsapp", "zona", "categoria", "articulos", "estado", "fecha", "fotos_links", "comprobante_link"])
        
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
    except Exception as e:
        st.error(f"Error al guardar en Google Sheets: {e}")

def eliminar_de_sheets(id_b):
    try:
        df_actual = conn.read(spreadsheet=URL_HOJA_CALCULO, ttl=0).dropna(how="all")
        df_actual = df_actual[df_actual["id"].astype(str) != str(id_b)]
        conn.update(spreadsheet=URL_HOJA_CALCULO, data=df_actual)
    except:
        pass

# --- DISEÑO CSS ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #FFE5EC 0%, #FFB3C6 40%, #FF477E 100%); }
    .stForm, .preview-container, .public-block, .admin-box {
        background-color: rgba(255, 255, 255, 0.98) !important; padding: 20px; border-radius: 15px;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.15); margin-bottom: 25px;
    }
    .shein-card {
        background-color: #FFFFFF !important; border: 2px solid #FFB3C6 !important; border-radius: 12px;
        padding: 15px; margin-bottom: 20px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.05);
        display: flex; flex-direction: column; justify-content: space-between; height: 100%;
    }
    label, p, span, .stRadio p, h1, h2, h3, div[data-testid="stMarkdownContainer"] p { color: #1A1A1A !important; font-weight: bold !important; }
    textarea, input[type="text"], div[data-testid="stTextArea"] textarea, div[data-testid="stTextInput"] input {
        background-color: #FFFFFF !important; color: #1A1A1A !important; border: 2px solid #FF477E !important;
    }
    div[data-testid="stFileUploader"] section { background-color: #FFF0F5 !important; border: 2px dashed #E6005C !important; }
    div[data-testid="stFormSubmitButton"] button { background-color: #E6005C !important; color: #FFFFFF !important; border-radius: 10px !important; width: 100% !important; }
    .articulos-box-shein {
        background-color: #F8F9FA !important; color: #1A1A1A !important; padding: 10px; border-radius: 6px;
        border-left: 4px solid #E6005C; font-size: 14px; white-space: pre-wrap; max-height: 150px; overflow-y: auto;
    }
    .badge-activo-shein { background-color: #D4EDDA; color: #155724; padding: 3px 8px; border-radius: 4px; font-size: 11px; }
    .btn-wa-nativo {
        display: block; width: 100%; background-color: #25D366 !important; color: white !important;
        text-align: center; padding: 16px; border-radius: 12px; font-size: 18px; font-weight: bold; text-decoration: none;
    }
    .seccion-quejas { text-align: center; font-size: 11px; color: #666666; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown('<div style="text-align:center; font-size:42px; font-weight:900; color:#D81159;">✨ BAZAR DIGITAL DE K-POP & CLÓSET ✨</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center; font-size:18px; color:white; font-weight:bold; margin-bottom:25px;">🛍️ Publica Gratis y Vende en Monterrey</div>', unsafe_allow_html=True)

tab_bazar, tab_anunciarse, tab_admin = st.tabs(["🛍️ Ver el Bazar", "💜 Registrarse", "🔐 Panel de Control"])

# ==========================================
# TAB 1: ESCAPARATE PÚBLICO
# ==========================================
with tab_bazar:
    st.markdown('<div style="background-color: #FFF3CD; padding: 15px; border-radius: 10px; border-left: 6px solid #FFC107; margin-bottom: 20px;"><p style="color: #856404 !important; margin:0;">⚠️ <b>Aviso de Seguridad:</b> Haz tus entregas en lugares públicos (puntos de metro, plazas comerciales concurridas). ¡Cuida tu seguridad!</p></div>', unsafe_allow_html=True)

    bloques_activos = {k: v for k, v in st.session_state.bloques_db.items() if "ACTIVO" in str(v['estado'])}
    
    if not bloques_activos:
        st.info("¡El escaparate está listo! Esperando las primeras publicaciones aprobadas.")
    else:
        lista_bloques = list(bloques_activos.items())
        cols = st.columns(3)
        for idx, (id_b, info_b) in enumerate(lista_bloques):
            with cols[idx % 3]:
                url_wa_vendedor = f"https://wa.me/{info_b['whatsapp']}?text=Hola,%20vengo%20del%20bazar%20digital,%20me%20interesó%20tu%20anuncio!%20✨"
                st.markdown(f"""
                    <div class="shein-card">
                        <div>
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                <span class="badge-activo-shein">🟢 ACTIVO</span>
                                <span style="font-size: 11px; color: #666666;">📅 {info_b['fecha']}</span>
                            </div>
                            <h4 style="margin: 0 0 5px 0; color:#D81159; font-size: 18px;">🛍️ {info_b['vendedor']}</h4>
                            <p style="margin: 2px 0; color:#555555; font-size: 12px;">📂 <b>Categoría:</b> {info_b['categoria']}</p>
                            <p style="margin: 2px 0; color:#555555; font-size: 12px; margin-bottom: 10px;">📍 <b>Punto:</b> {info_b['zona']}</p>
                            <div class="articulos-box-shein">{info_b['articulos']}</div>
                        </div>
                """, unsafe_allow_html=True)
                
                # Renderizar imágenes directamente desde sus URLs de ImgBB
                if info_b.get("imagenes_links"):
                    st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
                    cols_img = st.columns(4)
                    for idx_img, link_url in enumerate(info_b["imagenes_links"][:4]):
                        with cols_img[idx_img % 4]:
                            st.image(link_url, use_container_width=True)
                
                st.markdown(f"""
                        <div style="margin-top: 15px;">
                            <a href="{url_wa_vendedor}" target="_blank"><button style="background-color:#E6005C; color:white; border:none; padding:10px; border-radius:8px; width:100%; font-weight:bold; cursor:pointer;">💬 Contactar por WhatsApp</button></a>
                        </div>
                    </div><br>
                """, unsafe_allow_html=True)

# ==========================================
# TAB 2: REGISTRO DE VENDEDORAS (ILIMITADO)
# ==========================================
with tab_anunciarse:
    st.subheader("💜 Crea tu Espacio en el Bazar")
    
    with st.form("form_anuncio", clear_on_submit=True):
        nombre_vendedor = st.text_input("Nombre de tu Tienda / Vendedora *")
        whatsapp_vendedor = st.text_input("WhatsApp (10 dígitos, ej: 81XXXXXXXX) *")
        zona_entrega = st.text_input("Punto Seguro de Entrega (Ej: Metro Cuauhtémoc) *")
        tipo_articulo = st.radio("Categoría principal: *", ["K-Pop (Photocards/Coleccionables)", "Mi Clóset (Ropa/Accesorios)"])
        lista_articulos = st.text_area("Lista tus productos con precio (Uno por renglón): *")
        
        st.markdown("📸 **Sube las fotos de tus artículos (Hasta 15 fotos):**")
        fotos_articulos = st.file_uploader("Puedes seleccionar varias fotos a la vez:", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
        
        st.markdown("### 💳 Validación de Seguridad ($25 MXN)")
        st.markdown('<div style="background-color: #FFF; padding: 15px; border: 2px solid #D81159; border-radius:10px; margin-bottom:15px;"><b>🏛️ NU MÉXICO</b><br>🔑 CLABE: 0123 4567 8901 2345 67<br>👤 TITULAR: YAJAIRA LEIJA</div>', unsafe_allow_html=True)
        comprobante = st.file_uploader("Sube la captura de tu pago: *", type=["jpg", "png", "jpeg"])
        
        enviar_anuncio = st.form_submit_button("🚀 Subir y Registrar Bloque")

        if enviar_anuncio:
            if not (nombre_vendedor and whatsapp_vendedor and zona_entrega and lista_articulos and comprobante):
                st.error("Por favor, rellena todos los campos obligatorios marcados con *")
            else:
                with st.spinner("Subiendo imágenes a la nube de forma segura... Esto evita que la app se trabe ✨"):
                    # 1. Subir fotos de productos a ImgBB
                    links_fotos_subidas = []
                    if fotos_articulos:
                        for foto in fotos_articulos:
                            url_subida = subir_a_imgbb(foto)
                            if url_subida:
                                links_fotos_subidas.append(url_subida)
                    
                    # 2. Subir comprobante a ImgBB
                    url_comprobante = subir_a_imgbb(comprobante)
                    
                    # 3. Armar objeto final
                    id_transaccion = f"BZR-{datetime.now().strftime('%d%H%M%S')}"
                    info_b = {
                        "vendedor": nombre_vendedor,
                        "whatsapp": whatsapp_vendedor,
                        "zona": zona_entrega,
                        "categoria": tipo_articulo,
                        "articulos": lista_articulos,
                        "estado": "⏳ En espera de verificación",
                        "fecha": datetime.now().strftime("%d/%m/%Y"),
                        "imagenes_links": links_fotos_subidas,
                        "comprobante_link": url_comprobante if url_comprobante else ""
                    }
                    
                    # Guardar localmente y escribir enlaces limpios en Google Sheets
                    st.session_state.bloques_db[id_transaccion] = info_b
                    guardar_en_sheets(id_transaccion, info_b)
                    
                    st.success(f"🎉 ¡Bloque registrado exitosamente con ID: {id_transaccion}!")
                    
                    # Crear link de confirmación automático para la vendedora
                    msg_wa = f"Hola, mandé registro de Bazar.\n👤 Vendedora: {nombre_vendedor}\n🆔 ID: {id_transaccion}"
                    url_confirmacion = f"https://wa.me/528143029578?text={msg_wa.replace(' ', '%20')}"
                    st.markdown(f'<br><a class="btn-wa-nativo" href="{url_confirmacion}" target="_blank">📲 CLIC AQUÍ PARA CONFIRMAR TU COMPROBANTE</a>', unsafe_allow_html=True)

# ==========================================
# TAB 3: PANEL DE CONTROL DE ADMINISTRADORA
# ==========================================
with tab_admin:
    clave_ingresada = st.text_input("Contraseña de Administradora:", type="password")
    if clave_ingresada == CONTRASENA_ADMIN:
        st.success("Acceso Autorizado, Capitana.")
        
        if not st.session_state.bloques_db:
            st.info("No hay registros en la base de datos.")
            
        for b_id in list(st.session_state.bloques_db.keys()):
            b_info = st.session_state.bloques_db[b_id]
            st.markdown(f"""
                <div class="admin-box">
                    🆔 <b>ID:</b> <code>{b_id}</code> | 👤 <b>Vendedora:</b> {b_info["vendedor"]} | 📱 <b>WA:</b> {b_info["whatsapp"]}<br>
                    📍 <b>Zona:</b> {b_info["zona"]} | 📅 <b>Fecha:</b> {b_info["fecha"]}<br>
                    📋 <b>Estado Actual:</b> <code>{b_info["estado"]}</code>
                </div>
            """, unsafe_allow_html=True)
            
            # Mostrar imágenes cargadas desde los enlaces web estables
            if b_info.get("imagenes_links"):
                st.write("📸 Fotos del Producto:")
                cols_adm = st.columns(6)
                for i_l, link_l in enumerate(b_info["imagenes_links"]):
                    with cols_adm[i_l % 6]:
                        st.image(link_l, use_container_width=True)
            
            # Mostrar comprobante de pago
            if b_info.get("comprobante_link"):
                st.markdown(f"💳 [Ver Captura del Comprobante de Pago de $25 MXN]({b_info['comprobante_link']})")
            
            # Botones de Acción directos
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if "espera" in str(b_info['estado']).lower():
                    if st.button("🟢 Aprobar e Ir al Escaparate", key=f"app_{b_id}"):
                        st.session_state.bloques_db[b_id]['estado'] = "🟢 ACTIVO"
                        guardar_en_sheets(b_id, st.session_state.bloques_db[b_id])
                        st.rerun()
            with col_b2:
                if st.button("🗑️ Eliminar Registro Completo", key=f"del_{b_id}"):
                    if b_id in st.session_state.bloques_db:
                        del st.session_state.bloques_db[b_id]
                    eliminar_de_sheets(b_id)
                    st.rerun()
            st.markdown("<hr>", unsafe_allow_html=True)

st.markdown('<div class="seccion-quejas">Soporte y aclaraciones técnico del sistema: 8143029578</div>', unsafe_allow_html=True)
