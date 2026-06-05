import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import requests
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Bazar Digital K-Pop & Clóset",
    page_icon="✨",
    layout="wide"
)

# ⚠️ CONFIGURACIÓN DE ADMINISTRADOR
TELEFONO_ADMIN_WHATSAPP = "528143029578"
CONTRASENA_ADMIN = "bazar123"
IMGBB_API_KEY = "c72da82c65cce967aac091defc1f41dd"

# --- FUNCIÓN PARA SUBIR IMÁGENES A IMGBB ---
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

# --- CONEXIÓN DE GOOGLE SHEETS ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Forzar la lectura limpia de la primera pestaña (Hoja 1)
    df_sheets = conn.read(ttl="0m")
    df_sheets = df_sheets.dropna(how="all")
except Exception as e:
    st.error(f"⚠️ Error de conexión con Sheets: {e}")
    df_sheets = pd.DataFrame(columns=["id", "vendedor", "whatsapp", "zona", "categoria", "articulos", "estado", "fecha", "imagenes", "comprobante"])

# Asegurar que todas las columnas necesarias existan en el DataFrame de memoria
for col in ["id", "vendedor", "whatsapp", "zona", "categoria", "articulos", "estado", "fecha", "imagenes", "comprobante"]:
    if col not in df_sheets.columns:
        df_sheets[col] = ""

# --- ESTILOS VISUALES CUIDADOS ---
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
    div[data-testid="stFileUploader"] section { background-color: #FFF0F5 !important; border: 2px dashed #E6005C !important; border-radius: 10px !important; }
    div[data-testid="stFormSubmitButton"] button {
        background-color: #E6005C !important; color: #FFFFFF !important; border: 2px solid #FFFFFF !important;
        border-radius: 10px !important; padding: 14px 28px !important; width: 100% !important; font-weight: 900 !important;
    }
    .articulos-box-shein {
        background-color: #F8F9FA !important; color: #1A1A1A !important; padding: 10px; border-radius: 6px;
        border-left: 4px solid #E6005C; font-size: 14px; white-space: pre-wrap; margin-bottom: 10px; max-height: 150px; overflow-y: auto;
    }
    .badge-activo-shein { background-color: #D4EDDA; color: #155724; padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; }
    .btn-wa-nativo {
        display: block; width: 100%; background-color: #25D366 !important; color: #1A1A1A !important; text-align: center;
        padding: 16px 32px; border-radius: 12px; font-size: 19px; font-weight: 900; text-decoration: none; border: 2px solid #FFFFFF;
    }
    </style>
""", unsafe_allow_html=True)

# Títulos del encabezado
st.markdown('<div style="text-align:center; font-size:42px; font-weight:900; color:#D81159;">✨ BAZAR DIGITAL DE K-POP & CLÓSET ✨</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center; font-size:18px; color:white; font-weight:bold; margin-bottom:25px;">🛍️ Photocards, Coleccionables & Moda • Monterrey</div>', unsafe_allow_html=True)

tab_bazar, tab_anunciarse, tab_admin = st.tabs(["🛍️ Ver el Bazar / Clóset", "💜 Registrarse como Vendedora", "🔐 Panel de Control (Solo Admin)"])

# ==========================================
# PESTAÑA 1: EL ESCAPARATE PÚBLICO
# ==========================================
with tab_bazar:
    st.markdown("""
        <div style="background-color: #FFF3CD; color: #856404; padding: 15px; border-radius: 12px; margin-bottom: 20px; border-left: 6px solid #FFC107;">
            ⚠️ <b>Aviso de Seguridad:</b> Realiza tus entregas únicamente en lugares públicos y concurridos. Cada vendedora es responsable de sus tratos y entregas.
        </div>
    """, unsafe_allow_html=True)

    # Filtrar bloques activos
    df_activos = df_sheets[df_sheets["estado"].astype(str).str.contains("ACTIVO", na=False, case=False)]
    
    if df_activos.empty:
        st.info("🛍️ No hay tienditas activas visibles en el mapa digital todavía. ¡Regístrate en la siguiente pestaña!")
    else:
        columnas_por_fila = 3
        lista_filas = [df_activos.iloc[i:i+columnas_por_fila] for i in range(0, len(df_activos), columnas_por_fila)]
        
        for fila in lista_filas:
            cols = st.columns(columnas_por_fila)
            for idx, (_, row) in enumerate(fila.iterrows()):
                with cols[idx]:
                    id_b = row["id"]
                    msg_wa = f"Hola, vengo del Bazar Digital. Me interesaron tus artículos del bloque {id_b}. ✨🛍️".replace(' ', '%20')
                    url_wa_vendedor = f"https://wa.me/{row['whatsapp']}?text={msg_wa}"
                    
                    st.markdown(f"""
                        <div class="shein-card">
                            <div>
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                    <span class="badge-activo-shein">🟢 ACTIVO</span>
                                    <span style="font-size: 11px; color: #666666;">📅 {row['fecha']}</span>
                                </div>
                                <h4 style="margin: 0 0 5px 0; color:#D81159; font-size: 18px;">🛍️ Bazar de {row['vendedor']}</h4>
                                <p style="margin: 2px 0; color:#555555; font-size: 12px;">📂 <b>Categoría:</b> {row['categoria']}</p>
                                <p style="margin: 2px 0; color:#555555; font-size: 12px; margin-bottom: 10px;">📍 <b>Punto:</b> {row['zona']}</p>
                                <div class="articulos-box-shein">{row['articulos']}</div>
                            </div>
                    """, unsafe_allow_html=True)
                    
                    # Renderizar imágenes si existen links guardados
                    if "imagenes" in row and pd.notna(row["imagenes"]) and str(row["imagenes"]).strip() != "":
                        links_fotos = str(row["imagenes"]).split(",")
                        cols_img = st.columns(4)
                        for f_idx, link_f in enumerate(links_fotos[:4]):
                            if link_f.strip():
                                with cols_img[f_idx % 4]:
                                    st.image(link_f.strip(), use_container_width=True)
                    
                    st.markdown(f"""
                            <div style="margin-top: 15px;">
                                <a href="{url_wa_vendedor}" target="_blank" style="text-decoration: none;">
                                    <button style="background-color:#E6005C; color:white; border:none; padding:10px 15px; font-weight:bold; border-radius:8px; cursor:pointer; width:100%; font-size:13px;">
                                        💬 Contactar por WhatsApp
                                    </button>
                                </a>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

# ==========================================
# PESTAÑA 2: REGISTRO DE VENDEDORAS
# ==========================================
with tab_anunciarse:
    st.subheader("💜 Registra tu Bloque de Anuncios")
    st.write("Costo por bloque: **$25 MXN** con una vigencia automática de 15 días.")
    
    if "registro_actual" not in st.session_state:
        st.session_state.registro_actual = None

    with st.form("form_anuncio", clear_on_submit=True):
        st.markdown("### 👤 1. Datos de Contacto")
        col1, col2 = st.columns(2)
        with col1:
            nombre_vendedor = st.text_input("Nombre / Tienda *")
            whatsapp_vendedor = st.text_input("WhatsApp de Contacto * (10 dígitos)")
        with col2:
            zona_entrega = st.text_input("Punto Seguro de Entrega * (ej. Centro de Monterrey)")
            tipo_articulo = st.radio("Categoría: *", ["K-Pop (Photocards/Coleccionables)", "Mi Clóset (Ropa/Accesorios)"])
            
        st.markdown("---")
        st.markdown("### 🛍️ 2. Tus Artículos y Precios")
        lista_articulos = st.text_area("Lista tus productos (Uno por renglón con precio) *", placeholder="Ejemplo:\n- Photocard Seungmin ODDINARY - $120")
        
        st.markdown("### 📸 3. Fotos de tus Artículos")
        fotos_articulos = st.file_uploader("Selecciona imágenes de tus productos:", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
        
        st.markdown("---")
        st.markdown("### 💳 4. Pago de Validación ($25 MXN)")
        st.markdown("""
            <div style="background-color: #FFFFFF; padding: 15px; border-radius: 10px; border: 2px solid #D81159; margin-bottom: 15px;">
                <p style="color: #D81159 !important; margin: 0; font-weight: 900;">🏛️ BANCO: NU MÉXICO</p>
                <p style="color: #1A1A1A !important; margin: 5px 0; font-family: monospace;">🔑 CLABE: 0123 4567 8901 2345 67</p>
                <p style="color: #1A1A1A !important; margin: 0;">👤 TITULAR: RAQUEL COVARRUBIAS</p>
            </div>
        """, unsafe_allow_html=True)
        
        foto_comprobante = st.file_uploader("Sube la captura de tu comprobante de pago: *", type=["jpg", "png", "jpeg"])
        
        enviar_anuncio = st.form_submit_button("Subir Bloque de Anuncios para Validación")

        if enviar_anuncio:
            if not (nombre_vendedor and whatsapp_vendedor and zona_entrega and lista_articulos and foto_comprobante):
                st.error("Por favor, llena todos los campos obligatorios (*) y anexa el comprobante.")
            else:
                id_transaccion = f"BZR-{datetime.now().strftime('%d%H%M%S')}"
                
                with st.spinner("Subiendo imágenes y procesando base de datos... ✨"):
                    # Subir fotos de productos a ImgBB
                    links_fotos = []
                    if fotos_articulos:
                        for f in fotos_articulos:
                            u = subir_a_imgbb(f)
                            if u: links_fotos.append(u)
                    str_links_fotos = ",".join(links_fotos)
                    
                    # Subir comprobante a ImgBB
                    link_comprobante = subir_a_imgbb(foto_comprobante)
                    
                    # Estructurar fila alineada a tus columnas en minúsculas de Google Sheets
                    nueva_fila = pd.DataFrame([{
                        "id": id_transaccion,
                        "vendedor": nombre_vendedor,
                        "whatsapp": whatsapp_vendedor,
                        "zona": zona_entrega,
                        "categoria": tipo_articulo,
                        "articulos": lista_articulos,
                        "estado": "⏳ Espera",
                        "fecha": datetime.now().strftime("%d/%m/%Y"),
                        "imagenes": str_links_fotos,
                        "comprobante": link_comprobante
                    }])
                    
                    try:
                        df_actualizado = pd.concat([df_sheets, nueva_fila], ignore_index=True)
                        conn.update(data=df_actualizado)
                        st.success("✅ ¡Registrado exitosamente en tu Google Sheets!")
                        
                        st.session_state.registro_actual = {
                            "id": id_transaccion, "vendedor": nombre_vendedor, "whatsapp": whatsapp_vendedor,
                            "zona": zona_entrega, "categoria": tipo_articulo, "articulos": lista_articulos,
                            "imagenes": links_fotos, "comprobante": link_comprobante
                        }
                    except Exception as sheet_err:
                        st.error(f"Error escribiendo en Sheets: {sheet_err}")

    if st.session_state.registro_actual:
        datos = st.session_state.registro_actual
        st.markdown('<div class="preview-container">', unsafe_allow_html=True)
        st.info("🚀 Registro guardado en la lista. Opcional: Envía tu confirmación directa:")
        msg = f"Hola Capitana Albatros, registré mi bloque {datos['id']}. Vendedora: {datos['vendedor']}. Comprobante: {datos['comprobante']}"
        url_wa = f"https://wa.me/{TELEFONO_ADMIN_WHATSAPP}?text={msg.replace(' ', '%20')}"
        st.markdown(f'<a class="btn-wa-nativo" href="{url_wa}" target="_blank">🚀 ENVIAR AVISO DE PAGO</a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 🔐 PESTAÑA 3: PANEL DE CONTROL DE ADMINISTRADORA
# ==========================================
with tab_admin:
    st.subheader("🔐 Panel de Aprobaciones Directas")
    clave = st.text_input("Introduce la Contraseña de Administradora:", type="password")
    
    if clave == CONTRASENA_ADMIN:
        st.success("Acceso Autorizado")
        
        if df_sheets.empty:
            st.info("No hay registros en la base de datos.")
        else:
            st.dataframe(df_sheets)
            st.markdown("### 🛠️ Administrar Solicitudes Pendientes")
            
            for idx, row in df_sheets.iterrows():
                if "espera" in str(row["estado"]).lower():
                    st.markdown(f"""
                        <div class="admin-box">
                            <b>ID:</b> {row['id']} | <b>Vendedora:</b> {row['vendedor']}<br>
                            <b>Artículos:</b> {row['articulos']}<br>
                            <b>Comprobante de pago:</b> <a href="{row['comprobante']}" target="_blank">Ver Captura de Pantalla</a>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    col_b1, col_b2 = st.columns(2)
                    with col_b1:
                        if st.button(f"🟢 Activar Bloque {row['id']}", key=f"act_{row['id']}"):
                            df_sheets.at[idx, "estado"] = "🟢 ACTIVO"
                            conn.update(data=df_sheets)
                            st.success(f"Bloque {row['id']} activado con éxito.")
                            st.rerun()
                    with col_b2:
                        if st.button(f"🗑️ Eliminar Bloque {row['id']}", key=f"del_{row['id']}"):
                            df_sheets = df_sheets.drop(idx)
                            conn.update(data=df_sheets)
                            st.warning(f"Bloque {row['id']} removido.")
                            st.rerun()

st.markdown('<div style="text-align:center; font-size:11px; color:#666666; margin-top:20px;">Quejas, sugerencias y aclaraciones, con Capitana Albatros: 8143029578</div>', unsafe_allow_html=True)
