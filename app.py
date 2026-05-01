from PIL import ImageEnhance, ImageFilter, ImageOps

def process_image(img, estilo):

    if estilo == "3D":
        # contraste forte + sombra
        img = ImageEnhance.Contrast(img).enhance(2.0)
        img = img.filter(ImageFilter.DETAIL)

    elif estilo == "Realista":
        # suaviza + melhora cores
        img = img.filter(ImageFilter.SMOOTH)
        img = ImageEnhance.Color(img).enhance(1.3)

    elif estilo == "Anime":
        # bordas + cores chapadas
        edges = img.filter(ImageFilter.FIND_EDGES)
        img = ImageOps.posterize(img, 3)
        img = Image.blend(img, edges, 0.3)

    elif estilo == "Disney":
        # cores vibrantes + brilho
        img = ImageEnhance.Color(img).enhance(1.8)
        img = ImageEnhance.Brightness(img).enhance(1.2)
        img = img.filter(ImageFilter.SMOOTH_MORE)

    return img
