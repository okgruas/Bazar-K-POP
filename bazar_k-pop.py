import streamlit as st
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Bazar Digital K-Pop & Clóset",
    page_icon="✨",
    layout="wide"
)

# ⚠️ CONFIGURACIÓN DE ADMINISTRADOR ⚠️
TELEFONO_ADMIN_WHATSAPP = "528143029578"
CONTRASENA_ADMIN = "bazar123"

# --- BASE DE DATOS EN MEMORIA PERMANENTE ---
if "bloques_db" not in st.session_state:
    st.session_state.bloques_db = {}

# --- ESTILOS CSS REFORZADOS ---
st.markdown("""
    <style>
    /* Fondo general */
    .stApp {
        background: linear-gradient(135deg, #FFE5EC 0%, #FFB3C6 40%, #FF477E 100%);
    }
    
    /* Contenedores blancos */
    .stForm, .preview-container, .public-block, .admin-box {
        background-color: rgba(255, 255, 255, 0.98) !important;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.15);
        margin-bottom: 25px;
    }
    
    /* Forzar títulos y etiquetas generales en negro */
    label, p, span, .stRadio p, h1, h2, h3, div[data-testid="stMarkdownContainer"] p {
        color: #1A1A1A !important;
        font-weight: bold !important;
    }
    
    /* Arreglo de texto en los campos de escritura */
    textarea, input[type="text"], div[data-testid="stTextArea"] textarea, div[data-testid="stTextInput"] input {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        border: 2px solid #FF477E !important;
        -webkit-text-fill-color: #1A1A1A !important;
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

    /* BOTÓN DE ACCIÓN (Verde, grande, sin cuadro negro de fondo) */
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
    
    /* Fotos miniatura controladas */
    .mini-foto img {
        max-height: 140px !important;
        object-fit: contain !important;
        border-radius: 8px;
        border: 1px solid #FFB3C6;
    }
    
    .articulos-box {
        background-color: #F8F9FA !important;
        color: #1A1A1A !important;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #E6005C;
        font-size: 16px;
        white-space: pre-wrap;
    }
    
    .badge-activo {
        background-color: #D4EDDA; color: #155724; padding: 5px 10px; border-radius: 5px; font-weight: bold;
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
# PESTAÑA 1: EL ESCAPARATE PÚBLICO
# ==========================================
with tab_bazar:
    # ⚠️ LEYENDA DE SEGURIDAD AL PRINCIPIO DE LA PESTAÑA ⚠️
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
    bloques_activos = {k: v for k, v in st.session_state.bloques_db.items() if v['estado'] == "🟢 ACTIVO"}
    
    if not bloques_activos:
        st.info("No hay tienditas activas en este momento. Las publicaciones aprobadas aparecerán aquí de inmediato.")
    else:
        for id_b, info_b in bloques_activos.items():
            # Creación del mensaje automático codificado para WhatsApp
            texto_mensaje = "Hola, vengo del bazar digital de k-pop, me interesó alguno de tus artículos. ✨🛍️"
            texto_codificado = texto_mensaje.replace(' ', '%20').replace('\n', '%0A')
            url_wa_vendedor = f"https://wa.me/{info_b['whatsapp']}?text={texto_codificado}"

            st.markdown(f"""
                <div class="public-block">
                    <span class="badge-activo">🟢 TIENDA ACTIVA</span>
                    <h3 style="margin-top:10px; margin-bottom:5px; color:#D81159;">🛍️ Bazar de {info_b['vendedor']}</h3>
                    <p style="margin: 2px 0; color:#1A1A1A;">📂 <b>Categoría:</b> {info_b['categoria']} | 📅 <b>Publicado:</b> {info_b['fecha']}</p>
                    <p style="margin: 2px 0; color:#1A1A1A;">📍 <b>Punto Seguro:</b> {info_b['zona']}</p>
                    <hr style="border-color:#FFB3C6;">
                    <div class="articulos-box">{info_b['articulos']}</div>
                    <br>
            """, unsafe_allow_html=True)
            
            if info_b.get('imagenes'):
                st.markdown("**📸 Fotos del Bazar:**")
                cols_img = st.columns(6)
                for idx, img_file in enumerate(info_b['imagenes']):
                    with cols_img[idx % 6]:
                        st.markdown('<div class="mini-foto">', unsafe_allow_html=True)
                        st.image(img_file, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown(f"""
                    <br>
                    <a href="{url_wa_vendedor}" target="_blank">
                        <button style="background-color:#E6005C; color:white; border:none; padding:12px 24px; font-weight:bold; border-radius:8px; cursor:pointer;">
                            💬 Contactar al Vendedor por vía WhatsApp
                        </button>
                    </a>
                </div>
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

    with st.form("form_anuncio", clear_on_submit=False):
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
        st.markdown("### 💳 4. Pago de Validación ($25 MXN)")
        st.markdown("""
            <div style="background-color: #FFFFFF; padding: 20px; border-radius: 10px; border: 2px solid #D81159;">
                <p style="color: #D81159 !important; font-size: 17px !important; margin: 0 0 5px 0; font-weight: 900;">🏛️ BANCO: NU MÉXICO</p>
                <p style="color: #1A1A1A !important; font-size: 17px !important; margin: 0 0 5px 0; font-family: monospace; font-weight: bold;">🔑 CLABE: 0123 4567 8901 2345 67</p>
                <p style="color: #1A1A1A !important; font-size: 17px !important; margin: 0; font-weight: bold;">👤 TITULAR: CAPITANA ALBATROS</p>
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
                    "estado": "⏳ En espera de verificación",
                    "fecha": datetime.now().strftime("%d/%m/%Y")
                }
                st.session_state.enviado_ok = False # Reiniciar estado de WhatsApp

    # --- SECCIÓN DE VISTA PREVIA Y GUARDADO BLINDADO ---
    if st.session_state.pre_registro is not None:
        datos = st.session_state.pre_registro
        id_b = datos["id"]
        
        if id_b in st.session_state.bloques_db and st.session_state.bloques_db[id_b]['estado'] == "🟢 ACTIVO":
            st.session_state.pre_registro = None
            st.session_state.enviado_ok = False
            st.rerun()
        else:
            st.markdown('<div class="preview-container">', unsafe_allow_html=True)
            st.warning("⏳ Tu registro está en proceso de revisión. Por favor, realiza el paso final de WhatsApp en la parte de abajo.")
            
            st.markdown("### 👀 Detalles de tu Solicitud")
            col_p1, col_p2 = st.columns([1, 2])
            with col_p1:
                st.metric(label="Monto por Validar", value="$15 MXN")
                st.write(f"🆔 **ID Asignado:** `{id_b}`")
            with col_p2:
                st.write(f"👤 **Vendedora:** {datos['vendedor']}")
                st.write(f"📍 **Punto Seguro:** {datos['zona']}")
                st.write("**📝 Lista enviada:**")
                st.markdown(f'<div class="articulos-box">{datos["articulos"]}</div>', unsafe_allow_html=True)
            
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
            url_wa = f"https://wa.me/{8143029578}?text={msg_encoded}"
            
            # PASO A: El botón de Streamlit guarda en base de datos local primero para que NO se pierda
            if not st.session_state.enviado_ok:
                if st.button("📲 Click Para Registrar y Preparar Envío de WhatsApp", key="btn_disparador_wa"):
                    st.session_state.bloques_db[id_b] = {
                        "vendedor": datos["vendedor"],
                        "whatsapp": datos["whatsapp"],
                        "zona": datos["zona"],
                        "categoria": datos["categoria"],
                        "articulos": datos["articulos"],
                        "imagenes": datos["imagenes"],
                        "estado": "⏳ En espera de verificación",
                        "fecha": datos["fecha"]
                    }
                    st.session_state.enviado_ok = True
                    st.rerun()
            else:
                # PASO B: Se habilita el botón nativo HTML con target="_blank" para abrir en otra pestaña limpia
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
                
                if b_info['estado'] == "⏳ En espera de verificación":
                    if st.button("🟢 Aceptar Bloque", key=f"tab_acc_{b_id}"):
                        st.session_state.bloques_db[b_id]['estado'] = "🟢 ACTIVO"
                        st.toast(f"¡Bloque {b_id} activado con éxito!")
                        st.rerun()
                
                nuevo_texto = st.text_area(f"Modificar artículos de {b_id}:", value=b_info['articulos'], key=f"tab_edit_{b_id}")
                if nuevo_texto != b_info['articulos']:
                    st.session_state.bloques_db[b_id]['articulos'] = nuevo_texto
                
                if st.button(f"🗑️ Eliminar permanentemente {b_id}", key=f"tab_del_{b_id}"):
                    del st.session_state.bloques_db[b_id]
                    st.rerun()
                st.markdown("---")

# Sección discreta de quejas al fondo
st.markdown('<div class="seccion-quejas">Quejas, sugerencias y aclaraciones, con Capitana Albatros: 8143029578</div>', unsafe_allow_html=True)
