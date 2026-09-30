class Usuario:
    """Representa a un usuario registrado en el sistema del restaurante."""

    def __init__(self, identificacion: str, nombre: str, correo: str, clave: str, rol: str = "Cliente") -> None:
        self.identificacion: str = identificacion
        self.nombre: str = nombre
        self.correo: str = correo
        self.clave: str = clave
        self.rol: str = rol

    def to_dict(self) -> dict:
        """Convierte el objeto Usuario en un diccionario para la persistencia JSON."""
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
            "clave": self.clave,
            "rol": self.rol
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Usuario":
        """Crea una instancia de Usuario a partir de un diccionario."""
        return cls(
            identificacion=data.get("identificacion", ""),
            nombre=data.get("nombre", ""),
            correo=data.get("correo", ""),
            clave=data.get("clave", ""),
            rol=data.get("rol", "Cliente")
        )