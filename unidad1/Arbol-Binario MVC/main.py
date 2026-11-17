"""Abre el conversor de expresiones de escritorio (Tkinter).

Ejecutar desde esta carpeta:  python main.py
"""

import tkinter as tk

from controllers.controlador import ControladorConversor
from views.vista import VistaConversor


def main():
    ventana = tk.Tk()
    vista = VistaConversor(ventana)
    ControladorConversor(vista)
    ventana.mainloop()


if __name__ == "__main__":
    main()
