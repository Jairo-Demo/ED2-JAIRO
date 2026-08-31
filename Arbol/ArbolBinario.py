# ArbolBinario.py

from Nodo import Nodo

class ArbolBinario:
    def __init__(self):
        self.__raiz = None
        self.__cantidad = 0

    def get_raiz(self):
        return self.__raiz

    def get_cantidad(self):
        return self.__cantidad

    def esta_vacio(self) -> bool:
        return self.__raiz is None

    def __len__(self) -> int:
        return self.__cantidad

    def insertar(self, dato) -> None:
        self.__raiz = self.__insertar_rec(self.__raiz, dato)

    def __insertar_rec(self, nodo, dato):
        if nodo is None:
            self.__cantidad += 1
            return Nodo(dato)

        if dato < nodo.get_dato():
            nodo.set_izquierdo(self.__insertar_rec(nodo.get_izquierdo(), dato))
        elif dato > nodo.get_dato():
            nodo.set_derecho(self.__insertar_rec(nodo.get_derecho(), dato))

        return nodo

    def imprimir(self) -> None:
        self.__imprimir_rec(self.__raiz, 0)

    def __imprimir_rec(self, nodo, nivel) -> None:
        if nodo:
            self.__imprimir_rec(nodo.get_derecho(), nivel + 1)
            print("    " * nivel + f"[{nodo.get_dato()}]")
            self.__imprimir_rec(nodo.get_izquierdo(), nivel + 1)