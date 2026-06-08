import base64
import os

# Función para convertir imágenes locales a Base64 y que el HTML las pueda leer
def obtener_base64_de_imagen(ruta_relativa):
    if os.path.exists(ruta_relativa):
        with open(ruta_relativa, "rb") as image_file:
            return f"data:image/png;base64,{base64.b64encode(image_file.read()).decode()}"
    return ""

# Cargar tus imágenes locales (ajusta el nombre exacto de tus archivos si es necesario)
# Si tus logos están en la raíz junto a app.py, déjalos como "portada1.png" y "portada2.png"
ruta_portada = "portada1.png" 
ruta_perfil = "portada2.png"

img_portada_base64 = obtener_base64_de_imagen(ruta_portada)
img_perfil_base64 = obtener_base64_de_imagen(ruta_perfil)
