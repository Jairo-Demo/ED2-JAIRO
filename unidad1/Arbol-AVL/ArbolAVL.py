"""Árbol AVL: árbol binario de búsqueda que se balancea solo.

Después de cada inserción o eliminación revisa el factor de equilibrio
de los nodos del camino y aplica rotaciones si hace falta.

Ejecutar desde esta carpeta:  python ArbolAVL.py
"""


class NodoAVL:
    """Nodo del AVL: valor, hijos y altura del subárbol."""

    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None
        self.altura = 1  # una hoja tiene altura 1

    def factor_equilibrio(self):
        """Altura del hijo izquierdo menos altura del hijo derecho."""
        altura_izquierda = self.izquierdo.altura if self.izquierdo else 0
        altura_derecha = self.derecho.altura if self.derecho else 0
        return altura_izquierda - altura_derecha

    def __repr__(self):
        return f"NodoAVL(valor={self.valor}, altura={self.altura})"


class ArbolAVL:
    """Árbol AVL con insertar, eliminar, buscar y recorridos."""

    def __init__(self):
        self.raiz = None

    # --- Utilidades ---

    def _altura(self, nodo):
        return nodo.altura if nodo else 0

    def _actualizar_altura(self, nodo):
        """Recalcula la altura del nodo a partir de sus hijos."""
        nodo.altura = 1 + max(self._altura(nodo.izquierdo),
                              self._altura(nodo.derecho))

    def _nodo_minimo(self, nodo):
        """Nodo con el menor valor del subárbol (el de más a la izquierda)."""
        nodo_actual = nodo
        while nodo_actual.izquierdo:
            nodo_actual = nodo_actual.izquierdo
        return nodo_actual

    # --- Rotaciones ---

    def _rotar_derecha(self, nodo):
        """Rotación simple a la derecha (caso izquierda-izquierda).

               nodo              hijo
               /                 /   \\
            hijo       ->       A    nodo
            /   \\                    /
           A   medio              medio
        """
        hijo = nodo.izquierdo
        medio = hijo.derecho

        hijo.derecho = nodo
        nodo.izquierdo = medio

        self._actualizar_altura(nodo)   # primero el que quedó abajo
        self._actualizar_altura(hijo)
        return hijo                     # nueva raíz del subárbol

    def _rotar_izquierda(self, nodo):
        """Rotación simple a la izquierda (caso derecha-derecha).

            nodo                   hijo
               \\                  /   \\
               hijo      ->     nodo    A
              /   \\               \\
           medio   A              medio
        """
        hijo = nodo.derecho
        medio = hijo.izquierdo

        hijo.izquierdo = nodo
        nodo.derecho = medio

        self._actualizar_altura(nodo)
        self._actualizar_altura(hijo)
        return hijo

    # --- Balancear ---

    def _balancear(self, nodo):
        """Aplica la rotación que corresponda según el factor de equilibrio.

        Izquierda-izquierda: rotar a la derecha.
        Izquierda-derecha:   rotar el hijo a la izquierda y luego derecha.
        Derecha-derecha:     rotar a la izquierda.
        Derecha-izquierda:   rotar el hijo a la derecha y luego izquierda.
        """
        factor = nodo.factor_equilibrio()

        if factor > 1:  # cargado a la izquierda
            if nodo.izquierdo.factor_equilibrio() < 0:
                nodo.izquierdo = self._rotar_izquierda(nodo.izquierdo)
            return self._rotar_derecha(nodo)

        if factor < -1:  # cargado a la derecha
            if nodo.derecho.factor_equilibrio() > 0:
                nodo.derecho = self._rotar_derecha(nodo.derecho)
            return self._rotar_izquierda(nodo)

        return nodo  # ya está balanceado

    # --- Insertar ---

    def insertar(self, valor):
        """Inserta el valor y rebalancea el camino hasta la raíz."""
        self.raiz = self._insertar(self.raiz, valor)

    def _insertar(self, nodo, valor):
        if nodo is None:
            return NodoAVL(valor)
        if valor < nodo.valor:
            nodo.izquierdo = self._insertar(nodo.izquierdo, valor)
        else:
            nodo.derecho = self._insertar(nodo.derecho, valor)
        # Al volver de la recursión: actualizar altura y balancear.
        self._actualizar_altura(nodo)
        return self._balancear(nodo)

    # --- Eliminar ---

    def eliminar(self, valor):
        """Elimina el valor (como en un ABB) y rebalancea el árbol."""
        self.raiz = self._eliminar(self.raiz, valor)

    def _eliminar(self, nodo, valor):
        if nodo is None:
            return None

        # 1. Buscar el nodo.
        if valor < nodo.valor:
            nodo.izquierdo = self._eliminar(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            nodo.derecho = self._eliminar(nodo.derecho, valor)
        else:
            # 2. Nodo encontrado.
            if nodo.izquierdo is None:
                return nodo.derecho     # hoja o solo hijo derecho
            if nodo.derecho is None:
                return nodo.izquierdo   # solo hijo izquierdo
            # Dos hijos: copiar el sucesor inorden y eliminarlo.
            sucesor = self._nodo_minimo(nodo.derecho)
            nodo.valor = sucesor.valor
            nodo.derecho = self._eliminar(nodo.derecho, sucesor.valor)

        # 3. Actualizar altura y balancear.
        self._actualizar_altura(nodo)
        return self._balancear(nodo)

    # --- Consultas ---

    def buscar(self, valor):
        """True si el valor está en el árbol."""
        nodo_actual = self.raiz
        while nodo_actual:
            if valor == nodo_actual.valor:
                return True
            if valor < nodo_actual.valor:
                nodo_actual = nodo_actual.izquierdo
            else:
                nodo_actual = nodo_actual.derecho
        return False

    def altura(self):
        return self.raiz.altura if self.raiz else 0

    # --- Recorridos ---

    def inorden(self):
        resultado = []
        self._inorden(self.raiz, resultado)
        return resultado

    def _inorden(self, nodo, resultado):
        if nodo:
            self._inorden(nodo.izquierdo, resultado)
            resultado.append(nodo.valor)
            self._inorden(nodo.derecho, resultado)

    def preorden(self):
        resultado = []
        self._preorden(self.raiz, resultado)
        return resultado

    def _preorden(self, nodo, resultado):
        if nodo:
            resultado.append(nodo.valor)
            self._preorden(nodo.izquierdo, resultado)
            self._preorden(nodo.derecho, resultado)

    def postorden(self):
        resultado = []
        self._postorden(self.raiz, resultado)
        return resultado

    def _postorden(self, nodo, resultado):
        if nodo:
            self._postorden(nodo.izquierdo, resultado)
            self._postorden(nodo.derecho, resultado)
            resultado.append(nodo.valor)

    # --- Mostrar en consola ---

    def imprimir(self):
        """Dibuja el árbol de lado con altura (h) y factor (FE)."""
        self._imprimir(self.raiz, 0)

    def _imprimir(self, nodo, nivel):
        if nodo:
            self._imprimir(nodo.derecho, nivel + 1)
            print("    " * nivel + f"[{nodo.valor} h={nodo.altura} "
                  f"FE={nodo.factor_equilibrio()}]")
            self._imprimir(nodo.izquierdo, nivel + 1)


if __name__ == "__main__":
    # Prueba 1: inserciones que obligan a rebalancear.
    arbol_insercion = ArbolAVL()
    valores = [30, 20, 40, 10, 25, 22]
    print(f"Insertando: {valores}")
    print("(La inserción de 22 causa un desbalance izquierda-derecha)")
    for valor in valores:
        print(f"\n--- Insertando {valor} ---")
        arbol_insercion.insertar(valor)
        arbol_insercion.imprimir()
        print(f"Altura del árbol: {arbol_insercion.altura()}")
        print(f"Inorden: {arbol_insercion.inorden()}")

    print("\n" + "=" * 60)
    print("El árbol se mantiene balanceado automáticamente.")
    print("La altura es O(log n) gracias a las rotaciones.")
    print("=" * 60)

    # Prueba 2: eliminaciones con rebalanceo.
    arbol_eliminacion = ArbolAVL()
    for valor in [50, 30, 70, 20, 40, 60, 80]:
        arbol_eliminacion.insertar(valor)

    print("Árbol inicial:")
    arbol_eliminacion.imprimir()
    print(f"Inorden: {arbol_eliminacion.inorden()}\n")

    arbol_eliminacion.eliminar(30)
    print("Después de eliminar 30:")
    arbol_eliminacion.imprimir()
    print(f"Inorden: {arbol_eliminacion.inorden()}\n")

    arbol_eliminacion.eliminar(50)
    print("Después de eliminar 50:")
    arbol_eliminacion.imprimir()
    print(f"Inorden: {arbol_eliminacion.inorden()}")
