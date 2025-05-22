import streamlit as st
from streamlit_option_menu import option_menu
import os
import json
from datetime import datetime
from PIL import Image
import base64
from database import agregar_evento, obtener_eventos, eliminar_evento

# Configuración inicial
st.set_page_config(page_title="Eventos York & Katy", layout="wide")

st.markdown("""
    <style>
    /* Texto blanco por defecto global */
    /* Color blanco solo para cuerpo general, sin afectar tarjetas */
    body, .stApp {
        color: white;
    }

    /* Inputs y campos de texto */
    input[type="text"], textarea, input[type="email"], input[type="number"], input[type="date"] {
        background-color: rgba(255, 255, 255, 0.85) !important;
        color: black !important;
        border: 1px solid rgba(0, 0, 0, 0.3);
        border-radius: 10px;
        padding: 10px;
        font-size: 15px;
    }

    /* Selects */
    .css-1wa3eu0-placeholder, .css-1uccc91-singleValue, div[data-baseweb="select"] * {
        color: black !important;
    }

    /* Botón principal */
    button[kind="primary"] {
        background-color: #ff4b9b !important;
        color: white !important;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        border: none;
        transition: 0.3s ease-in-out;
    }

    button[kind="primary"]:hover {
        background-color: #e6448a !important;
        transform: scale(1.02);
        box-shadow: 0 0 10px #ff4b9b80;
    }

    /* Títulos y etiquetas */
    h2 {
        text-align: center;
        font-size: 28px;
        margin-top: 10px;
        margin-bottom: 30px;
        color: white !important;
    }

    label {
        color: white !important;
        font-weight: bold;
    }

    /* Estilo de formularios centrado */
    .stTextInput, .stTextArea, .stSelectbox, .stDateInput {
        max-width: 600px;
        margin: 0 auto 15px auto;
    }

    /* Forzar texto negro dentro de bloques blancos */
    div[style*="background: rgba(255, 255, 255, 0.92)"] *,
    div[style*="background-color: rgba(255,255,255,0.85)"] *,
    div[style*="background-color: rgba(255, 255, 255, 0.85)"] * {
        color: #000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Fondo personalizado con glassmorphism en sidebar
def set_background(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    css = f"""
    <style>
    html {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }}
    .stApp {{
        background-color: rgba(0,0,0,0);
    }}
    section[data-testid="stSidebar"] > div:first-child {{
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 4px 0 12px rgba(0, 0, 0, 0.2);
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_background("recursos/fondo_app_eventos.png")

DATOS_FILE = "datos/eventos.json"
GALERIA_DIR = "galeria"
LOGO_PATH = "recursos/yorkat_logo_animado.gif"

os.makedirs("datos", exist_ok=True)
os.makedirs(GALERIA_DIR, exist_ok=True)

def guardar_evento(evento):
    if os.path.exists(DATOS_FILE):
        with open(DATOS_FILE, "r", encoding="utf-8") as file:
            eventos = json.load(file)
    else:
        eventos = []
    eventos.append(evento)
    with open(DATOS_FILE, "w", encoding="utf-8") as file:
        json.dump(eventos, file, indent=4, ensure_ascii=False)

with st.sidebar:
    menu = option_menu(
        menu_title="Menú",
        options=["Inicio", "Crear evento", "Ver eventos", "Galería", "Contacto", "Testimonios"],
        icons=["house", "calendar-plus", "list-task", "camera", "envelope", "chat-square-text"],
        default_index=0,
        menu_icon="app-indicator",
        styles={
            "container": {"padding": "5px"},
            "icon": {"color": "#ff4b9b", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "5px",
                "--hover-color": "#ffe6f0",
            },
            "nav-link-selected": {"background-color": "#ff4b9b", "color": "white"},
        }
    )

if menu == "Inicio":
    st.image(LOGO_PATH, width=150)
    st.markdown("""
    <div style='text-align:center;'>
        <h1 style='color:#fff;'>Eventos York & Katy</h1>
        <h3 style='color:#ff69b4;'>❤️ El sabor del York. El estilo de Katy. La magia de tu evento.</h3>
        <p style='color:#fff;'>Somos una pareja apasionada por crear celebraciones memorables.</p>
        <ul style='color:#fff; font-size:16px; text-align:left; display:inline-block;'>
            <li><strong>York</strong>, cocinero con más de 15 años de experiencia.</li>
            <li><strong>Katy</strong>, organizadora y decoradora de eventos con gusto y estilo.</li>
        </ul>
        <p style='color:#7CFC00; font-weight:bold;'>✨ ¡Bienvenido! Explora el menú a la izquierda para comenzar.</p>
    </div>
    """, unsafe_allow_html=True)

elif menu == "Crear evento":
    st.markdown("<h2>📝 Registrar nuevo evento</h2>", unsafe_allow_html=True)

    nombre = st.text_input("Nombre del cliente")
    tipo = st.selectbox("Tipo de evento", ["Cumpleaños", "Boda", "Cena", "Evento Corporativo"])
    fecha = st.date_input("Fecha del evento")
    lugar = st.text_input("Lugar")
    comentario = st.text_area("Comentario adicional")
    enviado = st.form_submit_button("🚀 Guardar evento")

    if enviado:
        agregar_evento(fecha.strftime("%d/%m/%Y"), nombre, tipo, lugar, comentario)
        st.success("✅ Evento registrado con éxito.")

elif menu == "Ver eventos":
    st.markdown("<h2>📋 Lista de eventos registrados</h2>", unsafe_allow_html=True)
    if os.path.exists(DATOS_FILE):
        with open(DATOS_FILE, "r", encoding="utf-8") as file:
            eventos = json.load(file)
        for i, e in enumerate(eventos):
            st.markdown(f"""
            <div style='
                background: rgba(255, 255, 255, 0.92);
                backdrop-filter: blur(5px);
                padding: 20px;  
                border-radius: 14px;
                margin: 20px auto;
                max-width: 620px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.12);
                font-family: "Segoe UI", sans-serif;
                font-size: 16px;
            '>
                <p style="margin: 0; font-weight: bold; font-size: 18px; color: #000;">🗓️ <span style="color: #000;">{e['fecha']}</span></p>
                <ul style="list-style: none; padding-left: 0; margin-top: 10px;">
                    <li style="margin-bottom: 6px;"><span style="color: #000;"><strong>⭐ Cliente:</strong> {e['nombre']}</span></li>
                    <li style="margin-bottom: 6px;"><span style="color: #000;"><strong>🎉 Tipo:</strong> {e['tipo']}</span></li>
                    <li style="margin-bottom: 6px;"><span style="color: #000;"><strong>📍 Lugar:</strong> {e['lugar']}</span></li>
                    <li><span style="color: #000;"><strong>📝 Comentario:</strong> {e['comentario']}</span></li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

            # Botón para eliminar
            if st.button(f"🗑️ Eliminar evento {i+1}", key=f"delete_{i}"):
                eventos.pop(i)
                with open(DATOS_FILE, "w", encoding="utf-8") as file:
                    json.dump(eventos, file, indent=4, ensure_ascii=False)
                st.success("✅ Evento eliminado correctamente")
                st.rerun()

    else:
        st.markdown("<p class='text-light'>No hay eventos registrados todavía.</p>", unsafe_allow_html=True)

elif menu == "Galería":
    st.markdown("<h2>📸 Galería de eventos</h2>", unsafe_allow_html=True)
    imagenes = [img for img in os.listdir(GALERIA_DIR) if img.endswith((".png", ".jpg", ".jpeg"))]

    if imagenes:
        cols = st.columns(3)
        for index, imagen in enumerate(imagenes):
            path = os.path.join(GALERIA_DIR, imagen)
            with cols[index % 3]:
                st.image(Image.open(path), use_container_width=True)
    else:
        st.info("Aún no hay imágenes en la galería. Coloca fotos en la carpeta `/galeria/`.")

elif menu == "Contacto":
    st.markdown("<h2>📨 Contacta con nosotros</h2>", unsafe_allow_html=True)
    st.write("¿Tienes dudas o quieres reservar un evento? ¡Déjanos tu mensaje o contáctanos directamente:")

    with st.form("form_contacto"):
        nombre = st.text_input("Tu nombre")
        correo = st.text_input("Tu correo electrónico")
        asunto = st.text_input("Asunto")
        mensaje = st.text_area("Mensaje")
        enviar = st.form_submit_button("📧 Enviar mensaje")

        if enviar:
            if nombre and correo and mensaje:
                st.success("✅ ¡Gracias por tu mensaje! Te responderemos pronto.")
            else:
                st.warning("Por favor, completa todos los campos obligatorios.")

    st.markdown("---")
    st.markdown("### 📬 O contáctanos directamente:")
    st.markdown("""
    - 📧 [Enviar correo](mailto:Yorkat@gmail.com)
    - 💬 [Enviar WhatsApp](https://wa.me/34666030923?text=Hola%2C%20quiero%20información%20sobre%20un%20evento)
    """, unsafe_allow_html=True)

elif menu == "Testimonios":
    st.markdown("<h2>💬 Lo que dicen nuestros clientes</h2>", unsafe_allow_html=True)
    st.write("Gracias a quienes han confiado en nosotros para hacer de sus eventos algo inolvidable.")

    testimonios = [
        {
            "nombre": "María Gómez",
            "evento": "Boda en Palma",
            "mensaje": "¡Todo fue perfecto! La decoración, la comida y la atención fueron espectaculares. 100% recomendado."
        },
        {
            "nombre": "Carlos Ruiz",
            "evento": "Cumpleaños infantil",
            "mensaje": "Mi hijo quedó feliz y los invitados encantados. Katherine tiene un gusto increíble para la decoración."
        },
        {
            "nombre": "Laura y José",
            "evento": "Cena aniversario",
            "mensaje": "Un ambiente romántico, cálido y delicioso. York cocina como los dioses."
        }
    ]

    for t in testimonios:
        st.markdown(f"""
        <div style='
            background-color: rgba(255,255,255,0.85);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            max-width: 700px;
        '>
            <h4><span style='color:#000;'>{t["nombre"]}</span> – <span style='font-weight:normal; color:#000;'>{t["evento"]}</span></h4>
            <p style='color:#000;'>{t["mensaje"]}</p>
        </div>
        """, unsafe_allow_html=True)
















