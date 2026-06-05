import streamlit as st
from datetime import datetime
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

# 🔥 TU LLAVE DE IMGBB INTEGRADA 🔥
IMGBB_API_KEY = "c72da82c65cce967aac091defc1f41dd"

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

# =========================================================================
# 📦 TU BASE DE DATOS FIJA Y PERMANENTE (Estilo tus catálogos anteriores)
# Aquí puedes agregar, editar o activar manualmente las tienditas directamente en el código.
# Si quieres activar una nueva vendedora, solo cambia su estado a "🟢 ACTIVO".
# =========================================================================
if "bloques_db" not in st.session_state:
    st.session_state.bloques_db = {
        "BZR-01": {
            "vendedor": "Yajaira Leija",
            "whatsapp": "528143029578",
            "zona": "Metro Cuauhtémoc / Centro de Monterrey",
            "categoria": "K-Pop (Photocards/Coleccionables)",
            "articulos": "- Photocard Seungmin ODDINARY (Perfecto Estado) - $150\n- Álbum Stray Kids 5-STAR (Sin PC) - $250\n- Mini Banner Stray Kids Oficial - $100",
            "estado": "🟢 ACTIVO",
            "fecha": "05/06/2026",
            "imagenes": [
                "https://i.ibb.co/6wXb7Y0/sample-skz1.jpg",
                "https://i.ibb.co/4p3L8X1/sample-skz2.jpg"
            ],
            "comprobante_link": ""
        },
        "BZR-02": {
            "vendedor": "Julieta Moda",
            "whatsapp": "528143029578",
            "zona": "Plaza Fiesta San Agustín",
            "categoria": "Mi Clóset (Ropa/Accesorios)",
            "articulos": "- Blusa Rosa Pastel Estilo Shein (Talla M) - $120\n- Vestido Coreano Denim (Talla S, Nuevo) - $300\n- Gorro de Invierno Blanco K-Pop - $90",
            "estado": "🟢 ACTIVO",
            "fecha": "05/06/2026",
            "imagenes": [
                "https://i.ibb.co/2sn7X9M/sample-closet1.jpg"
            ],
            "comprobante_link": ""
        }
    }

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
        st.info("No hay tienditas activas en este momento.")
    else:
        lista_bloques = list(bloques_activos.items())
        columnas_por_fila = 3
        
        for i in range(0, len(lista_bloques), columnas_por_fila):
            fila_bloques = lista_bloques[i:i+columnas_por_fila]
            cols = st.columns(columnas_por_fila)
            
            for idx_col, (id_b, info_b) in enumerate(fila_bloques):
                with cols[idx_col]:
                    texto_mensaje = f"Hola, vengo del Bazar Digital. Me interesaron tus artículos del bloque {id_b}. ✨🛍️"
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
        
        st.markdown("### 📸 3. Fotos de tus Artículos (Anexa links de fotos de ImgBB, Facebook o Pinterest o súbelas aquí)")
        fotos_articulos = st.file_uploader("Selecciona tus imágenes:", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
        
        st.markdown("---")
        st.markdown("### 💳 4. Pago de Validación ($25 MXN)")
        st.markdown("""
            <div style="background-color: #FFFFFF; padding: 20px; border-radius: 10px; border: 2px solid #D81159;">
                <p style="color: #D81159 !important; font-size: 17px !important; margin: 0 0 5px 0; font-weight: 900;">🏛️ BANCO: NU MÉXICO</p>
                <p style="color: #1A1A1A !important; font-size: 17px !important; margin: 0 0 5px 0; font-family: monospace; font-weight: bold;">🔑 CLABE: 0123 4567 8901 2345 67</p>
                <p style="color: #1A1A1A !important; font-size: 17px !important; margin: 0; font-weight: bold;">👤 TITULAR: CAPITANA ALBATROS</p>
            </div>
        """, unsafe_allow_html=True)
        st.write("")
        
        enviar_anuncio = st.form_submit_button("Subir Bloque de Anuncios para Validación")

        if enviar_anuncio:
            if not (nombre_vendedor and whatsapp_vendedor and zona_entrega and lista_articulos):
                st.error("Por favor, llena todos los campos obligatorios (*).")
            else:
                id_transaccion = f"BZR-{datetime.now().strftime('%d%H%M%S')}"
                
                # Convertir imágenes cargadas a links en la nube al instante
                links_subidos = []
                if fotos_articulos:
                    with st.spinner("Subiendo imágenes a la nube de forma segura... ✨"):
                        for f in fotos_articulos:
                            url_i = subir_a_imgbb(f)
                            if url_i:
                                links_subidos.append(url_i)

                st.session_state.pre_registro = {
                    "id": id_transaccion,
                    "vendedor": nombre_vendedor,
                    "whatsapp": whatsapp_vendedor,
                    "zona": zona_entrega,
                    "categoria": tipo_articulo,
                    "articulos": lista_articulos,
                    "imagenes": links_subidos, 
                    "estado": "⏳ En espera de verificación",
                    "fecha": datetime.now().strftime("%d/%m/%Y")
                }
                st.session_state.enviado_ok = False

    if st.session_state.pre_registro is not None:
        datos = st.session_state.pre_registro
        id_b = datos["id"]
        
        st.markdown('<div class="preview-container">', unsafe_allow_html=True)
        st.warning("⏳ Tu registro se procesó en el navegador. Realiza el paso final de WhatsApp para guardarlo permanentemente en el sistema.")
        
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
            st.write("**📸 Enlaces de tus imágenes generadas:**")
            for lk in datos["imagenes"]:
                st.code(lk)
        
        st.markdown("---")
        st.markdown("### 📲 ¡Paso Final Obligatorio!")
        
        # Formateamos el mensaje de WhatsApp incluyendo los links de las fotos para que tú los tengas completos
        links_texto = "\n".join(datos["imagenes"])
        msg = (
            f"Hola Capitana Albatros, vengo de la página del Bazar.\n\n"
            f"👤 *Vendedora:* {datos['vendedor']}\n"
            f"🆔 *ID de Registro:* {id_b}\n"
            f"📍 *Punto:* {datos['zona']}\n"
            f"📂 *Categoría:* {datos['categoria']}\n"
            f"📝 *Artículos:*\n{datos['articulos']}\n\n"
            f"📸 *Links de Fotos:*\n{links_texto}\n\n"
            f"📎 *(Aquí adjunto mi captura de pantalla del pago)*"
        )
        msg_encoded = msg.replace(' ', '%20').replace('\n', '%0A')
        url_wa = f"https://wa.me/528143029578?text={msg_encoded}"
        
        if not st.session_state.enviado_ok:
            if st.button("📲 Click Para Registrar y Preparar Mensaje de WhatsApp", key="btn_disparador_wa"):
                # Se guarda en la memoria temporal activa de la sesión corriente
                st.session_state.bloques_db[id_b] = datos
                st.session_state.enviado_ok = True
                st.rerun()
        else:
            st.success("✅ ¡Datos procesados con éxito!")
            st.markdown(f"""
                <a class="btn-wa-nativo" href="{url_wa}" target="_blank">
                    🚀 ¡TODO LISTO! CLIC AQUÍ PARA MANDAR ANUNCIO Y COMPROBANTE POR WHATSAPP
                </a>
            """, unsafe_allow_html=True)
            st.info("Al dar clic arriba se abrirá tu WhatsApp con toda la información armada incluyendo los links de las imágenes. Solo dale enviar y adjunta tu comprobante.")
            
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 🔐 PESTAÑA 3: PANEL DE CONTROL DE ADMINISTRADORA
# ==========================================
with tab_admin:
    st.subheader("🔐 Consola de Verificación Local")
    clave_ingresada = st.text_input("Introduce la Contraseña de Administradora:", type="password", key="tab_admin_key")
    
    if clave_ingresada == CONTRASENA_ADMIN:
        st.success("Acceso Autorizado - Modo Catálogo")
        st.info("💡 Consejo de Capitana Albatros: Para hacer un bloque permanente (que nunca se borre al picar la rueda), copia el bloque de texto que te llega a WhatsApp y pégalo directamente en la sección 'bloques_db' en tu GitHub.")
        
        st.markdown("### 🛠️ Solicitudes en Memoria Activa")
        
        for b_id in list(st.session_state.bloques_db.keys()):
            b_info = st.session_state.bloques_db[b_id]
            
            st.markdown(f"""
                <div class="admin-box">
                    <span style="color:#D81159;"><b>ID Solicitud:</b> {b_id} (Estado: {b_info['estado']})</span><br>
                    <b>Vendedora:</b> {b_info['vendedor']} | <b>Celular:</b> {b_info['whatsapp']}<br>
                    <b>Punto:</b> {b_info['zona']}
                </div>
            """, unsafe_allow_html=True)
            
            if b_info.get('imagenes'):
                st.markdown("**📸 Enlaces de Fotos Integrados:**")
                for img_url in b_info['imagenes']:
                    st.markdown(f"- <a href='{img_url}' target='_blank'>{img_url}</a>", unsafe_allow_html=True)
            
            if "espera" in str(b_info['estado']).lower():
                if st.button("🟢 Activar en Pantalla Temporal", key=f"tab_acc_{b_id}"):
                    st.session_state.bloques_db[b_id]['estado'] = "🟢 ACTIVO"
                    st.rerun()
            
            nuevo_texto = st.text_area(f"Modificar artículos de {b_id}:", value=b_info['articulos'], key=f"tab_edit_{b_id}")
            if nuevo_texto != b_info['articulos']:
                st.session_state.bloques_db[b_id]['articulos'] = nuevo_texto
            
            if st.button(f"🗑️ Quitar {b_id}", key=f"tab_del_{b_id}"):
                if b_id in st.session_state.bloques_db:
                    del st.session_state.bloques_db[b_id]
                st.rerun()
            st.markdown("---")

st.markdown('<div class="seccion-quejas">Quejas, sugerencias y aclaraciones, con Capitana Albatros: 8143029578</div>', unsafe_allow_html=True)
