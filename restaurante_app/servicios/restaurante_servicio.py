import datetime
from modelos.usuario import Usuario

class ObjetoAdaptador:
    """Permite acceso por punto (v.id_venta) tanto a diccionarios como a objetos."""
    def __init__(self, d):
        if isinstance(d, dict):
            for k, val in d.items():
                setattr(self, k, val)
        else:
            self.__dict__ = getattr(d, "__dict__", {})

    def __getattr__(self, name):
        return ""


class RestauranteServicio:
    """Servicio principal para la gestión integral de usuarios, productos y ventas."""

    def __init__(self, archivo_servicio) -> None:
        self.archivo_servicio = archivo_servicio
        self.usuarios = self.archivo_servicio.cargar_usuarios() if hasattr(self.archivo_servicio, "cargar_usuarios") else []
        self.productos = self.archivo_servicio.cargar_productos() if hasattr(self.archivo_servicio, "cargar_productos") else []
        self.ventas = self.archivo_servicio.cargar_ventas() if hasattr(self.archivo_servicio, "cargar_ventas") else []
        self.usuario_autenticado = None

    # --- AUTENTICACIÓN Y SESIÓN ---
    def autenticar_usuario(self, correo: str, clave: str):
        """Valida las credenciales de acceso."""
        correo = correo.strip().lower()
        clave = clave.strip()

        for usuario in self.usuarios:
            correo_usr = str(getattr(usuario, "correo", "")).strip().lower()
            clave_usr = str(getattr(usuario, "clave", getattr(usuario, "contrasena", ""))).strip()

            if correo_usr == correo and clave_usr == clave:
                self.usuario_autenticado = usuario
                return usuario

        self.usuario_autenticado = None
        return None

    def cerrar_sesion(self) -> None:
        """Limpia el usuario autenticado actual."""
        self.usuario_autenticado = None

    def logout(self) -> None:
        """Alias para cerrar_sesion."""
        self.cerrar_sesion()

    # --- MÉTODOS OBTENER ---
    def obtener_usuarios(self) -> list:
        return self.usuarios

    def obtener_usuario_por_id(self, usr_id: str):
        """Busca y retorna un usuario por su identificación."""
        for u in self.usuarios:
            if str(getattr(u, "identificacion", "")) == str(usr_id):
                return u
        return None

    def obtener_productos(self) -> list:
        return [ObjetoAdaptador(p) if isinstance(p, dict) else p for p in self.productos]

    def obtener_producto_por_codigo(self, codigo: str):
        """Busca y retorna un producto por su código."""
        for p in self.productos:
            cod_p = p.get("codigo", "") if isinstance(p, dict) else getattr(p, "codigo", "")
            if str(cod_p) == str(codigo):
                return ObjetoAdaptador(p) if isinstance(p, dict) else p
        return None

    def obtener_ventas(self) -> list:
        return [ObjetoAdaptador(v) if isinstance(v, dict) else v for v in self.ventas]

    # --- GESTIÓN DE USUARIOS ---
    def registrar_usuario(self, ident, nombre, correo, clave, rol) -> tuple[bool, str]:
        for u in self.usuarios:
            id_existente = str(getattr(u, "identificacion", ""))
            correo_existente = str(getattr(u, "correo", "")).strip().lower()
            if id_existente == str(ident) or correo_existente == str(correo).strip().lower():
                return False, "La identificación o correo ya se encuentra registrado."

        nuevo_usuario = Usuario(identificacion=str(ident), nombre=str(nombre), correo=str(correo), clave=str(clave), rol=str(rol))
        self.usuarios.append(nuevo_usuario)
        self.guardar_usuarios()
        return True, "Usuario registrado exitosamente."

    def agregar_usuario(self, usuario) -> bool:
        ident = getattr(usuario, "identificacion", "")
        nombre = getattr(usuario, "nombre", "")
        correo = getattr(usuario, "correo", "")
        clave = getattr(usuario, "clave", getattr(usuario, "contrasena", ""))
        rol = getattr(usuario, "rol", "Empleado")
        exito, _ = self.registrar_usuario(ident, nombre, correo, clave, rol)
        return exito

    def actualizar_usuario(self, ident, nombre=None, correo=None, clave=None, rol=None) -> tuple[bool, str]:
        if isinstance(ident, (dict, object)) and nombre is None:
            usr_obj = ident
            ident = getattr(usr_obj, "identificacion", "")
            nombre = getattr(usr_obj, "nombre", "")
            correo = getattr(usr_obj, "correo", "")
            clave = getattr(usr_obj, "clave", getattr(usr_obj, "contrasena", ""))
            rol = getattr(usr_obj, "rol", "Empleado")

        for i, u in enumerate(self.usuarios):
            if str(getattr(u, "identificacion", "")) == str(ident):
                self.usuarios[i] = Usuario(identificacion=str(ident), nombre=str(nombre), correo=str(correo), clave=str(clave), rol=str(rol))
                self.guardar_usuarios()
                return True, "Usuario actualizado correctamente."
        return False, "Usuario no encontrado."

    def eliminar_usuario(self, identificacion: str) -> tuple[bool, str]:
        for i, u in enumerate(self.usuarios):
            if str(getattr(u, "identificacion", "")) == str(identificacion):
                del self.usuarios[i]
                self.guardar_usuarios()
                return True, "Usuario eliminado correctamente."
        return False, "Usuario no encontrado."

    def guardar_usuarios(self) -> bool:
        if hasattr(self.archivo_servicio, "guardar_usuarios"):
            return self.archivo_servicio.guardar_usuarios(self.usuarios)
        return False

    # --- GESTIÓN DE PRODUCTOS ---
    def registrar_producto(self, codigo, nombre, categoria, precio, stock) -> tuple[bool, str]:
        for p in self.productos:
            cod_p = p.get("codigo", "") if isinstance(p, dict) else getattr(p, "codigo", "")
            if str(cod_p) == str(codigo):
                return False, f"El código '{codigo}' ya está registrado."

        nuevo_prod = {
            "codigo": str(codigo),
            "nombre": str(nombre),
            "categoria": str(categoria),
            "precio": float(precio),
            "stock": int(stock)
        }
        self.productos.append(nuevo_prod)
        self.guardar_productos()
        return True, "Producto registrado correctamente."

    def agregar_producto(self, producto) -> tuple[bool, str]:
        if isinstance(producto, dict):
            return self.registrar_producto(
                producto.get("codigo", ""), producto.get("nombre", ""),
                producto.get("categoria", ""), producto.get("precio", 0.0),
                producto.get("stock", 0)
            )
        return self.registrar_producto(
            getattr(producto, "codigo", ""), getattr(producto, "nombre", ""),
            getattr(producto, "categoria", ""), getattr(producto, "precio", 0.0),
            getattr(producto, "stock", 0)
        )

    def actualizar_producto(self, codigo, nombre=None, categoria=None, precio=None, stock=None) -> tuple[bool, str]:
        if isinstance(codigo, (dict, object)) and nombre is None:
            prod_obj = codigo
            codigo = prod_obj.get("codigo", "") if isinstance(prod_obj, dict) else getattr(prod_obj, "codigo", "")
            nombre = prod_obj.get("nombre", "") if isinstance(prod_obj, dict) else getattr(prod_obj, "nombre", "")
            categoria = prod_obj.get("categoria", "") if isinstance(prod_obj, dict) else getattr(prod_obj, "categoria", "")
            precio = prod_obj.get("precio", 0.0) if isinstance(prod_obj, dict) else getattr(prod_obj, "precio", 0.0)
            stock = prod_obj.get("stock", 0) if isinstance(prod_obj, dict) else getattr(prod_obj, "stock", 0)

        for i, p in enumerate(self.productos):
            cod_p = p.get("codigo", "") if isinstance(p, dict) else getattr(p, "codigo", "")
            if str(cod_p) == str(codigo):
                self.productos[i] = {
                    "codigo": str(codigo),
                    "nombre": str(nombre),
                    "categoria": str(categoria),
                    "precio": float(precio),
                    "stock": int(stock)
                }
                self.guardar_productos()
                return True, "Producto actualizado correctamente."
        return False, "Producto no encontrado."

    def eliminar_producto(self, codigo: str) -> tuple[bool, str]:
        for i, p in enumerate(self.productos):
            cod_p = p.get("codigo", "") if isinstance(p, dict) else getattr(p, "codigo", "")
            if str(cod_p) == str(codigo):
                del self.productos[i]
                self.guardar_productos()
                return True, "Producto eliminado correctamente."
        return False, "Producto no encontrado."

    def guardar_productos(self) -> bool:
        if hasattr(self.archivo_servicio, "guardar_productos"):
            return self.archivo_servicio.guardar_productos(self.productos)
        return False

    # --- GESTIÓN DE VENTAS ---
    def registrar_venta(self, usr_id: str, prod_cod: str, cantidad: int) -> tuple[bool, str]:
        producto_encontrado = None
        idx_prod = -1
        for idx, p in enumerate(self.productos):
            cod_p = p.get("codigo", "") if isinstance(p, dict) else getattr(p, "codigo", "")
            if str(cod_p) == str(prod_cod):
                producto_encontrado = p
                idx_prod = idx
                break

        if not producto_encontrado:
            return False, "El producto seleccionado no existe."

        nombre_prod = producto_encontrado.get("nombre", "Producto") if isinstance(producto_encontrado, dict) else getattr(producto_encontrado, "nombre", "Producto")
        precio_prod = float(producto_encontrado.get("precio", 0.0) if isinstance(producto_encontrado, dict) else getattr(producto_encontrado, "precio", 0.0))
        stock_actual = int(producto_encontrado.get("stock", 0) if isinstance(producto_encontrado, dict) else getattr(producto_encontrado, "stock", 0))

        if int(cantidad) > stock_actual:
            return False, f"Stock insuficiente. Disponible: {stock_actual}"

        if isinstance(self.productos[idx_prod], dict):
            self.productos[idx_prod]["stock"] = stock_actual - int(cantidad)
        else:
            setattr(self.productos[idx_prod], "stock", stock_actual - int(cantidad))
        self.guardar_productos()

        nombre_usr = "Usuario"
        for u in self.usuarios:
            id_u = getattr(u, "identificacion", "")
            if str(id_u) == str(usr_id):
                nombre_usr = getattr(u, "nombre", "Usuario")
                break

        total = precio_prod * int(cantidad)
        id_venta = f"V-{len(self.ventas) + 1:03d}"
        fecha_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        nueva_venta = {
            "id_venta": id_venta,
            "fecha": fecha_str,
            "usuario_id": usr_id,
            "usuario_nombre": nombre_usr,
            "producto_codigo": prod_cod,
            "producto_nombre": nombre_prod,
            "cantidad": int(cantidad),
            "precio_unitario": precio_prod,
            "total": total
        }

        self.ventas.append(nueva_venta)
        self.guardar_ventas()
        return True, f"Venta {id_venta} registrada por un total de ${total:.2f}."

    def guardar_ventas(self) -> bool:
        if hasattr(self.archivo_servicio, "guardar_ventas"):
            return self.archivo_servicio.guardar_ventas(self.ventas)
        return False