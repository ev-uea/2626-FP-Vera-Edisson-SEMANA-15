class Usuario:
    """Entidad que representa a los usuarios y personal del sistema del restaurante."""

    def __init__(self, identificacion: str, nombre: str, correo: str, clave: str) -> None:
        self.identificacion: str = identificacion.strip()
        self.nombre: str = nombre.strip()
        self.correo: str = correo.strip()
        self.clave: str = clave.strip()

    def a_diccionario(self) -> dict:
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
            "clave": self.clave
        }

    @staticmethod
    def desde_diccionario(datos: dict) -> "Usuario":
        return Usuario(
            identificacion=str(datos["identificacion"]),
            nombre=str(datos["nombre"]),
            correo=str(datos["correo"]),
            clave=str(datos["clave"])
        )