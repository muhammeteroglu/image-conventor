import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from file_manager import get_output_path
from converter import convert_image

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ALLOWED_FORMATS = [
    'jpeg', 'jpg', 'png', 'bmp', 'gif',
    'tiff', 'tif', 'webp', 'ico', 'dds'
]

class ImageConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Image Converter")
        self.geometry("700x450")
        self.resizable(False, False)

        self.input_path = ctk.StringVar()
        self.target_format = ctk.StringVar(value=ALLOWED_FORMATS[0])
        self.preview_img = None
        control_frame = ctk.CTkFrame(self, width=260, corner_radius=10)
        control_frame.pack(side="left", padx=20, pady=20, fill="y")

        ctk.CTkLabel(control_frame, text="Görsel Seç", font=("Helvetica", 16)).pack(pady=(10,5))
        ctk.CTkEntry(control_frame, textvariable=self.input_path, width=200).pack(pady=5)
        ctk.CTkButton(control_frame, text="Dosya Seç", command=self.select_file).pack(pady=5)

        ctk.CTkLabel(control_frame, text="Hedef Format", font=("Helvetica", 16)).pack(pady=(20,5))
        ctk.CTkOptionMenu(control_frame, values=ALLOWED_FORMATS, variable=self.target_format).pack(pady=5)

        ctk.CTkButton(control_frame, text="Dönüştür", fg_color="#1F6AA5", command=self.convert).pack(pady=(30,5))

        preview_frame = ctk.CTkFrame(self, corner_radius=10)
        preview_frame.pack(side="right", padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(preview_frame, text="Önizleme", font=("Helvetica", 16)).pack(pady=(10,5))
        self.preview_label = ctk.CTkLabel(
            preview_frame,
            text="görsel seçilmedi",
            width=360, height=320,
            fg_color="#333333", corner_radius=8
        )
        self.preview_label.pack(pady=10)

    def select_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("All Images", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff;*.tif;*.webp;*.ico;*.dds")]
        )
        if path:
            self.input_path.set(path)
            self.show_preview(path)

    def show_preview(self, path):
        try:
            img = Image.open(path)
            resample_filter = (
                Image.Resampling.LANCZOS
                if hasattr(Image, "Resampling")
                else Image.LANCZOS
            )
            img.thumbnail((360, 320), resample_filter)
            self.preview_img = ImageTk.PhotoImage(img)
            self.preview_label.configure(image=self.preview_img, text="")
        except Exception as e:
            messagebox.showerror("Önizleme Hatası", f"Görsel yüklenemedi:\n{e}")

    def convert(self):
        inp = self.input_path.get().strip()
        fmt = self.target_format.get().strip().lower()
        if not inp or not os.path.isfile(inp):
            messagebox.showwarning('Uyarı', 'Lütfen geçerli bir görsel seçin.')
            return
        try:
            outp = get_output_path(inp, fmt)
            convert_image(inp, outp, fmt)
            messagebox.showinfo('Başarılı', f'Görsel başarıyla kaydedildi:\n{outp}')
        except Exception as e:
            messagebox.showerror('Hata', f'Dönüştürme sırasında hata oluştu:\n{e}')

def run_app():
    app = ImageConverterApp()
    app.mainloop()

if __name__ == "__main__":
    run_app()
