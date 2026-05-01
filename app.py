import streamlit as st
from PIL import Image
import numpy as np
from io import BytesIO

# ===== CONFIG =====
st.set_page_config(page_title="Kolors", layout="centered")

# ===== TÍTULO =====
st.title("🎨 Kolors")

# ===== UPLOAD =====
uploaded_file = st.file_uploader("Envie uma imagem", type=["png", "jpg", "jpeg"])

# ===== ESTILO =====
estilo = st.selectbox("Estilo", ["3D", "Realista", "Anime", "Disney"])

# ===== PROCESSAMENTO SIMPLES (VERSÃO ESTÁVEL) =====
def process_image(img, estilo):
    arr = np.array(img).astype(np.float32)

    if estilo == "3D":
        arr *= 1.2
    elif estilo == "Realista":
        arr = arr * 1.1 + 10
    elif estilo == "Anime":
        arr *= 0.9
    elif estilo == "Disney":
        arr *= 1.3

    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

# ===== EXECUÇÃO =====
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Original")

    if st.button("Processar"):
        result = process_image(image, estilo)

        st.image(result, caption="Resultado")

        # download
        buf = BytesIO()
        result.save(buf, format="PNG")

        st.download_button(
            "Download",
            buf.getvalue(),
            file_name="kolors.png",
            mime="image/png"
        )
