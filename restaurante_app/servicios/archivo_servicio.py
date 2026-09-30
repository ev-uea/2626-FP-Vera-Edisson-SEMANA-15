import json
import os
from modelos.usuario import Usuario

class ArchivoServicio:
    """Servicio encargado de la lectura y escritura de archivos JSON."""

    def __init__(self, ruta_usuarios: str, ruta_productos: str = "datos/productos.json", ruta_ventas: str = "datos/ventas.json") -> None:
        self.ruta_usuarios = ruta_usuarios
        self.ruta_productos = ruta_productos
        self.ruta_ventas = ruta_ventas

    def cargar_usuarios(self) -> list:
        """Carga los usuarios desde el archivo JSON."""
        if not os.path.exists(self.ruta_usuarios):
            return []

        try:
            with open(self.ruta_usuarios, "r", encoding="utf-8") as f:
                datos = json.load(f)
                usuarios = []
                for reg in datos:
                    if hasattr(Usuario, "from_dict"):
                        usuarios.append(Usuario.from_dict(reg))
                    elif hasattr(Usuario, "desde_diccionario"):
                        usuarios.append(Usuario.desde_diccionario(reg))
                    else:
                        usuarios.append(Usuario(**reg))
                return usuarios
        except Exception as e:
            print(f"Error al cargar usuarios: {e}")
            return []

    def guardar_usuarios(self, usuarios: list) -> bool:
        """Guarda la lista de usuarios en el archivo JSON."""
        try:
            datos = []
            for u in usuarios:
                if isinstance(u, dict):
                    datos.append(u)
                elif hasattr(u, "to_dict"):
                    datos.append(u.to_dict())
                else:
                    datos.append({
                        "identificacion": getattr(u, "identificacion", ""),
                        "nombre": getattr(u, "nombre", ""),
                        "correo": getattr(u, "correo", ""),
                        "clave": getattr(u, "clave", getattr(u, "contrasena", "")),
                        "rol": getattr(u, "rol", "Empleado")
                    })

            os.makedirs(os.path.dirname(self.ruta_usuarios), exist_ok=True)
            with open(self.ruta_usuarios, "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Error al guardar usuarios: {e}")
            return False

    def cargar_productos(self) -> list:
        if not os.path.exists(self.ruta_productos):
            return []
        try:
            with open(self.ruta_productos, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def cargar_ventas(self) -> list:
        if not os.path.exists(self.ruta_ventas):
            return []
        try:
            with open(self.ruta_ventas, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []