from PIL import Image

def convert_image(input_path: str, output_path: str, target_format: str) -> None:
    fmt = target_format.lower()
    with Image.open(input_path) as img:
        if fmt in ['jpeg', 'jpg', 'bmp', 'tiff', 'tif', 'webp', 'dds']:
            img_to_save = img.convert('RGB')
        elif fmt in ['png', 'gif', 'ico']:
            img_to_save = img.convert('RGBA')
        else:
            raise ValueError(f"desteklenmeyen format: {target_format}")

        img_to_save.save(output_path, format=fmt.upper())
