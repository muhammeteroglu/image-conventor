import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from file_manager import get_output_path, list_image_files
from converter import convert_image, FILTERS

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ALLOWED_FORMATS = [ext.strip('.') for ext in ['.jpeg','.jpg','.png','.bmp','.gif','.tiff','.tif','.webp','.ico','.dds']]

class ImageConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Advanced Image Converter")
        self.geometry("1000x600")
        self.resizable(False, False)

        # --- Değişkenler ---
        self.input_path = ctk.StringVar()
        self.is_batch = ctk.BooleanVar(value=False)
        self.is_recursive = ctk.BooleanVar(value=False)
        self.target_format = ctk.StringVar(value=ALLOWED_FORMATS[0])
        # işleme seçenekleri
        self.resize_w = ctk.IntVar(value=0)
        self.resize_h = ctk.IntVar(value=0)
        self.rotate = ctk.DoubleVar(value=0.0)
        self.filter = ctk.StringVar(value="None")
        self.wm_text = ctk.StringVar(value="")
        self.wm_pos = ctk.StringVar(value="bottom-right")

        self.preview_img = None
        self.file_list = []

        # --- Layout ---
        ctrl = ctk.CTkFrame(self, width=300, corner_radius=8)
        ctrl.pack(side="left", padx=10, pady=10, fill="y")

        # Batch seçenekleri
        ctk.CTkLabel(ctrl, text="Batch Modu", font=("Helvetica",14)).pack(pady=(5,0))
        ctk.CTkCheckBox(ctrl, text="Klasör Dönüştür", variable=self.is_batch).pack(anchor="w", padx=10)
        ctk.CTkCheckBox(ctrl, text="Alt Klasörleri de Dahil Et", variable=self.is_recursive).pack(anchor="w", padx=30)

        # Dosya/Klasör seçimi
        ctk.CTkButton(ctrl, text="Girdi Seç", command=self.select_file).pack(pady=(10,5))

        # Dönüştürme formatı
        ctk.CTkLabel(ctrl, text="Hedef Format", font=("Helvetica",14)).pack(pady=(15,0))
        ctk.CTkOptionMenu(ctrl, values=ALLOWED_FORMATS, variable=self.target_format).pack()

        # İşlem Seçenekleri — ince bir çizgi gibi göstermek için CTkFrame kullanalım
        separator = ctk.CTkFrame(ctrl, height=2, fg_color="#555555")
        separator.pack(fill="x", pady=10)
        ctk.CTkLabel(ctrl, text="İşleme Seçenekleri", font=("Helvetica",14)).pack(pady=(5,0))

        # Yeniden boyutlandırma
        size_frame = ctk.CTkFrame(ctrl)
        size_frame.pack(pady=5, padx=10, fill="x")
        ctk.CTkLabel(size_frame, text="Resize W:").grid(row=0,column=0,sticky="e")
        ctk.CTkEntry(size_frame, textvariable=self.resize_w, width=50).grid(row=0,column=1)
        ctk.CTkLabel(size_frame, text="H:").grid(row=0,column=2)
        ctk.CTkEntry(size_frame, textvariable=self.resize_h, width=50).grid(row=0,column=3)

        # Rotate
        rt_frame = ctk.CTkFrame(ctrl)
        rt_frame.pack(pady=5, padx=10, fill="x")
        ctk.CTkLabel(rt_frame, text="Rotate°:").pack(side="left")
        ctk.CTkEntry(rt_frame, textvariable=self.rotate, width=50).pack(side="left", padx=5)

        # Filter
        ctk.CTkLabel(ctrl, text="Filter:").pack(pady=(5,0))
        ctk.CTkOptionMenu(ctrl, values=list(FILTERS.keys()), variable=self.filter).pack()

        # Watermark
        ctk.CTkLabel(ctrl, text="Watermark Metni:").pack(pady=(5,0))
        ctk.CTkEntry(ctrl, textvariable=self.wm_text).pack(padx=10, fill="x")
        ctk.CTkLabel(ctrl, text="WM Pozisyon:").pack(pady=(5,0))
        ctk.CTkOptionMenu(ctrl, values=[
            "top-left","top-right","bottom-left","bottom-right"
        ], variable=self.wm_pos).pack()

        # Convert butonu
        ctk.CTkButton(ctrl, text="İşlemi Başlat", fg_color="#1F6AA5", command=self.convert).pack(pady=20)

        # Sağ panel: Önizleme ve log
        right = ctk.CTkFrame(self, corner_radius=8)
        right.pack(side="right", padx=10, pady=10, fill="both", expand=True)

        ctk.CTkLabel(right, text="Önizleme", font=("Helvetica",16)).pack(pady=(10,0))
        self.preview_label = ctk.CTkLabel(
            right, text="Henüz seçim yok", width=560, height=360,
            fg_color="#333333", corner_radius=8
        )
        self.preview_label.pack(pady=10)

        self.log_box = ctk.CTkTextbox(right, height=100, state="disabled")
        self.log_box.pack(fill="x", padx=10, pady=(0,10))

    def select_file(self):
        """Tekli veya batch modda girdi seçimi yapar ve önizleme ile listeyi günceller."""
        if self.is_batch.get():
            d = filedialog.askdirectory()
            if not d:
                return
            self.input_path.set(d)
            self.file_list = list_image_files(d, self.is_recursive.get())
            self._log(f"{len(self.file_list)} dosya bulundu.")
            if self.file_list:
                self.show_preview(self.file_list[0])
            else:
                self.preview_label.configure(image=None, text="Batch modu: dosya bulunamadı")
        else:
            f = filedialog.askopenfilename(
                filetypes=[("All Images","*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff;*.tif;*.webp;*.ico;*.dds")]
            )
            if not f:
                return
            self.input_path.set(f)
            self.file_list = [f]
            self.show_preview(f)

    def show_preview(self, path):
        try:
            img = Image.open(path)
            img.thumbnail((560, 360), Image.Resampling.LANCZOS if hasattr(Image, "Resampling") else Image.LANCZOS)
            self.preview_img = ImageTk.PhotoImage(img)
            self.preview_label.configure(image=self.preview_img, text="")
        except Exception as e:
            messagebox.showerror("Önizleme Hatası", f"{e}")

    def convert(self):
        inp_list = self.file_list
        if not inp_list:
            messagebox.showwarning("Uyarı","Önce giriş seçin.")
            return

        opts = {}
        if self.resize_w.get()>0 and self.resize_h.get()>0:
            opts["resize"] = (self.resize_w.get(), self.resize_h.get())
        if self.rotate.get()!=0.0:
            opts["rotate"] = self.rotate.get()
        if f := self.filter.get():
            opts["filter"] = f
        if wm := self.wm_text.get().strip():
            opts["watermark_text"] = wm
            opts["watermark_pos"] = self.wm_pos.get()

        success = 0
        for p in inp_list:
            try:
                outp = get_output_path(p, self.target_format.get())
                convert_image(p, outp, self.target_format.get(), options=opts)
                success += 1
                self._log(f"✔ {os.path.basename(p)} → {os.path.basename(outp)}")
            except Exception as e:
                self._log(f"✖ {os.path.basename(p)}: {e}")

        messagebox.showinfo("Bitti", f"{success}/{len(inp_list)} dosya başarıyla işlendi.")

    def _log(self, text: str):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", text + "\n")
        self.log_box.configure(state="disabled")
        self.log_box.see("end")

def run_app():
    app = ImageConverterApp()
    app.mainloop()

if __name__ == "__main__":
    run_app()
