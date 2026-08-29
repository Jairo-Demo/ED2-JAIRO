# nodo_arbol.py
# Unidad I: Árbol Binario de Búsqueda (ABB) - Versión básica
# =====================================================================
 
class Nodo:
    """Nodo de un árbol binario."""
 
    def __init__(self, dato):
        self.dato = dato
        self.izquierdo = None
        self.derecho = None
 
    def __repr__(self):
        return f"Nodo({self.dato})"
 
 
class ArbolBinarioBusqueda:
    """
    Árbol Binario de Búsqueda (ABB) - operaciones básicas.
 
    Propiedad ABB: para cada nodo N,
        - subárbol izquierdo < N.dato
        - subárbol derecho  > N.dato
    """
 
    def __init__(self):
        """Inicializa el árbol vacío."""
        self._raiz = None
        self._tamanio = 0
 
    def esta_vacio(self) -> bool:
        """Retorna True si el árbol no tiene nodos."""
        return self._raiz is None
 
    def __len__(self) -> int:
        return self._tamanio
 
    # ------------------------------------------------------------------
    # Inserción
    # ------------------------------------------------------------------
 
    def insertar(self, dato) -> None:
        """
        Inserta un nuevo dato manteniendo la propiedad ABB.
        Los valores duplicados son ignorados.
 
        Complejidad: O(h) donde h = altura del árbol.
        """
        self._raiz = self._insertar_rec(self._raiz, dato)
 
    def _insertar_rec(self, nodo: Nodo, dato) -> Nodo:
        """Auxiliar recursivo para insertar."""
        if nodo is None:
            self._tamanio += 1
            return Nodo(dato)
 
        if dato < nodo.dato:
            nodo.izquierdo = self._insertar_rec(nodo.izquierdo, dato)
        elif dato > nodo.dato:
            nodo.derecho = self._insertar_rec(nodo.derecho, dato)
        # dato == nodo.dato -> duplicado, se ignora
 
        return nodo
 
    # ------------------------------------------------------------------
    # Búsqueda
    # ------------------------------------------------------------------
 
    def buscar(self, dato) -> bool:
        """
        Busca un dato en el árbol.
 
        Retorna:
            True si el dato existe, False en caso contrario.
 
        Complejidad: O(h)
        """
        return self._buscar_rec(self._raiz, dato)
 
    def _buscar_rec(self, nodo: Nodo, dato) -> bool:
        """Auxiliar recursivo para buscar."""
        if nodo is None:
            return False
        if dato == nodo.dato:
            return True
        if dato < nodo.dato:
            return self._buscar_rec(nodo.izquierdo, dato)
        return self._buscar_rec(nodo.derecho, dato)
 
    # ------------------------------------------------------------------
    # Altura
    # ------------------------------------------------------------------
 
    def altura(self) -> int:
        """
        Calcula la altura del árbol.
        La altura de un árbol vacío es -1, la de un árbol con solo raíz es 0.
        """
        return self._altura_rec(self._raiz)
 
    def _altura_rec(self, nodo: Nodo) -> int:
        if nodo is None:
            return -1
        return 1 + max(self._altura_rec(nodo.izquierdo),
                       self._altura_rec(nodo.derecho))
 
    # ------------------------------------------------------------------
    # Recorrido en-orden
    # ------------------------------------------------------------------
 
    def en_orden(self) -> list:
        """Recorrido en-orden: izq -> raíz -> der. Produce lista ordenada."""
        resultado = []
        self._en_orden_rec(self._raiz, resultado)
        return resultado
 
    def _en_orden_rec(self, nodo: Nodo, resultado: list) -> None:
        if nodo:
            self._en_orden_rec(nodo.izquierdo, resultado)
            resultado.append(nodo.dato)
            self._en_orden_rec(nodo.derecho, resultado)
 
    # ------------------------------------------------------------------
    # Visualización
    # ------------------------------------------------------------------
 
    def imprimir(self) -> None:
        """Imprime el árbol en formato visual (rotado 90°)."""
        self._imprimir_rec(self._raiz, 0)
 
    def _imprimir_rec(self, nodo: Nodo, nivel: int) -> None:
        if nodo:
            self._imprimir_rec(nodo.derecho, nivel + 1)
            print("    " * nivel + f"[{nodo.dato}]")
            self._imprimir_rec(nodo.izquierdo, nivel + 1)
 
 
# ------------------------------------------------------------------
# Demo
# ------------------------------------------------------------------
 
if __name__ == "__main__":
    abb = ArbolBinarioBusqueda()
 
    valores = [50, 30, 70, 20, 40, 60, 80]
    print("=== Árbol Binario de Búsqueda (básico) ===")
    print(f"Insertando: {valores}")
    for v in valores:
        abb.insertar(v)
 
    print("\nÁrbol (leer de abajo hacia arriba = de izq a der):")
    abb.imprimir()
 
    print(f"\nAltura: {abb.altura()}")
    print(f"Tamaño: {len(abb)}")
    print(f"En-orden: {abb.en_orden()}")
 
    print(f"\n¿Existe 40? {abb.buscar(40)}")
    print(f"¿Existe 99? {abb.buscar(99)}")