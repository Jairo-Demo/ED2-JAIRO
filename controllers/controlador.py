
from models.modelo import ArbolBinario
from views.vista import VistaConversor


class ControladorConversor:
    """Controlador: escucha ambos botones y actualiza la Vista."""

    def __init__(self, vista: VistaConversor):
        self.vista = vista
        self.vista.boton_prefija.config(command=self.al_click_prefija)
        self.vista.boton_postfija.config(command=self.al_click_postfija)

    def al_click_prefija(self) -> None:
        """Se ejecuta al presionar el botón 'Prefija'."""
        arbol = self.__construir_arbol()
        if arbol is not None:
            self.vista.mostrar_resultado(arbol.obtener_prefija())

    def al_click_postfija(self) -> None:
        """Se ejecuta al presionar el botón 'Postfija'."""
        arbol = self.__construir_arbol()
        if arbol is not None:
            self.vista.mostrar_resultado(arbol.obtener_postfija())

    def __construir_arbol(self):
        """Lee la expresión de la Vista y construye el árbol.

        Retorna None (y avisa en el campo de resultado) si el campo
        de expresión está vacío.
        """
        expresion = self.vista.obtener_expresion()

        if not expresion.strip():
            self.vista.mostrar_resultado("Escribe una expresion")
            return None

        arbol = ArbolBinario()
        arbol.construir_desde_infija(expresion)
        return arbol
