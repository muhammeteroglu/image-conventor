from pathlib import Path

# Desteklenen uzantılar
SUPPORTED_EXTS = [
    '.jpeg', '.jpg', '.png', '.bmp', '.gif',
    '.tiff', '.tif', '.webp', '.ico', '.dds'
]

def get_output_path(input_path: str, target_format: str) -> str:
    """
    input_path dosyasının bulunduğu klasörde 'new' adında bir alt klasör oluşturur
    ve aynı isimle, yalnızca uzantısı değişmiş çıktıyı o klasöre yazar.
    """
    p = Path(input_path)
    # Hedef klasörü belirle
    out_dir = p.parent / 'new'
    out_dir.mkdir(exist_ok=True)  # klasör yoksa yarat

    # Yeni dosya adı: orijinal isim, yeni uzantı
    new_name = p.with_suffix(f'.{target_format}').name
    return str(out_dir / new_name)

def list_image_files(directory: str, recursive: bool=False) -> list[str]:
    """
    directory içindeki (ve recursive=True ise altındaki) tüm resim dosyalarını döner.
    """
    p = Path(directory)
    iterator = p.rglob("*") if recursive else p.glob("*")
    return [
        str(fp) for fp in iterator
        if fp.is_file() and fp.suffix.lower() in SUPPORTED_EXTS
    ]