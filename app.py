import streamlit as st
from PIL import Image
import numpy as np
import cv2
import pytesseract
from io import BytesIO

st.set_page_config(page_title="Kolors - Refinar Traços", layout="centered")

st.title("🖊️ Kolors - Refinar Traços de HQ")

uploaded_file = st.file_uploader("Envie uma imagem", type=["png", "jpg", "jpeg"])

# ===== DETECTAR TEXTO =====
def detectar_texto(img):
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    boxes = []

    for i in range(len(data["text"])):
        try:
            if int(data["conf"][i]) > 60:
                x = data["left"][i]
                y = data["top"][i]
                w = data["width"][i]
                h = data["height"][i]
                boxes.append((x, y, w, h))
        except:
            pass

    return boxes

# ===== REFINAR TRAÇOS =====
def refinar_tracos(img):

    img_np = np.array(img.convert("L"))

    # reduzir ruído
    blur = cv2.GaussianBlur(img_np, (3, 3), 0)

    # destacar bordas
    edges = cv2.Canny(blur, 50, 150)

    # engrossar linhas
    kernel = np.ones((2,2), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)

    # inverter (preto no branco)
    edges = cv2.bitwise_not(edges)

    return edges

# ===== RESTAURAR TEXTO =====
def restaurar_texto(original, refinado, boxes):

    orig_np = np.array(original.convert("RGB"))
    ref_np = cv2.cvtColor(refinado, cv2.COLOR_GRAY2RGB)

    for (x, y, w, h) in boxes:
        ref_np[y:y+h, x:x+w] = orig_np[y:y+h, x:x+w]

    return Image.fromarray(ref_np)

# ===== EXECUÇÃO =====
if uploaded_file:

    image = Image.open(uploaded_file)
    st.image(image, caption="Original")

    if st.button("Refinar traços"):

        with st.spinner("Processando..."):

            texto_boxes = detectar_texto(image)

            refinado = refinar_tracos(image)

            final = restaurar_texto(image, refinado, texto_boxes)

            st.image(final, caption="Resultado")

            buf = BytesIO()
            final.save(buf, format="PNG")

            st.download_button(
                "Baixar imagem",
                buf.getvalue(),
                file_name="refinado.png"
            )
