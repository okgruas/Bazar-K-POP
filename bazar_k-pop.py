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

# ⚠️ CONFIGURACIÓN DE ADMINISTRADOR ⚠️
TELEFONO_ADMIN_WHATSAPP = "528143029578"
CONTRASENA_ADMIN = "bazar123"
URL_HOJA_CALCULO = "https://docs.google.com/spreadsheets/d/1uj8Vkw3uQn5GYy7LD7ADwXH3mtpvpZu2vQtiZ33yCXQ/edit?usp=sharing"

# 🔥 TU LLAVE DE IMGBB INTEGRADA 🔥
IMGBB_API_KEY = "c72da82c65cce967aac091defc1f41dd"

# --- CONEXIÓN DIRECTA A GOOGLE SHEETS ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Forzamos ttl=0 para que siempre traiga lo más nuevo al recargar la página
    df_sheets = conn.read(spreadsheet=URL_HOJA_CALCULO, ttl=0).dropna(how="all")
except Exception as e:
    df_sheets = pd.DataFrame(columns=["id", "vendedor", "whatsapp", "zona", "categoria", "articulos", "estado", "fecha", "fotos_links", "comprobante_link"])

# --- FUNCIÓN PARA CONVERTIR IMÁGENES EN ENLACES WEB ---
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

# --- SINCRONIZACIÓN DE BASE DE DATOS ULTRA RESISTENTE AL INICIAR ---
if "bloques_db" not in st.session_state:
    st.session_state.bloques_db = {}

# Limpiamos y aseguramos que el DataFrame tenga los nombres de columnas correctos
df_sheets.columns = [c.strip() for c in df_sheets.columns]

for _, row in df_sheets.iterrows():
    try:
        b_id = str(row["id"]).strip()
        if not b_id or b_id == "nan":
            continue
            
        # Validar los links de fotos de manera mega segura
        links_fotos = []
        if "fotos_links" in row and pd.notna(row["fotos_links"]):
            links_fotos = [l.strip() for l in str(row["fotos_links"]).split(",") if l.strip()]
            
        comp_link = ""
        if "comprobante_link" in row and pd.notna(row["comprobante_link"]):
            comp_link = str(row["comprobante_link"]).strip()

        st.session_state.bloques_db[b_id] = {
            "vendedor": str(row.get("vendedor", "Anónimo")),
            "whatsapp": str(row.get("whatsapp", "")),
            "zona": str(row.get("zona", "")),
            "categoria": str(row.get("categoria", "")),
            "articulos": str(row.get("articulos", "")),
            "estado": str(row.get("estado", "⏳ En espera de verificación")),
            "fecha": str(row.get("fecha", "")),
            "imagenes": links_fotos,  
            "comprobante_link": comp_link
        }
    except Exception as e:
        # Si una fila está rota, que no rompa la lectura de las demás
        continue

# --- FUNCIÓN PARA GUARDAR O ACTUALIZAR EN GOOGLE SHEETS ---
def guardar_en_sheets(id_b, info_b):
    try:
        # Volver a leer la nube actual sin caché para evitar sobreescrituras accidentales
        df_actual = conn.read(spreadsheet=URL_HOJA_CALCULO, ttl=0).dropna(how="all")
        df_actual.columns = [c.strip() for c in df_actual.columns]
        
        # Eliminar el registro viejo si ya existe en la tabla para actualizarlo limpiamente
        if not df_actual.empty and "id" in df_actual.columns:
            df_actual = df_actual[df_actual["id"].astype(str).str.strip() != str(id_b).strip()]
        
        # Procesar imágenes (Convertir archivos binarios de Streamlit a links HTTPS reales)
        lista_links = []
        for img in info_b.get("imagenes", []):
            if isinstance(img, str):
                if img.startswith("http"):
                    lista_links.append(img)
            else:
                link_subido = subir_a_imgbb(img)
                if link_subido:
                    lista_links.append(link_subido)

        url_comp = info_b.get("comprobante_link", "")
        if url_comp and not isinstance(url_comp, str):
            url_comp = subir_a_imgbb(url_comp) or ""

        # Crear la nueva fila armada de forma idéntica a tu Sheets
        nuevo_registro = pd.DataFrame([{
            "id": str(id_b),
            "vendedor": str(info_b["vendedor"]),
            "whatsapp": str(info_b["whatsapp"]),
            "zona": str(info_b["zona"]),
            "categoria": str(info_b["categoria"]),
            "articulos": str(info_b["articulos"]),
            "estado": str(info_b["estado"]),
            "fecha": str(info_b["fecha"]),
            "fotos_links": ",".join(lista_links),
            "comprobante_link": str(url_comp)
        }])
        
        # Combinar y mandar directamente a la API de Google Sheets
        df_actual = pd.concat([df_actual, nuevo_registro], ignore_index=True)
        conn.update(spreadsheet=URL_HOJA_CALCULO, data=df_actual)
        
        # Refrescar nuestra memoria local para que se muestre al instante
        st.session_state.bloques_db[id_b]["imagenes"] = lista_links
        st.session_state.bloques_db[id_b]["comprobante_link"] = url_comp
    except Exception as e:
        st.error(f"Error al conectar con Google Sheets: {e}")

# --- ESTILOS CSS REFORZADOS (TU DISEÑO ORIGINAL EXACTO) ---
st.markdown("""
    <style>
    /* Fondo general */
    .stApp {
        background: linear-gradient(135deg, #FFE5EC 0%, #FFB3C6 40%, #FF477E 100%);
    }
    
    /* Contenedores blancos generales y tarjetas estilo Shein */
    .stForm, .preview-container, .public-block, .admin-box {
        background-color: rgba(255, 255, 255, 0.98) !important;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.15);
        margin-bottom: 25px;
    }
    
    /* Tarjeta compacta específica para el diseño de cuadritos */
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
    
    /* Forzar títulos y etiquetas generales en negro */
    label, p, span, .stRadio p, h1, h2, h3, div[data-testid="stMarkdownContainer"] p {
        color: #1A1A1A !important;
        font-weight: bold !important;
    }
    
    /* Arreglo de texto en los campos de escritura y forzar cursor (caret) negro */
    textarea, input[type="text"], div[data-testid="stTextArea"] textarea, div[data-testid="stTextInput"] input {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        border: 2px solid #FF477E !important;
        -webkit-text-fill-color: #1A1A1A !important;
        caret-color: #1A1A1A !important;
    }
    
    /* Marcador de posición (placeholder) tenue */
    textarea::placeholder, div[data-testid="stTextArea"] textarea::placeholder {
        color: #888888 !important;
        -webkit-text-fill-color: #888888 !important;
        font-weight: normal !important;
        opacity: 0.7 !important;
    }
    
    /* Cargar imagen en Rosa Pastel */
    div[data-testid="stFileUploader"] section {
        background-color: #FFF0F5 !important;
        border: 2px dashed #E6005C !important;
        border-radius: 10px !important;
    }
    div[data-testid="stFileUploader"] section * {
        color: #1A1A1A !important;
        -webkit-text-fill-color: #1A1A1A !important;
    }
    div[data-testid="stFileUploader"] button {
        background-color: #E6005C !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
    }
    div[data-testid="stFileUploader"] button * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    
    /* Botón "SUBIR BLOQUE DE ANUNCIOS" en Fucsia brillante */
    div[data-testid="stFormSubmitButton"] button, .stSubmitButton button, div.stSubmitButton > button {
        background-color: #E6005C !important;
        color: #FFFFFF !important;
        border: 2px solid #FFFFFF !important;
        border-radius: 10px !important;
        padding: 14px 28px !important;
        width: 100% !important;
        box-shadow: 0px 6px 15px rgba(230, 0, 92, 0.4) !important;
        opacity: 1 !important;
    }
    div[data-testid="stFormSubmitButton"] button *, .stSubmitButton button *, div.stSubmitButton > button * {
        color: #FFFFFF !important;
        font-size: 20px !important;
        font-weight: 900 !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    
    /* Botones del Administrador (Rosas) */
    div[data-testid="stHorizontalBlock"] button, div[data-testid="element-container"] button {
        background-color: #E6005C !important;
        color: #FFFFFF !important;
        border: 1px solid #FFFFFF !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }
    div[data-testid="stHorizontalBlock"] button *, div[data-testid="element-container"] button * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    /* BOTÓN DE ACCIÓN (Verde, grande) */
    div.stButton > button {
        background-color: #25D366 !important;
        color: #1A1A1A !important;
        border: 2px solid #FFFFFF !important;
        border-radius: 12px !important;
        padding: 16px 32px !important;
        width: 100% !important;
        box-shadow: 0px 6px 18px rgba(37, 211, 102, 0.4) !important;
    }
    div.stButton > button * {
        color: #1A1A1A !important;
        font-size: 19px !important;
        font-weight: 900 !important;
        -webkit-text-fill-color: #1A1A1A !important;
    }
    div.stButton > button:hover {
        background-color: #20BA56 !important;
    }
    
    /* Fotos miniatura controladas estilo catálogo */
    .mini-foto img {
        max-height: 100px !important;
        object-fit: contain !important;
        border-radius: 6px;
        border: 1px solid #FFB3C6;
    }
    
    /* Caja de artículos adaptada a tarjeta pequeña */
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
    
    /* Botón HTML nativo para apertura forzada en pestaña nueva */
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
    .btn-wa-nativo:hover {
        background-color: #20BA56 !important;
        color: #1A1A1A !important;
    }

    .seccion-quejas {
        text-align: center;
        font-size: 11px !important;
        color: #666666 !important;
        margin-top: 20px;
        font-weight: normal !important;
    }

    /* Estilo para el contenedor de la advertencia de seguridad superior */
    .alerta-seguridad-principal {
        background-color: #FFF3CD !important;
        color: #856404 !important;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.05);
        margin-bottom: 25px;
        border-left: 6px solid #FFC107;
    }
    .alerta-seguridad-principal p {
        color: #856404 !important;
        font-size: 14px !important;
        font-weight: normal !important;
        margin: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown('<div style="text-align:center; font-size:42px; font-weight:900; color:#D81159; text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.4);">✨ BAZAR DIGITAL DE K-POP & CLÓSET ✨</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center; font-size:18px; color:white; font-weight:bold; margin-bottom:25px;">🛍️ Photocards, Coleccionables & Moda • Monterrey</div>', unsafe_allow_html=True)

# --- PESTAÑAS PRINCIPALES ---
tab_bazar, tab_anunciarse, tab_admin = st.tabs(["🛍️ Ver el Bazar / Clóset", "💜 Registrarse como Vendedora", "🔐 Panel de Control (Solo Admin)"])

# ==========================================
# PESTAÑA 1: EL ESCAPARATE PÚBLICO (DISEÑO GRID ESTILO SHEIN)
# ==========================================
with tab_bazar:
    st.markdown("""
        <div class="alerta-seguridad-principal">
            <p>
                ⚠️ <b>Aviso de Seguridad:</b> Recuerda realizar tus entregas únicamente en <b>lugares públicos y concurridos</b>. 
                Cada vendedora se hace completamente responsable de sus artículos, precios, acuerdos de entrega y citas correspondientes. 
                Este espacio funciona únicamente como catálogo digital, por lo que toda transacción y trato es totalmente ajeno a la aplicación.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("🛒 Clósets y Productos Disponibles")
    bloques_activos = {k: v for k, v in st.session_state.bloques_db.items() if "ACTIVO" in str(v['estado'])}
    
    if not bloques_activos:
        st.info("No hay tienditas activas en este momento. Las publicaciones aprobadas aparecerán aquí de inmediato.")
    else:
        lista_bloques = list(bloques_activos.items())
        columnas_por_fila = 3
        
        for i in range(0, len(lista_bloques), columnas_por_fila):
            fila_bloques = lista_bloques[i:i+columnas_por_fila]
            cols = st.columns(columnas_por_fila)
            
            for idx_col, (id_b, info_b) in enumerate(fila_bloques):
                with cols[idx_col]:
                    texto_mensaje = "Hola, vengo del bazar digital de k-pop, me interesó alguno de tus artículos. ✨🛍️"
                    texto_codificado = texto_mensaje.replace(' ', '%20').replace('\n', '%0A')
                    url_wa_vendedor = f"https://wa.me/{info_b['whatsapp']}?text={texto_codificado}"

                    st.markdown(f"""
                        <div class="shein-card">
                            <div>
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                    <span class="badge-activo-shein">🟢 ACTIVO</span>
                                    <span style="font-size: 11px; color: #666666;">📅 {info_b['fecha']}</span>
                                </div>
                                <h4 style="margin: 0 0 5px 0; color:#D81159; font-size: 18px;">🛍️ Bazar de {info_b['vendedor']}</h4>
                                <p style="margin: 2px 0; color:#555555; font-size: 12px;">📂 <b>Categoría:</b> {info_b['categoria']}</p>
                                <p style="margin: 2px 0; color:#555555; font-size: 12px; margin-bottom: 10px;">📍 <b>Punto:</b> {info_b['zona']}</p>
                                <div class="articulos-box-shein">{info_b['articulos']}</div>
                            </div>
                    """, unsafe_allow_html=True)
                    
                    if info_b.get('imagenes'):
                        st.markdown("<span style='font-size:12px; color:#1A1A1A;'>📸 Fotos:</span>", unsafe_allow_html=True)
                        cols_img = st.columns(4)
                        for idx_img, img_file in enumerate(info_b['imagenes'][:4]):
                            with cols_img[idx_img % 4]:
                                st.markdown('<div class="mini-foto">', unsafe_allow_html=True)
                                st.image(img_file, use_container_width=True)
                                st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown(f"""
                            <div style="margin-top: 15px;">
                                <a href="{url_wa_vendedor}" target="_blank" style="text-decoration: none;">
                                    <button style="background-color:#E6005C; color:white; border:none; padding:10px 15px; font-weight:bold; border-radius:8px; cursor:pointer; width:100%; font-size:13px;">
                                        💬 Contactar por WhatsApp
                                    </button>
                                </a>
                                <div style="text-align: center; color: #D81159; font-weight: bold; font-size: 12px; margin-top: 8px; margin-bottom: 8px;">
                                    ✨ ¡Gracias por tu preferencia! ✨
                                </div>
                                <hr style="border: 0; height: 5px; background-color: #E6005C; margin: 0; border-radius: 5px;">
                            </div>
                        </div>
                        <br>
                    """, unsafe_allow_html=True)

# ==========================================
# PESTAÑA 2: REGISTRO DE VENDEDORAS
# ==========================================
with tab_anunciarse:
    st.subheader("💜 Registra tu Bloque de Anuncios")
    st.write("Costo por bloque: **$25 MXN** con una vigencia automática de 15 días.")
    
    if "pre_registro" not in st.session_state:
        st.session_state.pre_registro = None
    if "enviado_ok" not in st.session_state:
        st.session_state.enviado_ok = False

    with st.form("form_anuncio", clear_on_submit=True):
        st.markdown("### 👤 1. Datos de Contacto")
        col1, col2 = st.columns(2)
        with col1:
            nombre_vendedor = st.text_input("Nombre / Tienda *")
            whatsapp_vendedor = st.text_input("WhatsApp de Contacto * (10 dígitos)")
        with col2:
            zona_entrega = st.text_input("Punto Seguro de Entrega * (ej. Metro Cuauhtémoc)")
            tipo_articulo = st.radio("Categoría: *", ["K-Pop (Photocards/Coleccionables)", "Mi Clóset (Ropa/Accesorios)"])
            
        st.markdown("---")
        st.markdown("### 🛍️ 2. Tus Artículos y Precios")
        lista_articulos = st.text_area(
            "Lista tus productos (Uno por renglón, con precio) *", 
            placeholder="Ejemplo:\n- Blusa Azul Talla XL - $150\n- Photocard Seungmin ODDINARY - $120"
        )
        
        st.markdown("### 📸 3. Fotos de tus Artículos (Máximo 15)")
        fotos_articulos = st.file_uploader("Selecciona tus imágenes:", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
        
        st.markdown("---")
        st.markdown("### 💳 4. Pago de Validation ($25 MXN)")
        st.markdown("""
            <div style="background-color: #FFFFFF; padding: 20px; border-radius: 10px; border: 2px solid #D81159;">
                <p style="color: #D81159 !important; font-size: 17px !important; margin: 0 0 5px 0; font-weight: 900;">🏛️ BANCO: NU MÉXICO</p>
                <p style="color: #1A1A1A !important; font-size: 17px !important; margin: 0 0 5px 0; font-family: monospace; font-weight: bold;">🔑 CLABE: 0123 4567 8901 2345 67</p>
                <p style="color: #1A1A1A !important; font-size: 17px !important; margin: 0; font-weight: bold;">👤 TITULAR: RAQUEL COVARRUBIAS</p>
            </div>
        """, unsafe_allow_html=True)
        st.write("")
        comprobante = st.file_uploader("Sube la foto de tu comprobante de transferencia *", type=["jpg", "png", "jpeg"])
        
        enviar_anuncio = st.form_submit_button("Subir Bloque de Anuncios para Validación")

        if enviar_anuncio:
            if fotos_articulos and len(fotos_articulos) > 15:
                st.error("No puedes subir más de 15 fotos.")
            elif not (nombre_vendedor and whatsapp_vendedor and zona_entrega and lista_articulos and comprobante):
                st.error("Por favor, llena todos los campos obligatorios (*) y carga tu comprobante.")
            else:
                id_transaccion = f"BZR-{datetime.now().strftime('%d%H%M%S')}"
                st.session_state.pre_registro = {
                    "id": id_transaccion,
                    "vendedor": nombre_vendedor,
                    "whatsapp": whatsapp_vendedor,
                    "zona": zona_entrega,
                    "categoria": tipo_articulo,
                    "articulos": lista_articulos,
                    "imagenes": fotos_articulos, 
                    "comprobante_link": comprobante, 
                    "estado": "⏳ En espera de verificación",
                    "fecha": datetime.now().strftime("%d/%m/%Y")
                }
                st.session_state.enviado_ok = False

    if st.session_state.pre_registro is not None:
        datos = st.session_state.pre_registro
        id_b = datos["id"]
        
        if id_b in st.session_state.bloques_db and "ACTIVO" in str(st.session_state.bloques_db[id_b]['estado']):
            st.session_state.pre_registro = None
            st.session_state.enviado_ok = False
            st.rerun()
        else:
            st.markdown('<div class="preview-container">', unsafe_allow_html=True)
            st.warning("⏳ Tu registro está en proceso de revisión. Por favor, realiza el paso final de WhatsApp en la parte de abajo.")
            
            st.markdown("### 👀 Detalles de tu Solicitud")
            col_p1, col_p2 = st.columns([1, 2])
            with col_p1:
                st.metric(label="Monto por Validar", value="$25 MXN")
                st.write(f"🆔 **ID Asignado:** `{id_b}`")
            with col_p2:
                st.write(f"👤 **Vendedora:** {datos['vendedor']}")
                st.write(f"📍 **Punto Seguro:** {datos['zona']}")
                st.write("**📝 Lista enviada:**")
                st.markdown(f'<div class="articulos-box-shein">{datos["articulos"]}</div>', unsafe_allow_html=True)
            
            if datos["imagenes"]:
                st.write("**📸 Imágenes cargadas con éxito:**")
                cols_prev = st.columns(6)
                for i, img in enumerate(datos["imagenes"]):
                    with cols_prev[i % 6]:
                        st.markdown('<div class="mini-foto">', unsafe_allow_html=True)
                        st.image(img, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### 📲 ¡Paso Final Obligatorio!")
            
            msg = (
                f"Hola, vengo de la página del Bazar.\n\n"
                f"👤 *Vendedora:* {datos['vendedor']}\n"
                f"🆔 *ID de Registro:* {id_b}\n\n"
                f"📎 *(Por favor, adjunta aquí la foto de tu comprobante antes de enviar el mensaje)*"
            )
            msg_encoded = msg.replace(' ', '%20').replace('\n', '%0A')
            url_wa = f"https://wa.me/528143029578?text={msg_encoded}"
            
            if not st.session_state.enviado_ok:
                if st.button("📲 Click Para Registrar y Preparar Envío de WhatsApp", key="btn_disparador_wa"):
                    with st.spinner("Guardando en la nube de forma segura... ✨"):
                        # Registramos localmente
                        st.session_state.bloques_db[id_b] = datos
                        # Forzamos la subida a ImgBB y escritura instantánea en Google Sheets
                        guardar_en_sheets(id_b, datos)
                        st.session_state.enviado_ok = True
                        st.rerun()
            else:
                st.success("✅ ¡Datos registrados con éxito en el panel de administración!")
                st.markdown(f"""
                    <a class="btn-wa-nativo" href="{url_wa}" target="_blank">
                        🚀 ¡TODO LISTO! CLIC AQUÍ PARA CONFIRMAR TU PAGO VÍA WHATSAPP
                    </a>
                """, unsafe_allow_html=True)
                st.info("Al dar clic arriba se abrirá el chat. No olvides adjuntar foto del comprobante.")
                
            st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 🔐 PESTAÑA 3: PANEL DE CONTROL DE ADMINISTRADORA
# ==========================================
with tab_admin:
    st.subheader("🔐 Consola de Verificación")
    clave_ingresada = st.text_input("Introduce la Contraseña de Administradora:", type="password", key="tab_admin_key")
    
    if clave_ingresada == CONTRASENA_ADMIN:
        st.success("Acceso Autorizado - Modo Gestor")
        st.markdown("### 🛠️ Solicitudes del Sistema")
        
        if not st.session_state.bloques_db:
            st.info("No hay bloques registrados actualmente esperando acción en el sistema.")
        else:
            for b_id in list(st.session_state.bloques_db.keys()):
                b_info = st.session_state.bloques_db[b_id]
                
                st.markdown(f"""
                    <div class="admin-box">
                        <span style="color:#D81159;"><b>ID Solicitud:</b> {b_id}</span><br>
                        <b>Vendedora:</b> {b_info['vendedor']} | <b>Celular:</b> {b_info['whatsapp']}<br>
                        <b>Estado Actual:</b> <code>{b_info['estado']}</code>
                    </div>
                """, unsafe_allow_html=True)
                
                if b_info.get('imagenes'):
                    st.markdown("**📸 Fotos adjuntas por la vendedora:**")
                    cols_admin_img = st.columns(6)
                    for idx, img_obj in enumerate(b_info['imagenes']):
                        with cols_admin_img[idx % 6]:
                            st.markdown('<div class="mini-foto">', unsafe_allow_html=True)
                            st.image(img_obj, use_container_width=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                
                if b_info.get("comprobante_link") and isinstance(b_info["comprobante_link"], str) and b_info["comprobante_link"].startswith("http"):
                    st.markdown(f'<a href="{b_info["comprobante_link"]}" target="_blank" style="color: #E6005C; font-weight: bold;">👁️ Ver Comprobante de Pago en Grande</a>', unsafe_allow_html=True)
                
                if "espera" in str(b_info['estado']).lower():
                    if st.button("🟢 Aceptar Bloque", key=f"tab_acc_{b_id}"):
                        st.session_state.bloques_db[b_id]['estado'] = "🟢 ACTIVO"
                        guardar_en_sheets(b_id, st.session_state.bloques_db[b_id])
                        st.toast(f"¡Bloque {b_id} activado con éxito!")
                        st.rerun()
                
                nuevo_texto = st.text_area(f"Modificar artículos de {b_id}:", value=b_info['articulos'], key=f"tab_edit_{b_id}")
                if nuevo_texto != b_info['articulos']:
                    st.session_state.bloques_db[b_id]['articulos'] = nuevo_texto
                    guardar_en_sheets(b_id, st.session_state.bloques_db[b_id])
                
                if st.button(f"🗑️ Eliminar permanentemente {b_id}", key=f"tab_del_{b_id}"):
                    if b_id in st.session_state.bloques_db:
                        del st.session_state.bloques_db[b_id]
                    try:
                        df_actual = conn.read(spreadsheet=URL_HOJA_CALCULO, ttl=0).dropna(how="all")
                        df_actual.columns = [c.strip() for c in df_actual.columns]
                        df_actual = df_actual[df_actual["id"].astype(str).str.strip() != str(b_id).strip()]
                        conn.update(spreadsheet=URL_HOJA_CALCULO, data=df_actual)
                    except:
                        pass
                    st.rerun()
                st.markdown("---")

st.markdown('<div class="seccion-quejas">Quejas, sugerencias y aclaraciones, con Capitana Albatros: 8143029578</div>', unsafe_allow_html=True)
