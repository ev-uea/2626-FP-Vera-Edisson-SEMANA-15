# Restaurante App - Semana 15: Manejo de Eventos y Callbacks

**Estudiante:** Edisson Valentin Vera Gamboa  
**Materia:** Programación Orientada a Objetos  
**Carrera:** Tecnologías de la Información - Universidad Estatal Amazónica  

---

## 1. Propósito de la Semana 15
En esta versión evolucionada de `restaurante_app`, se incorpora el módulo de **Ventas** para relacionar usuarios y productos en una transacción real. El objetivo principal es comprender y demostrar el fundamento básico del manejo de eventos utilizando botones con la propiedad `command=` asociados a funciones *callback*, manteniendo la arquitectura en capas desarrollada previamente.

---

## 2. Flujo de Manejo de Eventos Evidenciado

```text
USUARIO
   ↓ (Realiza clic en 'Registrar Venta')
BOTÓN / COMPONENTE (ttk.Button con command=self._cmd_registrar_venta)
   ↓
CALLBACK (_cmd_registrar_venta toma la selección de los Combobox)
   ↓
RestauranteServicio (valida existencia, valida cantidad y descuenta stock)
   ↓
PERSISTENCIA (guarda cambios en productos.json y ventas.json)
   ↓
RESPUESTA EN LA INTERFAZ (Actualiza la tabla Treeview y notifica al usuario)