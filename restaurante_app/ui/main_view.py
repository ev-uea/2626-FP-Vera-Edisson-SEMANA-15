import os
import tkinter as tk
from tkinter import ttk, messagebox
from servicios.restaurante_servicio import RestauranteServicio


class MainView(ttk.Frame):
    """Panel principal con gestión de Productos, consulta de Usuarios y módulo de Ventas."""

    def __init__(self, parent: tk.Widget, restaurante_servicio: RestauranteServicio, on_logout: callable,
                 assets_dir: str) -> None:
        super().__init__(parent)
        self.restaurante_servicio: RestauranteServicio = restaurante_servicio
        self.on_logout: callable = on_logout
        self.assets_dir: str = assets_dir

        self.logo_img = None
        self._cargar_recursos_visuales()
        self._crear_interfaz()

    def _cargar_recursos_visuales(self) -> None:
        """Ajusta dinámicamente el logo a un máximo de 40px para el encabezado superior."""
        ruta_logo = os.path.join(self.assets_dir, "logo.png")
        if os.path.exists(ruta_logo):
            try:
                img_raw = tk.PhotoImage(file=ruta_logo)
                ancho_original = img_raw.width()

                # Escalar para que mida máximo 40px en la barra de título
                tamano_objetivo = 40
                factor = max(1, ancho_original // tamano_objetivo)

                self.logo_img = img_raw.subsample(factor, factor)
            except Exception:
                self.logo_img = None

    def _crear_interfaz(self) -> None:
        # Encabezado (Header)
        header = ttk.Frame(self, padding=10)
        header.pack(fill="x", side="top")

        if self.logo_img:
            lbl_logo = ttk.Label(header, image=self.logo_img)
            lbl_logo.image = self.logo_img
            lbl_logo.pack(side="left", padx=(0, 10))

        self.lbl_bienvenida = ttk.Label(header, text="Bienvenido/a", font=("Helvetica", 13, "bold"))
        self.lbl_bienvenida.pack(side="left")

        btn_logout = ttk.Button(header, text="Cerrar Sesión", command=self._cerrar_sesion)
        btn_logout.pack(side="right")

        # Control de Pestañas (Notebook)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Sección Ventas (Semana 15 - Eventos)
        self.tab_ventas = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_ventas, text="Registro de Ventas")
        self._construir_pestana_ventas()

        # Sección Productos
        self.tab_productos = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_productos, text="Gestión de Productos")
        self._construir_pestana_productos()

        # Sección Usuarios
        self.tab_usuarios = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_usuarios, text="Usuarios Registrados")
        self._construir_pestana_usuarios()

    # --- PESTAÑA DE VENTAS ---
    def _construir_pestana_ventas(self) -> None:
        frame_form = ttk.LabelFrame(self.tab_ventas, text=" Registrar Nueva Venta ", padding=10)
        frame_form.pack(side="left", fill="y", padx=(0, 10))

        ttk.Label(frame_form, text="Seleccionar Cliente / Usuario:").pack(anchor="w", pady=(5, 2))
        self.cmb_venta_usuario = ttk.Combobox(frame_form, width=32, state="readonly")
        self.cmb_venta_usuario.pack(fill="x", pady=(0, 10))

        ttk.Label(frame_form, text="Seleccionar Producto:").pack(anchor="w", pady=(5, 2))
        self.cmb_venta_producto = ttk.Combobox(frame_form, width=32, state="readonly")
        self.cmb_venta_producto.pack(fill="x", pady=(0, 10))

        ttk.Label(frame_form, text="Cantidad:").pack(anchor="w", pady=(5, 2))
        self.ent_venta_cantidad = ttk.Entry(frame_form, width=34)
        self.ent_venta_cantidad.pack(fill="x", pady=(0, 15))
        self.ent_venta_cantidad.insert(0, "1")

        # BOTÓN REGISTRAR VENTA
        btn_registrar_venta = ttk.Button(
            frame_form,
            text="🛒 Registrar Venta",
            command=self._cmd_registrar_venta
        )
        btn_registrar_venta.pack(fill="x", pady=10)

        # Tabla de Historial
        frame_tabla = ttk.LabelFrame(self.tab_ventas, text=" Historial de Ventas ", padding=10)
        frame_tabla.pack(side="right", fill="both", expand=True)

        cols = ("id", "fecha", "usuario", "producto", "cant", "total")
        self.tree_ventas = ttk.Treeview(frame_tabla, columns=cols, show="headings")

        self.tree_ventas.heading("id", text="ID")
        self.tree_ventas.heading("fecha", text="Fecha / Hora")
        self.tree_ventas.heading("usuario", text="Cliente")
        self.tree_ventas.heading("producto", text="Producto")
        self.tree_ventas.heading("cant", text="Cant.")
        self.tree_ventas.heading("total", text="Total ($)")

        self.tree_ventas.column("id", width=50, anchor="center")
        self.tree_ventas.column("fecha", width=130, anchor="center")
        self.tree_ventas.column("usuario", width=130, anchor="w")
        self.tree_ventas.column("producto", width=140, anchor="w")
        self.tree_ventas.column("cant", width=50, anchor="center")
        self.tree_ventas.column("total", width=70, anchor="e")

        sc = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree_ventas.yview)
        self.tree_ventas.configure(yscrollcommand=sc.set)
        self.tree_ventas.pack(side="left", fill="both", expand=True)
        sc.pack(side="right", fill="y")

    # CALLBACK REGISTRAR VENTA
    def _cmd_registrar_venta(self) -> None:
        sel_usr = self.cmb_venta_usuario.get()
        sel_prod = self.cmb_venta_producto.get()
        cant_str = self.ent_venta_cantidad.get().strip()

        if not sel_usr or not sel_prod:
            messagebox.showwarning("Atención", "Debe seleccionar un usuario y un producto.")
            return

        try:
            cantidad = int(cant_str)
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un entero válido.")
            return

        usr_id = sel_usr.split(" - ")[0].strip()
        prod_cod = sel_prod.split(" - ")[0].strip()

        exito, mensaje = self.restaurante_servicio.registrar_venta(usr_id, prod_cod, cantidad)

        if exito:
            messagebox.showinfo("Resultado", mensaje)
            self.ent_venta_cantidad.delete(0, tk.END)
            self.ent_venta_cantidad.insert(0, "1")
            self.actualizar_datos_vista()
        else:
            messagebox.showwarning("Resultado", mensaje)

    # --- PESTAÑA DE PRODUCTOS ---
    def _construir_pestana_productos(self) -> None:
        frame_form = ttk.LabelFrame(self.tab_productos, text=" Datos del Producto ", padding=10)
        frame_form.pack(side="left", fill="y", padx=(0, 10))

        ttk.Label(frame_form, text="Código:").grid(row=0, column=0, sticky="w", pady=4)
        self.ent_codigo = ttk.Entry(frame_form, width=18)
        self.ent_codigo.grid(row=0, column=1, pady=4)

        ttk.Label(frame_form, text="Nombre:").grid(row=1, column=0, sticky="w", pady=4)
        self.ent_nombre = ttk.Entry(frame_form, width=18)
        self.ent_nombre.grid(row=1, column=1, pady=4)

        ttk.Label(frame_form, text="Categoría:").grid(row=2, column=0, sticky="w", pady=4)
        self.cmb_categoria = ttk.Combobox(frame_form, values=["Comida Rápida", "Bebidas", "Postres"], width=16)
        self.cmb_categoria.grid(row=2, column=1, pady=4)

        ttk.Label(frame_form, text="Precio ($):").grid(row=3, column=0, sticky="w", pady=4)
        self.ent_precio = ttk.Entry(frame_form, width=18)
        self.ent_precio.grid(row=3, column=1, pady=4)

        ttk.Label(frame_form, text="Stock:").grid(row=4, column=0, sticky="w", pady=4)
        self.ent_stock = ttk.Entry(frame_form, width=18)
        self.ent_stock.grid(row=4, column=1, pady=4)

        frame_botones = ttk.Frame(frame_form, padding=(0, 10, 0, 0))
        frame_botones.grid(row=5, column=0, columnspan=2, sticky="ew")

        ttk.Button(frame_botones, text="Registrar", command=self._cmd_registrar_prod).pack(fill="x", pady=2)
        ttk.Button(frame_botones, text="Actualizar", command=self._cmd_actualizar_prod).pack(fill="x", pady=2)
        ttk.Button(frame_botones, text="Eliminar", command=self._cmd_eliminar_prod).pack(fill="x", pady=2)

        frame_tabla = ttk.LabelFrame(self.tab_productos, text=" Catálogo Registrado ", padding=10)
        frame_tabla.pack(side="right", fill="both", expand=True)

        cols = ("codigo", "nombre", "categoria", "precio", "stock")
        self.tree_productos = ttk.Treeview(frame_tabla, columns=cols, show="headings")
        for col, text in zip(cols, ["Código", "Nombre", "Categoría", "Precio ($)", "Stock"]):
            self.tree_productos.heading(col, text=text)
        self.tree_productos.pack(fill="both", expand=True)

    def _cmd_registrar_prod(self) -> None:
        try:
            exito, msg = self.restaurante_servicio.registrar_producto(
                self.ent_codigo.get(), self.ent_nombre.get(), self.cmb_categoria.get(),
                float(self.ent_precio.get()), int(self.ent_stock.get())
            )
            messagebox.showinfo("Resultado", msg)
            if exito:
                self.actualizar_datos_vista()
        except ValueError:
            messagebox.showerror("Error", "Verifique los valores numéricos ingresados.")

    def _cmd_actualizar_prod(self) -> None:
        try:
            exito, msg = self.restaurante_servicio.actualizar_producto(
                self.ent_codigo.get(), self.ent_nombre.get(), self.cmb_categoria.get(),
                float(self.ent_precio.get()), int(self.ent_stock.get())
            )
            messagebox.showinfo("Resultado", msg)
            if exito:
                self.actualizar_datos_vista()
        except ValueError:
            messagebox.showerror("Error", "Verifique los valores numéricos ingresados.")

    def _cmd_eliminar_prod(self) -> None:
        exito, msg = self.restaurante_servicio.eliminar_producto(self.ent_codigo.get())
        messagebox.showinfo("Resultado", msg)
        if exito:
            self.actualizar_datos_vista()

    # --- PESTAÑA DE USUARIOS ---
    def _construir_pestana_usuarios(self) -> None:
        frame_tabla = ttk.LabelFrame(self.tab_usuarios, text=" Usuarios Registrados ", padding=10)
        frame_tabla.pack(fill="both", expand=True)

        cols = ("id", "nombre", "correo")
        self.tree_usuarios = ttk.Treeview(frame_tabla, columns=cols, show="headings")
        self.tree_usuarios.heading("id", text="ID / Cédula")
        self.tree_usuarios.heading("nombre", text="Nombre")
        self.tree_usuarios.heading("correo", text="Correo Electrónico")
        self.tree_usuarios.pack(fill="both", expand=True)

    # --- REFRESCO VISUAL ---
    def _actualizar_comboboxes_ventas(self) -> None:
        usrs = [f"{u.identificacion} - {u.nombre}" for u in self.restaurante_servicio.obtener_usuarios()]
        prods = [f"{p.codigo} - {p.nombre} (${p.precio:.2f} | Stock: {p.stock})" for p in
                 self.restaurante_servicio.obtener_productos()]

        self.cmb_venta_usuario["values"] = usrs
        self.cmb_venta_producto["values"] = prods

        if usrs and not self.cmb_venta_usuario.get():
            self.cmb_venta_usuario.current(0)
        if prods and not self.cmb_venta_producto.get():
            self.cmb_venta_producto.current(0)

    def _actualizar_tabla_ventas(self) -> None:
        for item in self.tree_ventas.get_children():
            self.tree_ventas.delete(item)
        for v in self.restaurante_servicio.obtener_ventas():
            self.tree_ventas.insert("", "end",
                                    values=(v.id_venta, v.fecha, v.usuario_nombre, v.producto_nombre, v.cantidad,
                                            f"{v.total:.2f}"))

    def _actualizar_tabla_productos(self) -> None:
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
        for p in self.restaurante_servicio.obtener_productos():
            self.tree_productos.insert("", "end", values=(p.codigo, p.nombre, p.categoria, f"{p.precio:.2f}", p.stock))

    def _actualizar_tabla_usuarios(self) -> None:
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)
        for u in self.restaurante_servicio.obtener_usuarios():
            self.tree_usuarios.insert("", "end", values=(u.identificacion, u.nombre, u.correo))

    def actualizar_datos_vista(self) -> None:
        usr = self.restaurante_servicio.usuario_autenticado
        if usr:
            self.lbl_bienvenida.config(text=f"Bienvenido/a, {usr.nombre}")
        self._actualizar_tabla_ventas()
        self._actualizar_tabla_productos()
        self._actualizar_tabla_usuarios()
        self._actualizar_comboboxes_ventas()

    def _cerrar_sesion(self) -> None:
        self.restaurante_servicio.cerrar_sesion()
        self.on_logout()