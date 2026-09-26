import os
import tkinter as tk
from tkinter import ttk, messagebox
from servicios.restaurante_servicio import RestauranteServicio


class LoginView(ttk.Frame):
    """Vista del inicio de sesión con logo adaptativo y validación delegada a RestauranteServicio."""

    def __init__(self, parent: tk.Widget, restaurante_servicio: RestauranteServicio, on_login_success: callable,
                 assets_dir: str) -> None:
        super().__init__(parent, padding=20)
        self.restaurante_servicio: RestauranteServicio = restaurante_servicio
        self.on_login_success: callable = on_login_success
        self.assets_dir: str = assets_dir

        self.logo_img = None
        self._cargar_logo()
        self._crear_interfaz()

    def _cargar_logo(self) -> None:
        """Calcula dinámicamente la reducción para que el logo mida ~80px independientemente del tamaño original."""
        ruta_logo = os.path.join(self.assets_dir, "logo.png")
        if os.path.exists(ruta_logo):
            try:
                img_raw = tk.PhotoImage(file=ruta_logo)
                ancho_original = img_raw.width()

                # Calcular el divisor necesario para escalar a un tamaño objetivo de 80px
                tamano_objetivo = 80
                factor = max(1, ancho_original // tamano_objetivo)

                self.logo_img = img_raw.subsample(factor, factor)
            except Exception:
                self.logo_img = None

    def _crear_interfaz(self) -> None:
        frame_box = ttk.LabelFrame(self, text=" Acceso al Sistema ", padding=20)
        frame_box.place(relx=0.5, rely=0.5, anchor="center")

        if self.logo_img:
            lbl_logo = ttk.Label(frame_box, image=self.logo_img)
            lbl_logo.image = self.logo_img
            lbl_logo.pack(pady=(0, 10))

        ttk.Label(frame_box, text="Identificación / Cédula:").pack(anchor="w", pady=(5, 2))
        self.ent_usuario = ttk.Entry(frame_box, width=30)
        self.ent_usuario.pack(fill="x", pady=(0, 10))

        ttk.Label(frame_box, text="Contraseña:").pack(anchor="w", pady=(5, 2))
        self.ent_clave = ttk.Entry(frame_box, width=30, show="*")
        self.ent_clave.pack(fill="x", pady=(0, 15))

        btn_ingresar = ttk.Button(frame_box, text="Iniciar Sesión", command=self._cmd_ingresar)
        btn_ingresar.pack(fill="x", pady=5)

    def _cmd_ingresar(self) -> None:
        usr = self.ent_usuario.get()
        clave = self.ent_clave.get()

        exito, msg = self.restaurante_servicio.validar_acceso(usr, clave)

        if exito:
            messagebox.showinfo("Acceso Autorizado", msg)
            self.ent_usuario.delete(0, tk.END)
            self.ent_clave.delete(0, tk.END)
            self.on_login_success()
        else:
            messagebox.showwarning("Acceso Denegado", msg)