import os
import tkinter as tk
from tkinter import ttk, messagebox
from servicios.restaurante_servicio import RestauranteServicio


class MainView(ttk.Frame):
    """Interfaz principal del sistema con manejo de eventos en la pestaña de Usuarios."""

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
        ruta_logo = os.path.join(self.assets_dir, "logo.png")
        if os.path.exists(ruta_logo):
            try:
                img_raw = tk.PhotoImage(file=ruta_logo)
                factor = max(1, img_raw.width() // 40)
                self.logo_img = img_raw.subsample(factor, factor)
            except Exception:
                self.logo_img = None

    def _crear_interfaz(self) -> None:
        # Encabezado Superior
        header = ttk.Frame(self, padding=10)
        header.pack(fill="x", side="top")

        if self.logo_img:
            lbl_logo = ttk.Label(header, image=self.logo_img)
            lbl_logo.image = self.logo_img
            lbl_logo.pack(side="left", padx=(0, 10))

        self.lbl_bienvenida = ttk.Label(header, text="Bienvenido/a", font=("Helvetica", 12, "bold"))
        self.lbl_bienvenida.pack(side="left")

        btn_logout = ttk.Button(header, text="Cerrar Sesión", command=self._cerrar_sesion)
        btn_logout.pack(side="right")

        # Pestañas Principales
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # 1. Pestaña Ventas
        self.tab_ventas = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_ventas, text="Registro de Ventas")
        self._construir_pestana_ventas()

        # 2. Pestaña Productos
        self.tab_productos = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_productos, text="Gestión de Productos")
        self._construir_pestana_productos()

        # 3. Pestaña Usuarios (Semana 16 - Gestión & Eventos)
        self.tab_usuarios = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_usuarios, text="Gestión de Usuarios")
        self._construir_pestana_usuarios()

    # ==========================================
    # PESTAÑA USUARIOS (MANEJO DE EVENTOS - SEMANA 16)
    # ==========================================
    def _construir_pestana_usuarios(self) -> None:
        # Formulario de Usuario
        frame_form = ttk.LabelFrame(self.tab_usuarios, text=" Datos del Usuario ", padding=10)
        frame_form.pack(side="left", fill="y", padx=(0, 10))

        ttk.Label(frame_form, text="Cédula / ID:").grid(row=0, column=0, sticky="w", pady=4)
        self.ent_usr_id = ttk.Entry(frame_form, width=20)
        self.ent_usr_id.grid(row=0, column=1, pady=4)

        ttk.Label(frame_form, text="Nombre:").grid(row=1, column=0, sticky="w", pady=4)
        self.ent_usr_nombre = ttk.Entry(frame_form, width=20)
        self.ent_usr_nombre.grid(row=1, column=1, pady=4)

        ttk.Label(frame_form, text="Correo:").grid(row=2, column=0, sticky="w", pady=4)
        self.ent_usr_correo = ttk.Entry(frame_form, width=20)
        self.ent_usr_correo.grid(row=2, column=1, pady=4)

        ttk.Label(frame_form, text="Contraseña:").grid(row=3, column=0, sticky="w", pady=4)
        self.ent_usr_clave = ttk.Entry(frame_form, width=20, show="*")
        self.ent_usr_clave.grid(row=3, column=1, pady=4)

        ttk.Label(frame_form, text="Rol:").grid(row=4, column=0, sticky="w", pady=4)
        self.cmb_usr_rol = ttk.Combobox(frame_form, values=["Cliente", "Empleado", "Administrador"], width=18,
                                        state="readonly")
        self.cmb_usr_rol.set("Cliente")
        self.cmb_usr_rol.grid(row=4, column=1, pady=4)

        # Etiqueta de Estado Visual para <<ComboboxSelected>>
        self.lbl_rol_info = ttk.Label(frame_form, text="Rol seleccionado: Cliente", font=("Helvetica", 8, "italic"),
                                      foreground="gray")
        self.lbl_rol_info.grid(row=5, column=0, columnspan=2, sticky="w", pady=(2, 8))

        # Botones con command=
        frame_btn = ttk.Frame(frame_form)
        frame_btn.grid(row=6, column=0, columnspan=2, sticky="ew", pady=5)

        ttk.Button(frame_btn, text="Registrar", command=self._cmd_registrar_usuario).pack(fill="x", pady=2)
        ttk.Button(frame_btn, text="Actualizar", command=self._cmd_actualizar_usuario).pack(fill="x", pady=2)
        ttk.Button(frame_btn, text="Eliminar", command=self._cmd_eliminar_usuario).pack(fill="x", pady=2)
        ttk.Button(frame_btn, text="Limpiar (Esc)", command=self._cmd_limpiar_formulario_usuario).pack(fill="x", pady=2)

        # Tabla Treeview de Usuarios
        frame_tabla = ttk.LabelFrame(self.tab_usuarios, text=" Usuarios Registrados ", padding=10)
        frame_tabla.pack(side="right", fill="both", expand=True)

        cols = ("id", "nombre", "correo", "rol")
        self.tree_usuarios = ttk.Treeview(frame_tabla, columns=cols, show="headings")

        self.tree_usuarios.heading("id", text="ID / Cédula")
        self.tree_usuarios.heading("nombre", text="Nombre")
        self.tree_usuarios.heading("correo", text="Correo Electrónico")
        self.tree_usuarios.heading("rol", text="Rol")

        self.tree_usuarios.column("id", width=90, anchor="center")
        self.tree_usuarios.column("nombre", width=140, anchor="w")
        self.tree_usuarios.column("correo", width=160, anchor="w")
        self.tree_usuarios.column("rol", width=100, anchor="center")

        sc_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree_usuarios.yview)
        self.tree_usuarios.configure(yscrollcommand=sc_y.set)

        self.tree_usuarios.pack(side="left", fill="both", expand=True)
        sc_y.pack(side="right", fill="y")

        # --- EVENT BINDINGS (SEMANA 16) ---
        # 1. Evento de selección en el Treeview
        self.tree_usuarios.bind("<<TreeviewSelect>>", self._on_treeview_usuario_selected)

        # 2. Evento del Combobox al cambiar de Rol
        self.cmb_usr_rol.bind("<<ComboboxSelected>>", self._on_combobox_rol_changed)

        # 3. Evento Tecla Enter (<Return>) en las entradas para registrar rápido
        for entry in (self.ent_usr_id, self.ent_usr_nombre, self.ent_usr_correo, self.ent_usr_clave):
            entry.bind("<Return>", self._on_key_return)

        # 4. Evento Tecla Escape (<Escape>) para limpiar el formulario en cualquier momento
        self.bind_all("<Escape>", self._on_key_escape)

    # --- CALLBACKS DE EVENTOS BIND() ---
    def _on_treeview_usuario_selected(self, event) -> None:
        """Callback <<TreeviewSelect>>: Carga el usuario seleccionado en el formulario desde el servicio."""
        selected_items = self.tree_usuarios.selection()
        if not selected_items:
            return

        item_id = selected_items[0]
        valores = self.tree_usuarios.item(item_id, "values")
        if not valores:
            return

        usr_id = valores[0]
        # Consulta el objeto completo desde el servicio para evitar exponer contraseñas en la tabla
        usr = self.restaurante_servicio.obtener_usuario_por_id(usr_id)
        if usr:
            self.ent_usr_id.configure(state="normal")
            self.ent_usr_id.delete(0, tk.END)
            self.ent_usr_id.insert(0, usr.identificacion)
            self.ent_usr_id.configure(state="disabled")  # Deshabilitar ID para edición

            self.ent_usr_nombre.delete(0, tk.END)
            self.ent_usr_nombre.insert(0, usr.nombre)

            self.ent_usr_correo.delete(0, tk.END)
            self.ent_usr_correo.insert(0, usr.correo)

            self.ent_usr_clave.delete(0, tk.END)
            self.ent_usr_clave.insert(0, usr.clave)

            self.cmb_usr_rol.set(usr.rol)
            self.lbl_rol_info.config(text=f"Rol seleccionado: {usr.rol}")

    def _on_combobox_rol_changed(self, event) -> None:
        """Callback <<ComboboxSelected>>: Responde visualmente al cambio de rol."""
        rol_sel = self.cmb_usr_rol.get()
        self.lbl_rol_info.config(text=f"Rol seleccionado: {rol_sel}")

    def _on_key_return(self, event) -> None:
        """Callback <Return>: Reutiliza el comando de registrar usuario."""
        self._cmd_registrar_usuario()

    def _on_key_escape(self, event) -> None:
        """Callback <Escape>: Reutiliza el comando de limpiar el formulario."""
        self._cmd_limpiar_formulario_usuario()

    # --- ACCIONES DE BOTONES (COMMAND=) ---
    def _cmd_registrar_usuario(self) -> None:
        ident = self.ent_usr_id.get()
        nombre = self.ent_usr_nombre.get()
        correo = self.ent_usr_correo.get()
        clave = self.ent_usr_clave.get()
        rol = self.cmb_usr_rol.get()

        exito, msg = self.restaurante_servicio.registrar_usuario(ident, nombre, correo, clave, rol)
        if exito:
            messagebox.showinfo("Éxito", msg)
            self._cmd_limpiar_formulario_usuario()
            self.actualizar_datos_vista()
        else:
            messagebox.showwarning("Atención", msg)

    def _cmd_actualizar_usuario(self) -> None:
        ident = self.ent_usr_id.get()
        nombre = self.ent_usr_nombre.get()
        correo = self.ent_usr_correo.get()
        clave = self.ent_usr_clave.get()
        rol = self.cmb_usr_rol.get()

        exito, msg = self.restaurante_servicio.actualizar_usuario(ident, nombre, correo, clave, rol)
        if exito:
            messagebox.showinfo("Éxito", msg)
            self._cmd_limpiar_formulario_usuario()
            self.actualizar_datos_vista()
        else:
            messagebox.showwarning("Atención", msg)

    def _cmd_eliminar_usuario(self) -> None:
        ident = self.ent_usr_id.get()
        if not ident:
            messagebox.showwarning("Atención", "Seleccione un usuario de la tabla para eliminar.")
            return

        confirmar = messagebox.askyesno("Confirmar Eliminación",
                                        f"¿Está seguro de eliminar al usuario con ID '{ident}'?")
        if confirmar:
            exito, msg = self.restaurante_servicio.eliminar_usuario(ident)
            if exito:
                messagebox.showinfo("Éxito", msg)
                self._cmd_limpiar_formulario_usuario()
                self.actualizar_datos_vista()
            else:
                messagebox.showwarning("Atención", msg)

    def _cmd_limpiar_formulario_usuario(self) -> None:
        self.ent_usr_id.configure(state="normal")
        self.ent_usr_id.delete(0, tk.END)
        self.ent_usr_nombre.delete(0, tk.END)
        self.ent_usr_correo.delete(0, tk.END)
        self.ent_usr_clave.delete(0, tk.END)
        self.cmb_usr_rol.set("Cliente")
        self.lbl_rol_info.config(text="Rol seleccionado: Cliente")
        if self.tree_usuarios.selection():
            self.tree_usuarios.selection_remove(self.tree_usuarios.selection())

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

        btn_registrar_venta = ttk.Button(frame_form, text="🛒 Registrar Venta", command=self._cmd_registrar_venta)
        btn_registrar_venta.pack(fill="x", pady=10)

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
            self.tree_usuarios.insert("", "end", values=(u.identificacion, u.nombre, u.correo, u.rol))

    def actualizar_datos_vista(self) -> None:
        usr = self.restaurante_servicio.usuario_autenticado
        if usr:
            self.lbl_bienvenida.config(text=f"Bienvenido/a, {usr.nombre} ({usr.rol})")

            # Control de Acceso: Solo Administrador tiene habilitada la pestaña de Usuarios
            if usr.rol == "Administrador":
                if self.tab_usuarios not in self.notebook.tabs():
                    self.notebook.add(self.tab_usuarios, text="Gestión de Usuarios")
            else:
                if str(self.tab_usuarios) in self.notebook.tabs():
                    self.notebook.forget(self.tab_usuarios)

        self._actualizar_tabla_ventas()
        self._actualizar_tabla_productos()
        self._actualizar_tabla_usuarios()
        self._actualizar_comboboxes_ventas()

    def _cerrar_sesion(self) -> None:
        self.restaurante_servicio.cerrar_sesion()
        self.on_logout()