from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont
from typing import Optional, Tuple, Dict

# Desteklenen filtreler
FILTERS = {
    "None": None,
    "BLUR": ImageFilter.BLUR,
    "CONTOUR": ImageFilter.CONTOUR,
    "DETAIL": ImageFilter.DETAIL,
    "SHARPEN": ImageFilter.SHARPEN,
    "SMOOTH": ImageFilter.SMOOTH,
    "EMBOSS": ImageFilter.EMBOSS,
    "GRAYSCALE": "GRAYSCALE",
}

def process_image(img: Image.Image, options: Dict) -> Image.Image:
    """
    options: {
      "resize": (width:int, height:int),
      "rotate": angle_in_degrees:float,
      "filter": one_of_FILTERS_keys,
      "watermark_text": str,
      "watermark_pos": one_of("top-left","top-right","bottom-left","bottom-right")
    }
    """
    # 1) Yeniden boyutlandırma
    if opts := options.get("resize"):
        resample = Image.Resampling.LANCZOS if hasattr(Image, "Resampling") else Image.LANCZOS
        img = img.resize(opts, resample)

    # 2) Döndürme
    if angle := options.get("rotate"):
        img = img.rotate(angle, expand=True)

    # 3) Filtre
    f = options.get("filter", "None")
    if FILTERS.get(f) and f != "None":
        if f == "GRAYSCALE":
            img = img.convert("L").convert("RGBA")
        else:
            img = img.filter(FILTERS[f])

    # 4) Watermark
    wm = options.get("watermark_text")
    if wm:
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()

        # metin genişlik/yükseklik hesaplama
        try:
            w, h = font.getsize(wm)
        except AttributeError:
            bbox = draw.textbbox((0, 0), wm, font=font)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]

        # konum belirleme
        positions = {
            "top-left":     (10, 10),
            "top-right":    (img.width  - w - 10, 10),
            "bottom-left":  (10, img.height - h - 10),
            "bottom-right": (img.width  - w - 10, img.height - h - 10),
        }
        px, py = positions.get(options.get("watermark_pos", "bottom-right"), (10,10))

        # yarı saydam beyaz metin
        draw.text((px, py), wm, font=font, fill=(255,255,255,128))

    return img

def convert_image(
    input_path: str,
    output_path: str,
    target_format: str,
    options: Optional[Dict] = None
) -> None:
    fmt = target_format.lower()
    with Image.open(input_path) as img:
        # önce işleme uygula
        if options:
            img = process_image(img, options)

        # renk modu dönüşümü
        if fmt in ['jpeg','jpg','bmp','tiff','tif','webp','dds']:
            img = img.convert('RGB')
        elif fmt in ['png','gif','ico']:
            img = img.convert('RGBA')
        else:
            raise ValueError(f"Desteklenmeyen format: {target_format}")

        img.save(output_path, format=fmt.upper())
