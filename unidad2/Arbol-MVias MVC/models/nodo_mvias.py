"""Nodo de un árbol M-Vías."""


class NodoMVias:
    """Guarda hasta (orden - 1) claves ordenadas y hasta 'orden' hijos.

    El hijo en la posición i tiene claves menores que claves[i];
    el último hijo tiene claves mayores que la última clave.
    """

    def __init__(self, orden):
        self._orden = orden
        self._claves = []
        self._hijos = []

    # --- Getters y setters ---

    def get_orden(self):
        return self._orden

    def set_orden(self, orden):
        self._orden = orden

    def get_claves(self):
        return self._claves

    def set_claves(self, claves):
        self._claves = claves

    def get_hijos(self):
        return self._hijos

    def set_hijos(self, hijos):
        self._hijos = hijos

    # --- Consultas ---

    def es_hoja(self):
        """True si el nodo no tiene ningún hijo real."""
        return all(hijo is None for hijo in self._hijos)

    def esta_lleno(self):
        """True si ya tiene el máximo de claves (orden - 1)."""
        return len(self._claves) >= self._orden - 1

    def __repr__(self):
        return f"NodoMVias(claves={self._claves})"
