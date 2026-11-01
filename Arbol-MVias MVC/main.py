import sys
import os

# Asegurar que la carpeta actual esté en sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from controllers.controlador import Controlador
except (ImportError, ValueError):
    from controlador import Controlador

def main():
    """
    Punto de entrada de la aplicación.
    Solo se encarga de instanciar el controlador y arrancar el ciclo de vida.
    """
    app = Controlador()
    app.iniciar()

if __name__ == "__main__":
    main()
