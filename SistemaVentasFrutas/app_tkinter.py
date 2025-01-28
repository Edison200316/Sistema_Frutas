import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from datetime import datetime

# Conexión a la base de datos
def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="edi200316",
        database="frutas",
    )

# Funcion del CRUD para los productos
def agregar_producto():
    nombre = entry_nombre.get()
    precio = entry_precio.get()
    stock = entry_stock.get()

    if nombre and precio and stock:
        try:
            conn = conectar_bd()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO ventas_producto (nombre, precio, stock) VALUES (%s, %s, %s)", (nombre, precio, stock))
            conn.commit()
            messagebox.showinfo("Éxito", "Producto agregado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar producto: {e}")
        finally:
            conn.close()
        limpiar_campos_producto()
        mostrar_productos()
    else:
        messagebox.showerror("Error", "Todos los campos son obligatorios")

def actualizar_producto():
    producto_id = entry_id.get()
    nombre = entry_nombre.get()
    precio = entry_precio.get()
    stock = entry_stock.get()

    if producto_id and nombre and precio and stock:
        try:
            conn = conectar_bd()
            cursor = conn.cursor()
            cursor.execute("UPDATE ventas_producto SET nombre=%s, precio=%s, stock=%s WHERE id=%s", (nombre, precio, stock, producto_id))
            if cursor.rowcount == 0:
                raise ValueError("El ID no existe")
            conn.commit()
            messagebox.showinfo("Éxito", "Producto actualizado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar producto: {e}")
        finally:
            conn.close()
        limpiar_campos_producto()
        mostrar_productos()
    else:
        messagebox.showerror("Error", "Todos los campos son obligatorios")

def eliminar_producto():
    producto_id = entry_id.get()
    if producto_id:
        try:
            conn = conectar_bd()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ventas_producto WHERE id=%s", (producto_id,))
            if cursor.rowcount == 0:
                raise ValueError("El ID no existe")
            conn.commit()
            messagebox.showinfo("Éxito", "Producto eliminado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar producto: {e}")
        finally:
            conn.close()
        limpiar_campos_producto()
        mostrar_productos()
    else:
        messagebox.showerror("Error", "Ingrese un ID válido")

def mostrar_productos():
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ventas_producto")
        rows = cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Error", f"Error al mostrar productos: {e}")
        rows = []
    finally:
        conn.close()

    listbox_productos.delete(0, tk.END)
    for row in rows:
        listbox_productos.insert(tk.END, f"ID: {row[0]}, Nombre: {row[1]}, Precio: {row[2]}, Stock: {row[3]}")

def limpiar_campos_producto():
    entry_id.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_precio.delete(0, tk.END)
    entry_stock.delete(0, tk.END)

# Funcion del CRUD para los clientes
def agregar_cliente():
    nombre = entry_nombre_cliente.get()
    telefono = entry_telefono_cliente.get()
    email = entry_email_cliente.get()

    if nombre and telefono and email:
        try:
            conn = conectar_bd()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO ventas_cliente (nombre, telefono, email) VALUES (%s, %s, %s)", (nombre, telefono, email))
            conn.commit()
            messagebox.showinfo("Éxito", "Cliente agregado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar cliente: {e}")
        finally:
            conn.close()
        limpiar_campos_cliente()
        mostrar_clientes()
    else:
        messagebox.showerror("Error", "Todos los campos son obligatorios")

def actualizar_cliente():
    cliente_id = entry_id_cliente.get()
    nombre = entry_nombre_cliente.get()
    telefono = entry_telefono_cliente.get()
    email = entry_email_cliente.get()

    if cliente_id and nombre and telefono and email:
        try:
            conn = conectar_bd()
            cursor = conn.cursor()
            cursor.execute("UPDATE ventas_cliente SET nombre=%s, telefono=%s, email=%s WHERE id=%s", (nombre, telefono, email, cliente_id))
            conn.commit()
            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
            else:
                messagebox.showwarning("Atención", "No se encontró un cliente con ese ID")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar cliente: {e}")
        finally:
            conn.close()
        limpiar_campos_cliente()
        mostrar_clientes()
    else:
        messagebox.showerror("Error", "Todos los campos son obligatorios")

def eliminar_cliente():
    cliente_id = entry_id_cliente.get()

    if cliente_id:
        try:
            conn = conectar_bd()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ventas_cliente WHERE id=%s", (cliente_id,))
            conn.commit()
            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
            else:
                messagebox.showwarning("Atención", "No se encontró un cliente con ese ID")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar cliente: {e}")
        finally:
            conn.close()
        limpiar_campos_cliente()
        mostrar_clientes()
    else:
        messagebox.showerror("Error", "El campo ID es obligatorio")

def mostrar_clientes():
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ventas_cliente")
        rows = cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Error", f"Error al mostrar clientes: {e}")
        rows = []
    finally:
        conn.close()

    listbox_clientes.delete(0, tk.END)
    for row in rows:
        listbox_clientes.insert(tk.END, f"ID: {row[0]}, Nombre: {row[1]}, Email: {row[2]}, Teléfono: {row[3]}")

def limpiar_campos_cliente():
    entry_id_cliente.delete(0, tk.END)
    entry_nombre_cliente.delete(0, tk.END)
    entry_telefono_cliente.delete(0, tk.END)
    entry_email_cliente.delete(0, tk.END)

# Funcion del CRUD para las ventas
def agregar_venta():
    producto_id = entry_id_producto_venta.get()
    cliente_id = entry_id_cliente_venta.get()
    cantidad = entry_cantidad_venta.get()

    if producto_id and cliente_id and cantidad:
        try:
            conn = conectar_bd()
            cursor = conn.cursor()
            # Para verificar si el producto existe
            cursor.execute("SELECT precio FROM ventas_producto WHERE id = %s", (producto_id,))
            producto = cursor.fetchone()
            if not producto:
                raise ValueError("El ID del producto no existe.")
            precio_producto = producto[0]
            # Verificamos si el cliente existe
            cursor.execute("SELECT id FROM ventas_cliente WHERE id = %s", (cliente_id,))
            cliente = cursor.fetchone()
            if not cliente:
                raise ValueError("El ID del cliente no existe.")
            
            # Para calcular el total
            total = precio_producto * int(cantidad)
            
            #Para obtener la fecha actual
            fecha_venta = datetime.now()

            # Para insertar la venta en la base de datos
            cursor.execute("INSERT INTO ventas_venta (producto_id, cliente_id, cantidad, total, fecha) VALUES (%s, %s, %s, %s, %s)", 
                           (producto_id, cliente_id, cantidad, total, fecha_venta))
            conn.commit()

            messagebox.showinfo("Éxito", f"Venta registrada correctamente. Total: {total}")

        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar la venta: {e}")
        finally:
            conn.close()

        limpiar_campos_venta()
        mostrar_ventas()
    else:
        messagebox.showerror("Error", "Todos los campos son obligatorios")

# Función para mostrar las ventas
def mostrar_ventas():
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT ventas_venta.id, ventas_cliente.nombre, ventas_producto.nombre, ventas_venta.cantidad, ventas_venta.total, ventas_venta.fecha "
                       "FROM ventas_venta "
                       "JOIN ventas_cliente ON ventas_venta.cliente_id = ventas_cliente.id "
                       "JOIN ventas_producto ON ventas_venta.producto_id = ventas_producto.id")
        rows = cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Error", f"Error al mostrar ventas: {e}")
        rows = []
    finally:
        conn.close()

    listbox_ventas.delete(0, tk.END)
    for row in rows:
        listbox_ventas.insert(tk.END, f"ID Venta: {row[0]}, Cliente: {row[1]}, Producto: {row[2]}, Cantidad: {row[3]}, Total: ${row[4]}, Fecha: {row[5]}")

def limpiar_campos_venta():
    entry_id_producto_venta.delete(0, tk.END)
    entry_id_cliente_venta.delete(0, tk.END)
    entry_cantidad_venta.delete(0, tk.END)


# Configuración de la ventana principal
root = tk.Tk()
root.title("Sistema de Ventas de Frutas")
root.geometry("900x700")
root.configure(bg="#f7f7f7")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Apartado para los Productos
tab_productos = tk.Frame(notebook, bg="#ffffff")
notebook.add(tab_productos, text="Productos")

frame_form_productos = tk.Frame(tab_productos, bg="#ffffff", pady=10)
frame_form_productos.pack(pady=20)

fields_productos = ["ID", "Nombre", "Precio", "Stock"]
entries_productos = {}
for field in fields_productos:
    label = tk.Label(frame_form_productos, text=f"{field}:", bg="#ffffff", font=("Arial", 12))
    label.pack(anchor="w", padx=10, pady=5)
    entry = tk.Entry(frame_form_productos, font=("Arial", 12), width=30)
    entry.pack(anchor="w", padx=10, pady=5)
    entries_productos[field] = entry

entry_id = entries_productos["ID"]
entry_nombre = entries_productos["Nombre"]
entry_precio = entries_productos["Precio"]
entry_stock = entries_productos["Stock"]

frame_buttons_productos = tk.Frame(tab_productos, bg="#f7f7f7")
frame_buttons_productos.pack(pady=10)

buttons_productos = [
    ("Agregar Producto", agregar_producto),
    ("Actualizar Producto", actualizar_producto),
    ("Eliminar Producto", eliminar_producto),
    ("Mostrar Productos", mostrar_productos)
]

for text, command in buttons_productos:
    btn = tk.Button(frame_buttons_productos, text=text, command=command, font=("Arial", 12), bg="#4CAF50", fg="#ffffff", relief="flat", width=20)
    btn.pack(pady=5)

frame_list_productos = tk.Frame(tab_productos, bg="#ffffff")
frame_list_productos.pack(pady=20)

listbox_productos = tk.Listbox(frame_list_productos, font=("Arial", 12), width=60, height=15)
listbox_productos.pack(side="left", padx=10)

scrollbar_productos = tk.Scrollbar(frame_list_productos)
scrollbar_productos.pack(side="right", fill="y")
listbox_productos.config(yscrollcommand=scrollbar_productos.set)
scrollbar_productos.config(command=listbox_productos.yview)

# Apartado para los Clientes
tab_clientes = tk.Frame(notebook, bg="#ffffff")
notebook.add(tab_clientes, text="Clientes")

frame_form_clientes = tk.Frame(tab_clientes, bg="#ffffff", pady=10)
frame_form_clientes.pack(pady=20)

fields_clientes = ["ID", "Nombre", "Teléfono", "Email"]  
entries_clientes = {}
for field in fields_clientes:
    label = tk.Label(frame_form_clientes, text=f"{field}:", bg="#ffffff", font=("Arial", 12))
    label.pack(anchor="w", padx=10, pady=5)
    entry = tk.Entry(frame_form_clientes, font=("Arial", 12), width=30)
    entry.pack(anchor="w", padx=10, pady=5)
    entries_clientes[field] = entry

entry_id_cliente = entries_clientes["ID"]
entry_nombre_cliente = entries_clientes["Nombre"]
entry_telefono_cliente = entries_clientes["Teléfono"]
entry_email_cliente = entries_clientes["Email"] 

frame_buttons_clientes = tk.Frame(tab_clientes, bg="#f7f7f7", pady=10)
frame_buttons_clientes.pack(pady=20)

buttons_clientes = [
    ("Agregar Cliente", agregar_cliente),
    ("Actualizar Cliente", actualizar_cliente),
    ("Eliminar Cliente", eliminar_cliente),
    ("Mostrar Clientes", mostrar_clientes)
]

for text, command in buttons_clientes:
    btn = tk.Button(frame_buttons_clientes, text=text, command=command, font=("Arial", 12), bg="#4CAF50", fg="#ffffff", relief="flat", width=20)
    btn.pack(pady=5)

frame_list_clientes = tk.Frame(tab_clientes, bg="#ffffff")
frame_list_clientes.pack(pady=20)

listbox_clientes = tk.Listbox(frame_list_clientes, font=("Arial", 12), width=60, height=15)
listbox_clientes.pack(side="left", padx=10)

scrollbar_clientes = tk.Scrollbar(frame_list_clientes)
scrollbar_clientes.pack(side="right", fill="y")
listbox_clientes.config(yscrollcommand=scrollbar_clientes.set)
scrollbar_clientes.config(command=listbox_clientes.yview)

# Apartado para las Ventas
tab_ventas = tk.Frame(notebook, bg="#ffffff")
notebook.add(tab_ventas, text="Ventas")

frame_form_ventas = tk.Frame(tab_ventas, bg="#ffffff", pady=10)
frame_form_ventas.pack(pady=20)

fields_ventas = ["ID Producto", "ID Cliente", "Cantidad"]
entries_ventas = {}
for field in fields_ventas:
    label = tk.Label(frame_form_ventas, text=f"{field}:", bg="#ffffff", font=("Arial", 12))
    label.pack(anchor="w", padx=10, pady=5)
    entry = tk.Entry(frame_form_ventas, font=("Arial", 12), width=30)
    entry.pack(anchor="w", padx=10, pady=5)
    entries_ventas[field] = entry

entry_id_producto_venta = entries_ventas["ID Producto"]
entry_id_cliente_venta = entries_ventas["ID Cliente"]
entry_cantidad_venta = entries_ventas["Cantidad"]

frame_buttons_ventas = tk.Frame(tab_ventas, bg="#f7f7f7")
frame_buttons_ventas.pack(pady=10)

buttons_ventas = [
    ("Agregar Venta", agregar_venta),
    ("Mostrar Ventas", mostrar_ventas)
]

for text, command in buttons_ventas:
    btn = tk.Button(frame_buttons_ventas, text=text, command=command, font=("Arial", 12), bg="#4CAF50", fg="#ffffff", relief="flat", width=20)
    btn.pack(pady=5)

frame_list_ventas = tk.Frame(tab_ventas, bg="#ffffff")
frame_list_ventas.pack(pady=20)

listbox_ventas = tk.Listbox(frame_list_ventas, font=("Arial", 12), width=60, height=15)
listbox_ventas.pack(side="left", padx=10)

scrollbar_ventas = tk.Scrollbar(frame_list_ventas)
scrollbar_ventas.pack(side="right", fill="y")
listbox_ventas.config(yscrollcommand=scrollbar_ventas.set)
scrollbar_ventas.config(command=listbox_ventas.yview)

root.mainloop()









