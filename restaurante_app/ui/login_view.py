import os
import tkinter as tk
from tkinter import ttk, messagebox


class LoginView(ttk.Frame):
    """Vista del formulario de inicio de sesión."""

    def __init__(self, parent, on_login_success, assets_dir="assets", restaurante_servicio=None, servicio=None, *args, **kwargs) -> None:
        # Extraer parámetros personalizados para evitar TclError con super().__init__()
        if "restaurante_servicio" in kwargs:
            restaurante_servicio = kwargs.pop("restaurante_servicio")
        if "servicio" in kwargs:
            servicio = kwargs.pop("servicio")

        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.on_login_success = on_login_success
        self.assets_dir = assets_dir
        self.servicio = servicio or restaurante_servicio

        self._crear_interfaz()

    def _crear_interfaz(self) -> None:
        frame_centrado = ttk.Frame(self, padding="20")
        frame_centrado.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Cargar logo en PNG usando tk.PhotoImage y redimensionar con subsample
        ruta_logo = os.path.join(self.assets_dir, "logo.png")
        if os.path.exists(ruta_logo):
            try:
                img_original = tk.PhotoImage(file=ruta_logo)
                # Escala ajustada (divide entre 5 el tamaño original del logo)
                self.logo_img = img_original.subsample(5, 5)
                lbl_logo = ttk.Label(frame_centrado, image=self.logo_img)
                lbl_logo.pack(pady=(0, 10))
            except Exception:
                pass

        ttk.Label(frame_centrado, text="Iniciar Sesión", font=("Helvetica", 16, "bold")).pack(pady=10)

        # Campo Correo
        ttk.Label(frame_centrado, text="Correo Electrónico:").pack(anchor=tk.W, pady=(10, 2))
        self.ent_correo = ttk.Entry(frame_centrado, width=35)
        self.ent_correo.pack(fill=tk.X, pady=(0, 10))

        # Campo Contraseña
        ttk.Label(frame_centrado, text="Contraseña:").pack(anchor=tk.W, pady=(5, 2))
        self.ent_clave = ttk.Entry(frame_centrado, width=35, show="*")
        self.ent_clave.pack(fill=tk.X, pady=(0, 15))

        # Evento de tecla Enter
        self.ent_clave.bind("<Return>", lambda event: self._procesar_login())

        # Botón Ingresar
        btn_ingresar = ttk.Button(frame_centrado, text="Ingresar", command=self._procesar_login)
        btn_ingresar.pack(fill=tk.X, pady=10)

    def _procesar_login(self) -> None:
        correo = self.ent_correo.get().strip()
        clave = self.ent_clave.get().strip()

        if not correo or not clave:
            messagebox.showwarning("Campos vacíos", "Por favor ingrese el correo y la contraseña.")
            return

        if self.servicio:
            usuario = self.servicio.autenticar_usuario(correo, clave)
            if usuario:
                try:
                    self.on_login_success(usuario)
                except TypeError:
                    self.on_login_success()
            else:
                messagebox.showerror("Error de autenticación", "Correo o contraseña incorrectos.")
        else:
            try:
                self.on_login_success(None)
            except TypeError:
                self.on_login_success()