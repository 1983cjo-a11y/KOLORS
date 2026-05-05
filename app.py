import streamlit as st
from PIL import Image
import numpy as np
import cv2
from io import BytesIO

st.set_page_config(page_title="Kolors - 2D Real", layout="centered")

st.title("🎨 Kolors - Gráfico 2D Real")

uploaded_file = st.file_uploader(
    "Envie imagem (HQ, mangá, doujin)",
    type=["png", "jpg", "jpeg"]
)

# ===== DETECTAR SE É COLORIDO =====
def is_color(img_np):
    return len(img_np.shape) == 3 and img_np.shape[2] == 3

# ===== PROCESSAMENTO PRINCIPAL =====
def processar_2d_real(img):

    img_np = np.array(img)

    if is_color(img_np):
        # ===== COLORIDO =====

        # suavizar levemente (sem borrar)
        smooth = cv2.bilateralFilter(img_np, 7, 50, 50)

        # aumentar contraste
        lab = cv2.cvtColor(smooth, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)

        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        l = clahe.apply(l)

        lab = cv2.merge((l, a, b))
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)

        # sharpen leve
        kernel = np.array([
            [0, -1, 0],
            [-1, 5,-1],
            [0, -1, 0]
        ])

        final = cv2.filter2D(enhanced, -1, kernel)

    else:
        # ===== PRETO E BRANCO =====

        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

        # melhorar contraste local
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        contrast = clahe.apply(gray)

        # sharpen leve
        kernel = np.array([
            [0, -1, 0],
            [-1, 5,-1],
            [0, -1, 0]
        ])

        sharp = cv2.filter2D(contrast, -1, kernel)

        # voltar para RGB
        final = cv2.cvtColor(sharp, cv2.COLOR_GRAY2RGB)

    return final

# ===== EXECUÇÃO =====
if uploaded_file:

    image = Image.open(uploaded_file)
    st.image(image, caption="Original", use_column_width=True)

    if st.button("Aplicar 2D Real"):

        with st.spinner("Processando..."):

            resultado = processar_2d_real(image)

            final_img = Image.fromarray(resultado)

            st.image(final_img, caption="Resultado 2D Real", use_column_width=True)

            buf = BytesIO()
            final_img.save(buf, format="PNG")

            st.download_button(
                "Baixar imagem",
                buf.getvalue(),
                file_name="kolors_2d_real.png",
                mime="image/png"
            )
