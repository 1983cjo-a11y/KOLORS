import streamlit as st
from PIL import Image
import numpy as np
import cv2
from io import BytesIO

st.set_page_config(page_title="Kolors - Refinar Traços", layout="centered")

st.title("🖊️ Kolors - Refinar Traços de HQ")

uploaded_file = st.file_uploader("Envie uma imagem", type=["png", "jpg", "jpeg"])

# ===== REFINAR TRAÇOS =====
def refinar_tracos(img):

    img_np = np.array(img.convert("L"))

    # reduzir ruído
    blur = cv2.GaussianBlur(img_np, (3, 3), 0)

    # detectar bordas
    edges = cv2.Canny(blur, 50, 150)

    # engrossar linhas
    kernel = np.ones((2,2), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)

    # inverter (preto no branco)
    edges = cv2.bitwise_not(edges)

    return edges

# ===== EXECUÇÃO =====
if uploaded_file:

    image = Image.open(uploaded_file)
    st.image(image, caption="Original")

    if st.button("Refinar traços"):

        with st.spinner("Processando..."):

            refinado = refinar_tracos(image)

            # converter para RGB para exibir corretamente
            final = Image.fromarray(cv2.cvtColor(refinado, cv2.COLOR_GRAY2RGB))

            st.image(final, caption="Resultado")

            buf = BytesIO()
            final.save(buf, format="PNG")

            st.download_button(
                "Baixar imagem",
                buf.getvalue(),
                file_name="refinado.png"
            )
