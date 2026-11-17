"""Vista del conversor de expresiones (ventana Tkinter)."""

import tkinter as tk


class VistaConversor:
    """Ventana con la expresión, dos botones y el resultado."""

    def __init__(self, ventana):
        self.ventana = ventana
        ventana.title("Conversor de Expresiones")

        tk.Label(ventana, text="Expresión infija:").pack(pady=(15, 5))
        self.entrada_expresion = tk.Entry(ventana, width=40)
        self.entrada_expresion.pack()

        marco_botones = tk.Frame(ventana)
        marco_botones.pack(pady=15)
        # El controlador asigna qué hace cada botón.
        self.boton_prefija = tk.Button(marco_botones, text="Prefija")
        self.boton_prefija.pack(side="left", padx=10)
        self.boton_postfija = tk.Button(marco_botones, text="Postfija")
        self.boton_postfija.pack(side="left", padx=10)

        tk.Label(ventana, text="Resultado:").pack(pady=(10, 5))
        self.entrada_resultado = tk.Entry(ventana, width=40)
        self.entrada_resultado.pack(pady=(0, 15))

    def obtener_expresion(self):
        """Texto escrito en el campo de la expresión."""
        return self.entrada_expresion.get()

    def mostrar_resultado(self, texto):
        """Reemplaza el contenido del campo de resultado."""
        self.entrada_resultado.delete(0, tk.END)
        self.entrada_resultado.insert(0, texto)
