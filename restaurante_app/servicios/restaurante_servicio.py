from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio

class RestauranteServicio:
    """Servicio de negocio centralizado que administra las reglas y lógica del restaurante."""

    def __init__(self, archivo_servicio: ArchivoServicio) -> None:
        self.archivo_servicio: ArchivoServicio = archivo_servicio
        self.productos: list[Producto] = []
        self.usuarios: list[Usuario] = []
        self.ventas: list[Venta] = []
        self.usuario_autenticado: Usuario | None = None
        self.inicializar_datos()

    def inicializar_datos(self) -> None:
        self.productos = self.archivo_servicio.cargar_productos()
        self.usuarios = self.archivo_servicio.cargar_usuarios()
        self.ventas = self.archivo_servicio.cargar_ventas()

    def validar_acceso(self, identificacion: str, clave: str) -> tuple[bool, str]:
        id_clean = identificacion.strip()
        clave_clean = clave.strip()

        if not id_clean or not clave_clean:
            return False, "Por favor complete todos los campos requeridos."

        for usr in self.usuarios:
            if usr.identificacion.lower() == id_clean.lower() and usr.clave == clave_clean:
                self.usuario_autenticado = usr
                return True, f"Bienvenido/a, {usr.nombre}."

        return False, "Credenciales de acceso incorrectas."

    def cerrar_sesion(self) -> None:
        self.usuario_autenticado = None

    def obtener_productos(self) -> list[Producto]:
        return self.productos

    def obtener_usuarios(self) -> list[Usuario]:
        return self.usuarios

    def obtener_ventas(self) -> list[Venta]:
        return self.ventas

    def buscar_producto_por_codigo(self, codigo: str) -> Producto | None:
        for p in self.productos:
            if p.codigo.lower() == codigo.strip().lower():
                return p
        return None

    def buscar_usuario_por_id(self, usuario_id: str) -> Usuario | None:
        for u in self.usuarios:
            if u.identificacion.lower() == usuario_id.strip().lower():
                return u
        return None

    # Operaciones CRUD para Productos
    def registrar_producto(self, codigo: str, nombre: str, categoria: str, precio: float, stock: int) -> tuple[bool, str]:
        if self.buscar_producto_por_codigo(codigo) is not None:
            return False, f"El código '{codigo}' ya se encuentra registrado."
        try:
            nuevo = Producto(codigo, nombre, categoria, precio, stock)
            self.productos.append(nuevo)
            self.archivo_servicio.guardar_productos(self.productos)
            return True, f"Producto '{nuevo.nombre}' registrado correctamente."
        except ValueError as err:
            return False, str(err)

    def actualizar_producto(self, codigo: str, nombre: str, categoria: str, precio: float, stock: int) -> tuple[bool, str]:
        p = self.buscar_producto_por_codigo(codigo)
        if not p:
            return False, "Producto no encontrado."
        try:
            temp = Producto(codigo, nombre, categoria, precio, stock)
            p.nombre, p.categoria, p.precio, p.stock = temp.nombre, temp.categoria, temp.precio, temp.stock
            self.archivo_servicio.guardar_productos(self.productos)
            return True, f"Producto '{codigo}' actualizado correctamente."
        except ValueError as err:
            return False, str(err)

    def eliminar_producto(self, codigo: str) -> tuple[bool, str]:
        p = self.buscar_producto_por_codigo(codigo)
        if not p:
            return False, "Producto no encontrado."
        self.productos.remove(p)
        self.archivo_servicio.guardar_productos(self.productos)
        return True, "Producto eliminado con éxito."

    # Reglas de Negocio para el Registro de Ventas
    def registrar_venta(self, usuario_id: str, producto_codigo: str, cantidad: int) -> tuple[bool, str]:
        """
        Valida disponibilidad, descuenta stock, crea el registro de Venta
        y actualiza ambas persistencias JSON.
        """
        usuario = self.buscar_usuario_por_id(usuario_id)
        if not usuario:
            return False, "El usuario seleccionado no es válido."

        producto = self.buscar_producto_por_codigo(producto_codigo)
        if not producto:
            return False, "El producto seleccionado no existe."

        if cantidad <= 0:
            return False, "La cantidad ingresada debe ser mayor a cero."

        if producto.stock < cantidad:
            return False, f"Stock insuficiente. Quedan {producto.stock} unidades de {producto.nombre}."

        # Procesar la transacción
        producto.stock -= cantidad
        total_venta = producto.precio * cantidad
        id_venta = f"V{len(self.ventas) + 1:03d}"

        try:
            nueva_venta = Venta(
                id_venta=id_venta,
                usuario_id=usuario.identificacion,
                usuario_nombre=usuario.nombre,
                producto_codigo=producto.codigo,
                producto_nombre=producto.nombre,
                cantidad=cantidad,
                total=total_venta
            )

            self.ventas.append(nueva_venta)
            # Guardar ambos cambios en persistencia
            self.archivo_servicio.guardar_productos(self.productos)
            self.archivo_servicio.guardar_ventas(self.ventas)

            return True, f"Venta {id_venta} registrada exitosamente. Total a cobrar: ${total_venta:.2f}"
        except ValueError as err:
            producto.stock += cantidad  # Revertir descuento de stock si falla la instanciación
            return False, str(err)