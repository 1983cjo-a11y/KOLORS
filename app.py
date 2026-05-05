import streamlit as st
from PIL import Image
import numpy as np
import cv2
from io import BytesIO

st.set_page_config(page_title="Kolors - Refinar Traços", layout="centered")

st.title("🖊️ Kolors - Refinar Traços de HQ")

uploaded_file = st.file_uploader("Envie uma imagem (HQ, mangá, doujin)", type=["png", "jpg", "jpeg"])

# ===== REFINAR TRAÇOS (VERSÃO MELHORADA) =====
def refinar_tracos(img):

    img_np = np.array(img.convert("RGB"))

    # suavizar sem perder bordas
    smooth = cv2.bilateralFilter(img_np, d=9, sigmaColor=75, sigmaSpace=75)

    # aumentar nitidez (sharpen)
    kernel = np.array([
        [0, -1, 0],
        [-1, 5,-1],
        [0, -1, 0]
    ])

    sharpen = cv2.filter2D(smooth, -1, kernel)

    return sharpen

# ===== EXECUÇÃO =====
if uploaded_file:

    image = Image.open(uploaded_file)
    st.image(image, caption="Imagem Original", use_column_width=True)

    if st.button("Refinar traços"):

        with st.spinner("Melhorando os traços..."):

            refinado = refinar_tracos(image)

            final = Image.fromarray(refinado)

            st.image(final, caption="Resultado Refinado", use_column_width=True)

            # download
            buf = BytesIO()
            final.save(buf, format="PNG")

            st.download_button(
                "Baixar imagem refinada",
                buf.getvalue(),
                file_name="kolors_refinado.png",
                mime="image/png"
            )
