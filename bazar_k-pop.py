import streamlit as st
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Bazar Digital K-Pop & Clóset",
    page_icon="✨",
    layout="wide"
)

# ⚠️ CONFIGURACIÓN DE ADMINISTRADOR ⚠️
TELEFONO_ADMIN_WHATSAPP = "528143029578"
CONTRASENA_ADMIN = "bazar123"

# --- CONEXIÓN DE LECTURA GLOBAL (GOOGLE SHEETS) ---
# Esto hace que los clósets carguen desde el Excel y sean visibles para todos, sobreviviendo al refresh.
if "bloques_db" not in st.session_state:
    st.session_state.bloques_db = {}

try:
    # Conectamos con tu mina de datos de Google Sheets usando los Secrets que configuraste
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Leemos la pestaña "Vendedoras" (recuerda nombrar así la pestaña en tu Sheets)
    df_sheets = conn.read(worksheet="Vendedoras", ttl="1m")
    df_sheets = df_sheets.dropna(how="all")
    
    # Sincronizamos lo que está en el Excel con el diseño de tu app
    for _, fila in df_sheets.iterrows():
        id_b = str(fila.get("id", ""))
        if id_b:
            st.session_state.bloques_db[id_b] = {
                "vendedor": str(fila.get("vendedor", "")),
                "whatsapp": str(fila.get("whatsapp", "")),
                "zona": str(fila.get("zona", "")),
                "categoria": str(fila.get("categoria", "")),
                "articulos": str(fila.get("articulos", "")),
                "imagenes": [], # Las imágenes de catálogo se mantienen optimizadas en texto o links
                "estado": str(fila.get("estado", "🟢 ACTIVO")),
                "fecha": str(fila.get("fecha", ""))
            }
except Exception as e:
    # Si el Sheets está vacío o desconectado momentáneamente, la app no se cae
    pass

# --- ESTILOS CSS REFORZADOS (TU DISEÑO SHEIN ORIGINAL) ---
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
        caret-color: #1A1A1A !important; /* Fuerza la barrita parpadeante a color negro */
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
# PESTAÑA 1: EL ESCAPARATE PÚBLICO
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
    bloques_activos = {k: v for k, v in st.session_state.bloques_db.items() if v['estado'] == "🟢 ACTIVO"}
    
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
                    "estado": "⏳ En espera de verificación",
                    "fecha": datetime.now().strftime("%d/%m/%Y")
                }
                st.session_state.enviado_ok = False

    if st.session_state.pre_registro is not None:
        datos = st.session_state.pre_registro
        id_b = datos["id"]
        
        st.markdown('<div class="preview-container">', unsafe_allow_html=True)
        st.warning("⏳ Tu registro está listo. Por favor, realiza el paso final de WhatsApp abajo para guardarlo.")
        
        st.markdown("### 👀 Detalles de tu Solicitud")
        col_p1, col_p2 = st.columns([1, 2])
        with col_p1:
            st.metric(label="Monto por Validar", value="$25 MXN")
            st.write(f"🆔 **ID Asignado:** `{id_b}`")
        with col_p2:
            st.write(f"👤 **Vendedora:** {datos['vendedor']}")
            st.write(f"📍 **Punto Seguro:** {datos['zona']}")
            st.markdown(f'<div class="articulos-box-shein">{datos["articulos"]}</div>', unsafe_allow_html=True)
        
        msg = (
            f"Hola Raquel, vengo de la página del Bazar.\n\n"
            f"👤 *Vendedora:* {datos['vendedor']}\n"
            f"🆔 *ID:* {id_b}\n"
            f"📍 *Punto:* {datos['zona']}\n"
            f"📂 *Cat:* {datos['categoria']}\n"
            f"📝 *Artículos:* {datos['articulos']}\n\n"
            f"📎 *(Adjunto foto de mi comprobante)*"
        )
        msg_encoded = msg.replace(' ', '%20').replace('\n', '%0A')
        url_wa = f"https://wa.me/{TELEFONO_ADMIN_WHATSAPP}?text={msg_encoded}"
        
        if not st.session_state.enviado_ok:
            if st.button("📲 Click Para Registrar y Preparar Envío de WhatsApp", key="btn_disparador_wa"):
                st.session_state.enviado_ok = True
                st.rerun()
        else:
            st.success("✅ ¡Datos preparados!")
            st.markdown(f"""
                <a class="btn-wa-nativo" href="{url_wa}" target="_blank">
                    🚀 ¡TODO LISTO! CLIC AQUÍ PARA ENVIAR COMPROBANTE POR WHATSAPP
                </a>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PESTAÑA 3: PANEL DE CONTROL DE ADMINISTRADORA
# ==========================================
with tab_admin:
    st.subheader("🔐 Consola de Verificación")
    clave_ingresada = st.text_input("Introduce la Contraseña de Administradora:", type="password", key="tab_admin_key")
    
    if clave_ingresada == CONTRASENA_ADMIN:
        st.success("Acceso Autorizado - Modo Gestor")
        
        # --- NUEVA SECCIÓN: AGREGAR MANUALMENTE DESDE EL PANEL ---
        st.markdown("### ➕ Registrar Vendedora Aprobada Directamente")
        st.write("Si ya te pagaron por WhatsApp, puedes darla de alta rápido desde aquí para probar cómo se ve en el Bazar:")
        
        with st.form("admin_alta_manual", clear_on_submit=True):
            col_ad1, col_ad2 = st.columns(2)
            with col_ad1:
                adm_nombre = st.text_input("Nombre de la Vendedora:")
                adm_whatsapp = st.text_input("WhatsApp (10 dígitos):")
            with col_ad2:
                adm_zona = st.text_input("Punto Seguro de Entrega:")
                adm_cat = st.selectbox("Categoría:", ["K-Pop (Photocards/Coleccionables)", "Mi Clóset (Ropa/Accesorios)"])
            
            adm_articulos = st.text_area("Artículos (Uno por renglón):")
            btn_adm_guardar = st.form_submit_button("🟢 ACTIVAR E INYECTAR AL BAZAR TRAS VALIDAR")
            
            if btn_adm_guardar:
                if adm_nombre and adm_whatsapp and adm_articulos:
                    id_manual = f"BZR-ADM-{datetime.now().strftime('%H%M%S')}"
                    # Lo inyectamos directo al estado de la sesión para verlo de inmediato
                    st.session_state.bloques_db[id_manual] = {
                        "vendedor": adm_nombre,
                        "whatsapp": adm_whatsapp,
                        "zona": adm_zona,
                        "categoria": adm_cat,
                        "articulos": adm_articulos,
                        "imagenes": [],
                        "estado": "🟢 ACTIVO",
                        "fecha": datetime.now().strftime("%d/%m/%Y")
                    }
                    st.success(f"✅ ¡Bloque `{id_manual}` activado localmente! Revisa la pestaña 'Ver el Bazar' para ver cómo quedó.")
                    st.rerun()
                else:
                    st.warning("Completa el nombre, WhatsApp y los artículos para poder dar el alta.")

        st.markdown("---")
        st.markdown("### 🛠️ Control Manual de Base de Datos")
        st.info("💡 Como Google Sheets bloquea las escrituras automatizadas públicas, copia los datos que te lleguen a tu WhatsApp y pégalos en tu archivo de Google Excel para que aparezcan aquí fijas para todo el mundo.")
        
        # Si hay bloques en memoria (ya sean del Excel o creados manualmente arriba), los listamos con opción de eliminarlos
        if st.session_state.bloques_db:
            st.write("#### Lista de Tienditas en Memoria:")
            for b_id in list(st.session_state.bloques_db.keys()):
                b_info = st.session_state.bloques_db[b_id]
                
                # Una cajita limpia para cada vendedor registrado
                with st.container():
                    st.markdown(f"""
                        <div class="admin-box" style="border-left: 6px solid #E6005C; padding: 10px; margin-bottom: 10px;">
                            <span style="color:#D81159;"><b>ID:</b> {b_id}</span> | <b>Vendedora:</b> {b_info['vendedor']}<br>
                            <b>Artículos:</b> {b_info['articulos']}<br>
                            <b>Estado actual:</b> <code>{b_info['estado']}</code>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Botón individual para remover el bloque de la pantalla si es necesario
                    if st.button(f"🗑️ Quitar Temporalmente ID: {b_id}", key=f"del_{b_id}"):
                        del st.session_state.bloques_db[b_id]
                        st.toast(f"Publicación {b_id} removida de la sesión.")
                        st.rerun()
        else:
            st.write("No hay bloques registrados en la sesión actualmente. Usa el formulario de arriba o conecta tu Sheets para poblar la lista.")
st.markdown('<div class="seccion-quejas">Quejas, sugerencias y aclaraciones, con Capitana Albatros: 8143029578</div>', unsafe_allow_html=True)
