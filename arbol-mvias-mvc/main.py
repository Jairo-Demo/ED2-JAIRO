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
