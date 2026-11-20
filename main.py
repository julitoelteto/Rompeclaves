import itertools
import tkinter as tk
from tkinter import messagebox

# 1. Ventana principal de 800x600
ventana = tk.Tk()
ventana.title("Rompe Claves Digital")
ventana.geometry("800x600")
ventana.configure(bg="#1e293b")
ventana.resizable(False, False)

# 2. Cuadrado centrado en el medio
cuadro_central = tk.Frame(
    ventana,
    bg="#0f172a",
    bd=2,
    relief="groove",
    width=460,
    height=380,
)
cuadro_central.place(relx=0.5, rely=0.5, anchor="center")
cuadro_central.pack_propagate(False)

# Texto dentro del cuadrado
lbl_titulo = tk.Label(
    cuadro_central,
    text="Inserte Contraseña digital\nde 8 dígitos (números del 0 al 7):",
    font=("Arial", 13, "bold"),
    bg="#0f172a",
    fg="white",
)
lbl_titulo.pack(pady=(20, 10))


# --- FUNCIÓN DE VALIDACIÓN EN TIEMPO REAL ---
# Impide escribir más de 8 caracteres y solo deja pasar números del 0 al 7
def limitar_entrada(texto_nuevo):
    if len(texto_nuevo) > 8:
        return False
    return all(c in "01234567" for c in texto_nuevo)


validacion = ventana.register(limitar_entrada)

# Caja para escribir la contraseña (bloqueada a máximo 8 dígitos del 0 al 7)
entrada_clave = tk.Entry(
    cuadro_central,
    font=("Courier", 16, "bold"),
    width=14,
    justify="center",
    bg="white",
    fg="black",
    validate="key",
    validatecommand=(validacion, "%P"),
)
entrada_clave.pack(pady=5)
entrada_clave.focus_set()

# Pantalla donde se imprime uno por uno (N1 | clave | V o F)
pantalla_proceso = tk.Text(
    cuadro_central,
    width=42,
    height=10,
    font=("Courier", 11),
    bg="#020617",
    fg="#22c55e",
)
pantalla_proceso.pack(pady=15)


# 3. Función que rompe la contraseña usando itertools
def romper_clave():
    clave_temporal = entrada_clave.get().strip()

    # Validar que no falten dígitos (por si escribió menos de 8)
    if len(clave_temporal) < 8:
        messagebox.showerror(
            "Faltan dígitos",
            "Debe completar los 8 dígitos antes de iniciar.",
        )
        return

    btn_romper.config(state="disabled")
    entrada_clave.config(state="disabled")  # Bloquea la caja mientras busca
    pantalla_proceso.delete("1.0", tk.END)

    # Crear archivo clave.txt
    archivo = open("clave.txt", "w", encoding="utf-8")

    # Formato tabla con palote (|)
    encabezado = f"{'N°':<10} | {'Clave':<10} | {'Detalle':<7}\n"
    separador = "-" * 34 + "\n"

    pantalla_proceso.insert(tk.END, encabezado + separador)
    archivo.write(encabezado + separador)

    # Generar combinaciones del 0 al 7 de 8 dígitos
    combinaciones = itertools.product("01234567", repeat=8)

    def evaluar_uno_por_uno(intento):
        try:
            clave_actual = "".join(next(combinaciones))
        except StopIteration:
            archivo.close()
            btn_romper.config(state="normal")
            entrada_clave.config(state="normal")
            return

        detalle = "V" if clave_actual == clave_temporal else "F"
        fila = f"N{intento:<9} | {clave_actual:<10} | {detalle:<7}\n"

        pantalla_proceso.insert(tk.END, fila)
        pantalla_proceso.see(tk.END)
        archivo.write(fila)

        if detalle == "V":
            mensaje = f"\nCLAVE HALLADA: {clave_actual}\nGuardada en clave.txt\n"
            pantalla_proceso.insert(tk.END, mensaje)
            pantalla_proceso.see(tk.END)
            archivo.write(mensaje)
            archivo.close()
            btn_romper.config(state="normal")
            entrada_clave.config(state="normal")
            messagebox.showinfo("Éxito", f"Clave encontrada: {clave_actual}")
        else:
            ventana.after(5, evaluar_uno_por_uno, intento + 1)

    evaluar_uno_por_uno(1)


# Botón abajo
btn_romper = tk.Button(
    cuadro_central,
    text="Romper clave digital",
    font=("Arial", 12, "bold"),
    bg="#2563eb",
    fg="white",
    command=romper_clave,
)
btn_romper.pack(pady=5)

ventana.mainloop()