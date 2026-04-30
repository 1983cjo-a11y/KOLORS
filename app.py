import streamlit as st
from PIL import Image
import numpy as np
from io import BytesIO

# ===== CONFIG =====
st.set_page_config(page_title="Kolors", layout="centered")

# ===== IDIOMA AUTOMÁTICO =====
def detect_language():
    try:
        lang = st.headers.get("Accept-Language", "")
        if "pt" in lang:
            return "PT"
        elif "es" in lang:
            return "ES"
        else:
            return "EN"
    except:
        return "EN"

if "lang" not in st.session_state:
    st.session_state.lang = detect_language()

# ===== TEXTOS =====
TEXTS = {
    "PT": {
        "title": "🎨 Kolors",
        "upload": "Envie uma imagem",
        "style": "Estilo",
        "process": "Processar",
        "original": "Original",
        "result": "Resultado",
        "download": "Baixar imagem",
        "done": "Pronto!"
    },
    "EN": {
        "title": "🎨 Kolors",
        "upload": "Upload image",
        "style": "Style",
        "process": "Process",
        "original": "Original",
        "result": "Result",
        "download": "Download image",
        "done": "Done!"
    },
    "ES": {
        "title": "kolors"
