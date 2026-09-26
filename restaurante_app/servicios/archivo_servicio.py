import json
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta

class ArchivoServicio:
    """Servicio encargado de la lectura y escritura de archivos JSON para la aplicación."""

    def __init__(self, ruta_productos: str, ruta_usuarios: str, ruta_ventas: str) -> None:
        self.ruta_productos: str = ruta_productos
        self.ruta_usuarios: str = ruta_usuarios
        self.ruta_ventas: str = ruta_ventas

    def guardar_productos(self, lista_productos: list[Producto]) -> bool:
        try:
            datos = [prod.a_diccionario() for prod in lista_productos]
            with open(self.ruta_productos, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False

    def cargar_productos(self) -> list[Producto]:
        productos: list[Producto] = []
        try:
            with open(self.ruta_productos, "r", encoding="utf-8") as archivo:
                contenido = json.load(archivo)
                for reg in contenido:
                    if isinstance(reg, dict):
                        productos.append(Producto.desde_diccionario(reg))
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return productos

    def cargar_usuarios(self) -> list[Usuario]:
        usuarios: list[Usuario] = []
        try:
            with open(self.ruta_usuarios, "r", encoding="utf-8") as archivo:
                contenido = json.load(archivo)
                for reg in contenido:
                    if isinstance(reg, dict):
                        usuarios.append(Usuario.desde_diccionario(reg))
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return usuarios

    def guardar_ventas(self, lista_ventas: list[Venta]) -> bool:
        try:
            datos = [v.a_diccionario() for v in lista_ventas]
            with open(self.ruta_ventas, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False

    def cargar_ventas(self) -> list[Venta]:
        ventas: list[Venta] = []
        try:
            with open(self.ruta_ventas, "r", encoding="utf-8") as archivo:
                contenido = json.load(archivo)
                for reg in contenido:
                    if isinstance(reg, dict):
                        ventas.append(Venta.desde_diccionario(reg))
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return ventas