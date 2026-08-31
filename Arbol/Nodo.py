
class Nodo:
    """
    Representa un nodo de un árbol binario.
 
    Encapsula el dato y las referencias a sus hijos (izquierdo y derecho)
    como atributos privados, expuestos únicamente mediante getters/setters.
    """
 
    def __init__(self, dato):
        self.__dato = dato
        self.__izquierdo = None
        self.__derecho = None
 
    # ------------------------------------------------------------------
    # Getters y Setters
    # ------------------------------------------------------------------
 
    def get_dato(self):
        """Retorna el dato almacenado en el nodo."""
        return self.__dato
 
    def set_dato(self, dato) -> None:
        """Asigna un nuevo valor al dato del nodo."""
        self.__dato = dato
 
    def get_izquierdo(self) -> "Nodo":
        """Retorna la referencia al hijo izquierdo (o None)."""
        return self.__izquierdo
 
    def set_izquierdo(self, nodo: "Nodo") -> None:
        """Asigna el hijo izquierdo del nodo."""
        self.__izquierdo = nodo
 
    def get_derecho(self) -> "Nodo":
        """Retorna la referencia al hijo derecho (o None)."""
        return self.__derecho
 
    def set_derecho(self, nodo: "Nodo") -> None:
        """Asigna el hijo derecho del nodo."""
        self.__derecho = nodo
 
    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------
 
    def es_hoja(self) -> bool:
        """Retorna True si el nodo no tiene hijos (izq. y der. None)."""
        return self.__izquierdo is None and self.__derecho is None
 
    def __repr__(self) -> str:
        return f"Nodo({self.__dato})"
 