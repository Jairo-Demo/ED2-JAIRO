"""Controlador del conversor de expresiones (versión de escritorio)."""

from models.modelo import ArbolBinario
from views.vista import VistaConversor


class ControladorConversor:
    """Conecta los botones de la Vista con el árbol de expresiones."""

    def __init__(self, vista: VistaConversor):
        self.vista = vista
        self.vista.boton_prefija.config(command=self.mostrar_prefija)
        self.vista.boton_postfija.config(command=self.mostrar_postfija)

    def mostrar_prefija(self):
        """Botón 'Prefija': muestra la expresión en notación prefija."""
        arbol = self.__construir_arbol()
        if arbol is not None:
            self.vista.mostrar_resultado(arbol.obtener_prefija())

    def mostrar_postfija(self):
        """Botón 'Postfija': muestra la expresión en notación postfija."""
        arbol = self.__construir_arbol()
        if arbol is not None:
            self.vista.mostrar_resultado(arbol.obtener_postfija())

    def __construir_arbol(self):
        """Arma el árbol con la expresión escrita, o None si está vacía."""
        expresion = self.vista.obtener_expresion()
        if not expresion.strip():
            self.vista.mostrar_resultado("Escribe una expresión")
            return None
        arbol = ArbolBinario()
        arbol.construir_desde_infija(expresion)
        return arbol
