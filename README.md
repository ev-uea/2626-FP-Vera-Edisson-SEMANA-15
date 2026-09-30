# Restaurante App - Sistema de Gestión Integrado (Semana 16)

**Estudiante:** Edisson Vera  
**Asignatura:** Programación Orientada a Objetos  
**Tema:** Manejo de Eventos en Tkinter  

---

## Descripción del Proyecto
`restaurante_app` es una aplicación de escritorio modular construida en Python con Tkinter. El sistema evoluciona incorporando el manejo integral de eventos sobre la Gestión de Usuarios con roles diferenciados (**Administrador**, **Empleado** y **Cliente**).

---

##  Eventos Implementados (`bind` vs `command`)

1. **`<<TreeviewSelect>>`**: Evento virtual asociado a la tabla de usuarios. Al seleccionar una fila, obtiene el ID y consulta al `RestauranteServicio` para cargar automáticamente los datos en el formulario sin exponer la contraseña en la tabla.
2. **`<Return>`**: Evento de teclado para las entradas de texto. Permite confirmar el registro rápido de usuarios al presionar la tecla `Enter`.
3. **`<Escape>`**: Evento de teclado global. Permite limpiar el formulario, restablecer los estados de los campos y deseleccionar la fila actual en el Treeview.
4. **`<<ComboboxSelected>>`**: Evento virtual del selector de rol. Actualiza dinámicamente un indicador visual informativo en la interfaz.
5. **`command=`**: Mantenido en los botones principales (`Registrar`, `Actualizar`, `Eliminar`, `Limpiar`) para separar eventos de selección de acciones directas.

---

##  Estructura del Proyecto

```text
restaurante_app/
│
├── assets/
│   └── logo.png                # Imagen del logotipo del sistema
│
├── datos/
│   ├── usuarios.json           # Base de datos local de usuarios
│   ├── productos.json          # Base de datos local de productos
│   └── ventas.json             # Registro de transacciones/ventas
│
├── modelos/
│   ├── __init__.py
│   └── usuario.py              # Clase/Modelo de datos para Usuario
│
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py     # Manejo de lectura/escritura JSON
│   └── restaurante_servicio.py # Lógica de negocio (Autenticación, CRUDs)
│
├── ui/
│   ├── __init__.py
│   ├── login_view.py           # Vista del formulario de inicio de sesión
│   └── main_view.py            # Vista principal (Panel de control con módulos)
│
├── main.py                     # Punto de entrada y controlador principal
└── README.md                   # Documentación del proyecto