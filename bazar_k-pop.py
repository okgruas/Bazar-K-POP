import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA Y DISEÑO
# ==========================================
st.set_page_config(
    page_title="Registro de Clósets - Sistema de Cobranza",
    page_icon="📐",
    layout="centered"
)

st.title("📐 Registro de Clósets")
st.write("Agrega los clósets a la lista y presiona el botón de guardar para enviarlos a Google Sheets.")

# ==========================================
# 2. INICIALIZACIÓN DEL ESTADO DE LA SESIÓN (SESSION STATE)
# ==========================================
# Esto evita que los datos temporales se borren al interactuar con otros botones
if "lista_closets" not in st.session_state:
    st.session_state.lista_closets = []

# ==========================================
# 3. FUNCIÓN PARA GUARDAR EN GOOGLE SHEETS
# ==========================================
def guardar_en_google_sheets(datos_nuevos):
    """
    Función encargada de enviar los datos acumulados a Google Sheets.
    Modifica los parámetros internos según la librería que uses.
    """
    try:
        # --- OPCIÓN A: Si usas st.connection ("st-sheets-connection") ---
        # conn = st.connection("gsheets", type=GSheetsConnection)
        # 
        # # Primero leemos lo que ya hay para no borrar nada
        # df_existente = conn.read(worksheet="Closets")
        # 
        # # Convertimos los nuevos datos a DataFrame
        # df_nuevos = pd.DataFrame(datos_nuevos, columns=["Fecha", "Modelo", "Medidas", "Precio", "Notas"])
        # 
        # # Concatenamos el histórico con lo nuevo
        # df_total = pd.concat([df_existente, df_nuevos], ignore_index=True)
        # 
        # # Volvemos a escribir todo el bloque actualizado
        # conn.update(worksheet="Closets", data=df_total)
        
        # --- OPCIÓN B: Si usas gspread directamente (Descomenta si es tu caso) ---
        # # sheet.append_rows(datos_nuevos) 
        
        # Simulamos una pequeña espera de red para experiencia de usuario
        import time
        time.sleep(1.5)
        
        return True
        
    except Exception as e:
        st.error(f"❌ Error crítico de conexión con Google Sheets: {e}")
        return False

# ==========================================
# 4. FORMULARIO DE CAPTURA (INTERFAZ DE USUARIO)
# ==========================================
with st.form("formulario_registro", clear_on_submit=True):
    st.subheader("📝 Datos del Clóset")
    
    # Campos de entrada
    modelo_closet = st.text_input("Modelo / Descripción del Clóset:", placeholder="Ej. Clóset Minimalista RACO")
    medidas_closet = st.text_input("Medidas (Ancho x Alto x Fondo):", placeholder="Ej. 2.40 x 2.20 x 0.60 m")
    precio_closet = st.number_input("Precio de Venta ($):", min_value=0.0, step=50.0, format="%.2f")
    notas_closet = st.text_area("Notas u Observaciones adicionales:", placeholder="Detalles de instalación o color...")

    # Botón interno del formulario para agregar a la lista local
    btn_agregar = st.form_submit_button("➕ Agregar a la Lista Temporal")

    if btn_agregar:
        if modelo_closet.strip() == "" or medidas_closet.strip() == "":
            st.warning("⚠️ El Modelo y las Medidas son obligatorios para el registro.")
        else:
            # Creamos la fila de datos con la fecha y hora actual
            fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M")
            nueva_fila = [fecha_registro, modelo_closet, medidas_closet, precio_closet, notas_closet]
            
            # GUARDAMOS EN LA RAM DE STREAMLIT (No se borra al interactuar)
            st.session_state.lista_closets.append(nueva_fila)
            st.toast(f"✅ ¡{modelo_closet} añadido a la lista temporal!")

# ==========================================
# 5. VISUALIZACIÓN Y CONTROL DE DATOS TEMPORALES
# ==========================================
if st.session_state.lista_closets:
    st.write("---")
    st.subheader("📋 Clósets pendientes de guardar en Sheets")
    
    # Convertimos a DataFrame solo para mostrarlo bonito en la app
    df_temporal = pd.DataFrame(
        st.session_state.lista_closets, 
        columns=["Fecha", "Modelo", "Medidas", "Precio", "Notas"]
    )
    
    # Mostramos la tabla interactiva
    st.dataframe(df_temporal, use_container_width=True)
    
    # Métricas rápidas de control
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de Clósets en Espera", len(st.session_state.lista_closets))
    with col2:
        st.metric("Monto Total Acumulado", f"${df_temporal['Precio'].sum():,.2f}")
