import sys
import os
import tkinter as tk
from tkinter import ttk

# Obtener directorio actual del archivo main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


class App(tk.Tk):
    """Clase principal de la aplicación que administra las vistas y servicios."""

    def __init__(self) -> None:
        super().__init__()

        self.title("Restaurante App - Sistema de Gestión")
        self.geometry("880x580")
        self.minsize(820, 520)

        # Ruta exacta a la carpeta assets
        assets_dir = os.path.join(BASE_DIR, "assets")

        # Cargar Ícono de ventana si existe icon.ico
        ruta_icono = os.path.join(assets_dir, "icon.ico")
        if os.path.exists(ruta_icono):
            try:
                self.iconbitmap(ruta_icono)
            except Exception:
                pass

        # Rutas de Persistencia JSON dentro de datos/
        ruta_prod = os.path.join(BASE_DIR, "datos", "productos.json")
        ruta_usr = os.path.join(BASE_DIR, "datos", "usuarios.json")
        ruta_ventas = os.path.join(BASE_DIR, "datos", "ventas.json")

        self.archivo_servicio = ArchivoServicio(ruta_prod, ruta_usr, ruta_ventas)
        self.restaurante_servicio = RestauranteServicio(self.archivo_servicio)

        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Instanciación de Vistas pasando assets_dir
        self.login_view = LoginView(
            parent=self.container,
            restaurante_servicio=self.restaurante_servicio,
            on_login_success=self.mostrar_main_view,
            assets_dir=assets_dir
        )

        self.main_view = MainView(
            parent=self.container,
            restaurante_servicio=self.restaurante_servicio,
            on_logout=self.mostrar_login_view,
            assets_dir=assets_dir
        )

        self.mostrar_login_view()

    def mostrar_login_view(self) -> None:
        self.main_view.pack_forget()
        self.login_view.pack(fill="both", expand=True)

    def mostrar_main_view(self) -> None:
        self.login_view.pack_forget()
        self.main_view.actualizar_datos_vista()
        self.main_view.pack(fill="both", expand=True)


def main() -> None:
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()