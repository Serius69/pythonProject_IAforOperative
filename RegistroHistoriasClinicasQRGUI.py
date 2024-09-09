import sqlite3
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Conectar a la base de datos
conn = sqlite3.connect('historias_clinicas.db')
cursor = conn.cursor()


# Función para listar todos los registros con sus códigos QR
def listar_registros():
    cursor.execute("SELECT historia_id, estado, fecha_hora, qr_file FROM historias_clinicas")
    return cursor.fetchall()


# Función para mostrar los registros en la interfaz gráfica
def mostrar_registros():
    registros = listar_registros()

    for widget in frame.winfo_children():
        widget.destroy()

    for idx, registro in enumerate(registros):
        historia_id, estado, fecha_hora, qr_file = registro

        # Etiqueta para mostrar los datos del registro
        etiqueta = tk.Label(frame, text=f"ID: {historia_id}, Estado: {estado}, Fecha y Hora: {fecha_hora}")
        etiqueta.grid(row=idx, column=0, padx=10, pady=10, sticky="w")

        # Cargar y mostrar el código QR
        img = Image.open(qr_file)
        img = img.resize((100, 100))  # Redimensionar la imagen a 100x100 píxeles
        img = ImageTk.PhotoImage(img)

        etiqueta_img = tk.Label(frame, image=img)
        etiqueta_img.image = img  # Necesario para evitar que la imagen sea recogida por el recolector de basura
        etiqueta_img.grid(row=idx, column=1, padx=10, pady=10)


# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Listado de Historias Clínicas y Códigos QR")
ventana.geometry("600x400")

# Crear un marco para contener los registros
frame = ttk.Frame(ventana)
frame.pack(fill="both", expand=True, padx=10, pady=10)

# Botón para actualizar la lista de registros
boton_actualizar = ttk.Button(ventana, text="Actualizar Registros", command=mostrar_registros)
boton_actualizar.pack(pady=10)

# Inicializar mostrando los registros
mostrar_registros()

# Ejecutar la ventana principal
ventana.mainloop()

# Cerrar la conexión
conn.close()
