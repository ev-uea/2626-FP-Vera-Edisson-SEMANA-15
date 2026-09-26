from datetime import datetime


class Venta:
    """Entidad que representa una transacción de venta en el restaurante."""

    def __init__(self, id_venta: str, usuario_id: str, usuario_nombre: str,
                 producto_codigo: str, producto_nombre: str, cantidad: int,
                 total: float, fecha: str = None) -> None:

        if cantidad <= 0:
            raise ValueError("La cantidad vendida debe ser mayor a cero.")
        if total <= 0:
            raise ValueError("El total de la venta debe ser mayor a cero.")

        self.id_venta: str = id_venta.strip()
        self.usuario_id: str = usuario_id.strip()
        self.usuario_nombre: str = usuario_nombre.strip()
        self.producto_codigo: str = producto_codigo.strip()
        self.producto_nombre: str = producto_nombre.strip()
        self.cantidad: int = int(cantidad)
        self.total: float = float(total)
        self.fecha: str = fecha if fecha else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def a_diccionario(self) -> dict:
        return {
            "id_venta": self.id_venta,
            "usuario_id": self.usuario_id,
            "usuario_nombre": self.usuario_nombre,
            "producto_codigo": self.producto_codigo,
            "producto_nombre": self.producto_nombre,
            "cantidad": self.cantidad,
            "total": self.total,
            "fecha": self.fecha
        }

    @staticmethod
    def desde_diccionario(datos: dict) -> "Venta":
        return Venta(
            id_venta=str(datos["id_venta"]),
            usuario_id=str(datos["usuario_id"]),
            usuario_nombre=str(datos["usuario_nombre"]),
            producto_codigo=str(datos["producto_codigo"]),
            producto_nombre=str(datos["producto_nombre"]),
            cantidad=int(datos["cantidad"]),
            total=float(datos["total"]),
            fecha=str(datos.get("fecha", ""))
        )