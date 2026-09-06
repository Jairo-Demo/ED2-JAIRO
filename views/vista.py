import tkinter as tk


class VistaConversor:
    """Vista: ventana 'Conversor de Expresiones' con 2 botones."""

    def __init__(self, master):
        self.master = master
        master.title("Conversor de Expresiones")

        tk.Label(
            master, text="Expresion infija:", font=("Arial", 10, "bold")
        ).pack(pady=(15, 5))

        self.entrada_expresion = tk.Entry(master, width=40)
        self.entrada_expresion.pack()

    

        frame_botones = tk.Frame(master)
        frame_botones.pack(pady=15)

        self.boton_prefija = tk.Button(frame_botones, text="Prefija")
        self.boton_prefija.pack(side="left", padx=10)

        self.boton_postfija = tk.Button(frame_botones, text="Postfija")
        self.boton_postfija.pack(side="left", padx=10)

        tk.Label(
            master, text="Resultado:", font=("Arial", 10, "bold")
        ).pack(pady=(10, 5))

        self.entrada_resultado = tk.Entry(master, width=40)
        self.entrada_resultado.pack(pady=(0, 15))

    def obtener_expresion(self) -> str:
        """Retorna el texto escrito en el campo de expresión infija."""
        return self.entrada_expresion.get()

    def mostrar_resultado(self, texto: str) -> None:
        """Muestra un texto en el campo de resultado."""
        self.entrada_resultado.delete(0, tk.END)
        self.entrada_resultado.insert(0, texto)
