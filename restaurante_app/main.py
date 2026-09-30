import os
import tkinter as tk
from tkinter import ttk

from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


class App(tk.Tk):
    """Clase principal de la aplicación."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Restaurante App - Sistema de Gestión")
        self.geometry("1024x600")
        self.minsize(800, 500)

        # Configuración de rutas
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.assets_dir = os.path.join(self.base_dir, "assets")
        self.datos_dir = os.path.join(self.base_dir, "datos")

        # Inicialización del servicio de archivos
        self.archivo_servicio = ArchivoServicio(
            ruta_usuarios=os.path.join(self.datos_dir, "usuarios.json"),
            ruta_productos=os.path.join(self.datos_dir, "productos.json"),
            ruta_ventas=os.path.join(self.datos_dir, "ventas.json")
        )
        self.restaurante_servicio = RestauranteServicio(self.archivo_servicio)

        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.mostrar_login()

    def mostrar_login(self) -> None:
        """Muestra la vista de inicio de sesión."""
        for widget in self.container.winfo_children():
            widget.destroy()

        self.login_view = LoginView(
            parent=self.container,
            on_login_success=self.mostrar_main_view,
            assets_dir=self.assets_dir,
            restaurante_servicio=self.restaurante_servicio
        )
        self.login_view.pack(fill="both", expand=True)

    def mostrar_main_view(self, usuario=None) -> None:
        """Muestra la vista principal tras la autenticación."""
        for widget in self.container.winfo_children():
            widget.destroy()

        if usuario:
            self.restaurante_servicio.usuario_autenticado = usuario

        self.main_view = MainView(
            parent=self.container,
            restaurante_servicio=self.restaurante_servicio,
            on_logout=self.mostrar_login,
            assets_dir=self.assets_dir
        )
        self.main_view.pack(fill="both", expand=True)

        if hasattr(self.main_view, "actualizar_datos_vista"):
            self.main_view.actualizar_datos_vista()


def main() -> None:
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()