import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import webbrowser

# Conexión a la base de datos
def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="edi200316",
        database="frutas",
    )

# Funciones del CRUD para los productos
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

    for row in tree_productos.get_children():
        tree_productos.delete(row)
    for row in rows:
        tree_productos.insert("", tk.END, values=row)

def limpiar_campos_producto():
    entry_id.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_precio.delete(0, tk.END)
    entry_stock.delete(0, tk.END)

# Funciones del CRUD para los clientes
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

    for row in tree_clientes.get_children():
        tree_clientes.delete(row)
    for row in rows:
        tree_clientes.insert("", tk.END, values=row)

def limpiar_campos_cliente():
    entry_id_cliente.delete(0, tk.END)
    entry_nombre_cliente.delete(0, tk.END)
    entry_telefono_cliente.delete(0, tk.END)
    entry_email_cliente.delete(0, tk.END)

# Funciones del CRUD para las ventas
def agregar_venta():
    producto_id = entry_id_producto_venta.get()
    cliente_id = entry_id_cliente_venta.get()
    cantidad = entry_cantidad_venta.get()

    if producto_id and cliente_id and cantidad:
        try:
            conn = conectar_bd()
            cursor = conn.cursor()
            cursor.execute("SELECT precio FROM ventas_producto WHERE id = %s", (producto_id,))
            producto = cursor.fetchone()
            if not producto:
                raise ValueError("El ID del producto no existe.")
            precio_producto = producto[0]
            cursor.execute("SELECT id FROM ventas_cliente WHERE id = %s", (cliente_id,))
            cliente = cursor.fetchone()
            if not cliente:
                raise ValueError("El ID del cliente no existe.")
            
            total = precio_producto * int(cantidad)
            fecha_venta = datetime.now()

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

    for row in tree_ventas.get_children():
        tree_ventas.delete(row)
    for row in rows:
        tree_ventas.insert("", tk.END, values=row)

def limpiar_campos_venta():
    entry_id_producto_venta.delete(0, tk.END)
    entry_id_cliente_venta.delete(0, tk.END)
    entry_cantidad_venta.delete(0, tk.END)

# Función para generar factura
def generar_factura():
    venta_id = entry_id_venta.get()

    if not venta_id:
        messagebox.showerror("Error", "Ingrese un ID de venta válido")
        return

    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.id, c.nombre, c.email, p.nombre, v.cantidad, v.total, v.fecha
            FROM ventas_venta v
            JOIN ventas_cliente c ON v.cliente_id = c.id
            JOIN ventas_producto p ON v.producto_id = p.id
            WHERE v.id = %s
        """, (venta_id,))
        
        venta = cursor.fetchone()
        
        if not venta:
            raise ValueError("El ID de la venta no existe")
        
        factura_id, cliente, email, producto, cantidad, total, fecha = venta
        nombre_archivo = f"factura_{factura_id}.pdf"
        
        c = canvas.Canvas(nombre_archivo, pagesize=letter)
        c.setFont("Helvetica-Bold", 16)
        
        # Encabezado de la factura
        c.drawString(100, 750, "Tienda de Frutas - Factura")
        c.setFont("Helvetica", 12)
        c.drawString(100, 730, f"Factura ID: {factura_id}")
        c.drawString(100, 710, f"Fecha: {fecha}")
        c.drawString(100, 690, f"Cliente: {cliente}")
        c.drawString(100, 670, f"Email: {email}")
        c.drawString(100, 650, f"Producto: {producto}")
        c.drawString(100, 630, f"Cantidad: {cantidad}")
        c.drawString(100, 610, f"Total: ${total}")
        
        # Línea separadora
        c.line(100, 600, 500, 600)
        
        # Pie de página
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, 580, "Gracias por su compra!")
        
        c.save()
        
        messagebox.showinfo("Éxito", f"Factura generada: {nombre_archivo}")
        webbrowser.open_new_tab(nombre_archivo)
    
    except Exception as e:
        messagebox.showerror("Error", f"Error al generar la factura: {e}")
    
    finally:
        conn.close()

# Configuración de la ventana principal
root = tk.Tk()
root.title("Sistema de Ventas de Frutas")
root.geometry("1000x700")
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

columns_productos = ("ID", "Nombre", "Precio", "Stock")
tree_productos = ttk.Treeview(frame_list_productos, columns=columns_productos, show="headings", height=10)
tree_productos.heading("ID", text="ID")
tree_productos.heading("Nombre", text="Nombre")
tree_productos.heading("Precio", text="Precio")
tree_productos.heading("Stock", text="Stock")
tree_productos.pack(side="left", fill="both", expand=True)

scrollbar_productos = ttk.Scrollbar(frame_list_productos, orient="vertical", command=tree_productos.yview)
scrollbar_productos.pack(side="right", fill="y")
tree_productos.configure(yscrollcommand=scrollbar_productos.set)

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

columns_clientes = ("ID", "Nombre", "Teléfono", "Email")
tree_clientes = ttk.Treeview(frame_list_clientes, columns=columns_clientes, show="headings", height=10)
tree_clientes.heading("ID", text="ID")
tree_clientes.heading("Nombre", text="Nombre")
tree_clientes.heading("Teléfono", text="Teléfono")
tree_clientes.heading("Email", text="Email")
tree_clientes.pack(side="left", fill="both", expand=True)

scrollbar_clientes = ttk.Scrollbar(frame_list_clientes, orient="vertical", command=tree_clientes.yview)
scrollbar_clientes.pack(side="right", fill="y")
tree_clientes.configure(yscrollcommand=scrollbar_clientes.set)

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

columns_ventas = ("ID Venta", "Cliente", "Producto", "Cantidad", "Total", "Fecha")
tree_ventas = ttk.Treeview(frame_list_ventas, columns=columns_ventas, show="headings", height=10)
tree_ventas.heading("ID Venta", text="ID Venta")
tree_ventas.heading("Cliente", text="Cliente")
tree_ventas.heading("Producto", text="Producto")
tree_ventas.heading("Cantidad", text="Cantidad")
tree_ventas.heading("Total", text="Total")
tree_ventas.heading("Fecha", text="Fecha")
tree_ventas.pack(side="left", fill="both", expand=True)

scrollbar_ventas = ttk.Scrollbar(frame_list_ventas, orient="vertical", command=tree_ventas.yview)
scrollbar_ventas.pack(side="right", fill="y")
tree_ventas.configure(yscrollcommand=scrollbar_ventas.set)

# Apartado para las Facturas
tab_facturas = tk.Frame(notebook, bg="#ffffff")
notebook.add(tab_facturas, text="Facturas")

frame_form_facturas = tk.Frame(tab_facturas, bg="#ffffff", pady=10)
frame_form_facturas.pack(pady=20)

label_id_venta = tk.Label(frame_form_facturas, text="ID Venta:", bg="#ffffff", font=("Arial", 12))
label_id_venta.pack(anchor="w", padx=10, pady=5)
entry_id_venta = tk.Entry(frame_form_facturas, font=("Arial", 12), width=30)
entry_id_venta.pack(anchor="w", padx=10, pady=5)

frame_buttons_facturas = tk.Frame(tab_facturas, bg="#f7f7f7")
frame_buttons_facturas.pack(pady=10)

btn_factura = tk.Button(frame_buttons_facturas, text="Generar Factura", command=generar_factura, font=("Arial", 12), bg="#FF5733", fg="#ffffff", relief="flat", width=20)
btn_factura.pack(pady=5)

root.mainloop()