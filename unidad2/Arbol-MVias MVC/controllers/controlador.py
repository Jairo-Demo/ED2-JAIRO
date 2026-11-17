"""Controlador de la versión de consola del Árbol M-Vías."""

from models.arbol_mvias import ArbolMVias
from views.vista import VistaConsola


class Controlador:
    """Lee la opción del menú (Vista), usa el árbol (Modelo) y
    muestra el resultado (Vista)."""

    def __init__(self):
        self.vista = VistaConsola()
        self.arbol = None

    def iniciar(self):
        """Pide el orden del árbol y repite el menú hasta salir."""
        self.vista.mostrar_mensaje("Primero se crea el árbol.")
        orden = self.vista.pedir_orden()
        self.arbol = ArbolMVias(orden)
        self.vista.mostrar_mensaje(f"Árbol M-Vías de orden {orden} creado.")

        acciones = {
            "1": self._insertar,
            "2": self._insertar_varias,
            "3": self._buscar,
            "4": self._mostrar_en_orden,
            "5": self._mostrar_arbol,
        }
        while True:
            self.vista.mostrar_menu()
            opcion = self.vista.pedir_opcion()
            if opcion == "6":
                self.vista.mostrar_mensaje("Hasta luego.")
                break
            if opcion in acciones:
                acciones[opcion]()
            else:
                self.vista.mostrar_error("Opción inválida.")

    def _insertar(self):
        clave = self.vista.pedir_clave()
        self.arbol.insertar(clave)
        self.vista.mostrar_mensaje(f"Clave {clave} insertada.")

    def _insertar_varias(self):
        claves = self.vista.pedir_varias_claves()
        if not claves:
            self.vista.mostrar_error("No se ingresaron claves válidas.")
            return
        for clave in claves:
            self.arbol.insertar(clave)
        self.vista.mostrar_mensaje(f"Se insertaron {len(claves)} claves.")

    def _buscar(self):
        if self.arbol.esta_vacio():
            self.vista.mostrar_error("El árbol está vacío.")
            return
        clave = self.vista.pedir_clave()
        if self.arbol.buscar(clave):
            self.vista.mostrar_mensaje(f"La clave {clave} SÍ existe.")
        else:
            self.vista.mostrar_mensaje(f"La clave {clave} NO existe.")

    def _mostrar_en_orden(self):
        if self.arbol.esta_vacio():
            self.vista.mostrar_error("El árbol está vacío.")
        else:
            self.vista.mostrar_mensaje(
                f"Recorrido en orden: {self.arbol.en_orden()}")

    def _mostrar_arbol(self):
        self.vista.mostrar_arbol(self.arbol.obtener_niveles_texto())
