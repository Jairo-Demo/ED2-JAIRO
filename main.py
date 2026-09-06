
import tkinter as tk

from views.vista import VistaConversor
from controllers.controlador import ControladorConversor


def main() -> None:
    root = tk.Tk()

    vista = VistaConversor(root)
    ControladorConversor(vista)

    root.mainloop()


if __name__ == "__main__":
    main()
