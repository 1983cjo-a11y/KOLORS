from PIL import ImageEnhance, ImageFilter, ImageOps

def process_image(img, estilo):

    img = img.convert("RGB")

    if estilo == "3D":
        # profundidade + contraste forte
        img = ImageEnhance.Contrast(img).enhance(2.2)
        img = ImageEnhance.Sharpness(img).enhance(2.0)
        img = ImageEnhance.Brightness(img).enhance(1.1)

    elif estilo == "Realista":
        # suavização + cor equilibrada
        img = img.filter(ImageFilter.SMOOTH_MORE)
        img = ImageEnhance.Color(img).enhance(1.4)
        img = ImageEnhance.Contrast(img).enhance(1.3)

    elif estilo == "Anime":
        # efeito desenho forte
        img = ImageOps.posterize(img, 3)  # reduz cores
        img = ImageEnhance.Color(img).enhance(2.0)
        img = img.filter(ImageFilter.SHARPEN)

    elif estilo == "Disney":
        # super vibrante + suave
        img = ImageEnhance.Color(img).enhance(2.5)
        img = ImageEnhance.Brightness(img).enhance(1.3)
        img = img.filter(ImageFilter.SMOOTH_MORE)

    return img
