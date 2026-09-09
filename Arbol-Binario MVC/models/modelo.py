# ================================================================
# models/modelo.py
# MODELO: Nodo y ArbolBinario con ELIMINACIÓN (sucesor inorden)
# ================================================================


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


class ArbolBinario:
    """Árbol Binario de Búsqueda + árbol de expresiones (infija)."""

    def __init__(self):
        self.__raiz = None
        self.__cantidad = 0

    # ------------------------------------------------------------------
    # Getters y Setters
    # ------------------------------------------------------------------

    def get_raiz(self):
        return self.__raiz

    def get_cantidad(self):
        return self.__cantidad

    def esta_vacio(self) -> bool:
        return self.__raiz is None

    def __len__(self) -> int:
        return self.__cantidad

    # ------------------------------------------------------------------
    # Insertar
    # ------------------------------------------------------------------

    def insertar(self, dato) -> None:
        self.__raiz = self.__insertar_rec(self.__raiz, dato)

    def __insertar_rec(self, nodo, dato):
        if nodo is None:
            self.__cantidad += 1
            return Nodo(dato)

        if dato < nodo.get_dato():
            nodo.set_izquierdo(
                self.__insertar_rec(nodo.get_izquierdo(), dato))
        elif dato > nodo.get_dato():
            nodo.set_derecho(
                self.__insertar_rec(nodo.get_derecho(), dato))

        return nodo

    # ------------------------------------------------------------------
    # EsHoja
    # ------------------------------------------------------------------

    def es_hoja(self, nodo: Nodo) -> bool:
        """Retorna True si el nodo dado es una hoja."""
        if nodo is None:
            return False
        return nodo.es_hoja()

    # ------------------------------------------------------------------
    # Busqueda
    # ------------------------------------------------------------------

    def buscar(self, dato) -> bool:
        """Busca un dato en el árbol. Complejidad: O(h)."""
        return self.__buscar_rec(self.__raiz, dato)

    def __buscar_rec(self, nodo: Nodo, dato) -> bool:
        """Auxiliar recursivo para buscar."""
        if nodo is None:
            return False
        if dato == nodo.get_dato():
            return True
        if dato < nodo.get_dato():
            return self.__buscar_rec(nodo.get_izquierdo(), dato)
        return self.__buscar_rec(nodo.get_derecho(), dato)

    # ------------------------------------------------------------------
    # Recorridos
    # ------------------------------------------------------------------

    def in_orden(self) -> list:
        """Recorrido in-orden: izq -> raíz -> der."""
        resultado = []
        self.__in_orden_rec(self.__raiz, resultado)
        return resultado

    def __in_orden_rec(self, nodo, resultado) -> None:
        if nodo:
            self.__in_orden_rec(nodo.get_izquierdo(), resultado)
            resultado.append(nodo.get_dato())
            self.__in_orden_rec(nodo.get_derecho(), resultado)

    def pre_orden(self) -> list:
        """Recorrido pre-orden: raíz -> izq -> der."""
        resultado = []
        self.__pre_orden_rec(self.__raiz, resultado)
        return resultado

    def __pre_orden_rec(self, nodo, resultado) -> None:
        if nodo:
            resultado.append(nodo.get_dato())
            self.__pre_orden_rec(nodo.get_izquierdo(), resultado)
            self.__pre_orden_rec(nodo.get_derecho(), resultado)

    def post_orden(self) -> list:
        """Recorrido post-orden: izq -> der -> raíz."""
        resultado = []
        self.__post_orden_rec(self.__raiz, resultado)
        return resultado

    def __post_orden_rec(self, nodo, resultado) -> None:
        if nodo:
            self.__post_orden_rec(nodo.get_izquierdo(), resultado)
            self.__post_orden_rec(nodo.get_derecho(), resultado)
            resultado.append(nodo.get_dato())

    # ================================================================
    # ELIMINACIÓN (NUEVO - con sucesor inorden)
    # ================================================================

    def eliminar(self, dato) -> bool:
        """
        Elimina un nodo con el dato dado usando el SUCESOR INORDEN.

        Casos:
            1. Nodo es hoja (sin hijos) → eliminación directa.
            2. Nodo tiene 1 hijo → el hijo ocupa su lugar.
            3. Nodo tiene 2 hijos → se reemplaza con el SUCESOR INORDEN
               (el nodo más pequeño del subárbol derecho).

        Args:
            dato: El dato a eliminar.

        Returns:
            bool: True si eliminó, False si el dato no existía.

        Complejidad: O(h) donde h = altura del árbol.
        """
        if not self.buscar(dato):
            return False

        self.__raiz = self.__eliminar_rec(self.__raiz, dato)
        self.__cantidad -= 1
        return True

    def __eliminar_rec(self, nodo: Nodo, dato) -> Nodo:
        """
        Auxiliar recursivo para eliminar.
        Usa el SUCESOR INORDEN para el caso de 2 hijos.
        """
        if nodo is None:
            return None

        # ---- 1. BUSCAR EL NODO A ELIMINAR ----
        if dato < nodo.get_dato():
            nodo.set_izquierdo(self.__eliminar_rec(nodo.get_izquierdo(), dato))
        elif dato > nodo.get_dato():
            nodo.set_derecho(self.__eliminar_rec(nodo.get_derecho(), dato))
        else:
            # ---- 2. NODO ENCONTRADO ----

            # CASO 1: Nodo HOJA (sin hijos)
            if nodo.get_izquierdo() is None and nodo.get_derecho() is None:
                return None

            # CASO 2a: Solo tiene hijo DERECHO
            if nodo.get_izquierdo() is None:
                return nodo.get_derecho()

            # CASO 2b: Solo tiene hijo IZQUIERDO
            if nodo.get_derecho() is None:
                return nodo.get_izquierdo()

            # CASO 3: Tiene DOS HIJOS → usar SUCESOR INORDEN
            # El sucesor inorden es el nodo más a la izquierda del subárbol derecho
            sucesor = self.__minimo_nodo(nodo.get_derecho())

            # Copiar el dato del sucesor al nodo actual
            nodo.set_dato(sucesor.get_dato())

            # Eliminar el sucesor del subárbol derecho
            nodo.set_derecho(self.__eliminar_rec(
                nodo.get_derecho(), sucesor.get_dato()))

        return nodo

    def __minimo_nodo(self, nodo: Nodo) -> Nodo:
        """
        Retorna el nodo con el valor MÍNIMO del subárbol.
        El mínimo siempre está en el nodo más a la izquierda.
        """
        actual = nodo
        while actual.get_izquierdo() is not None:
            actual = actual.get_izquierdo()
        return actual

    # ------------------------------------------------------------------
    # Mínimo y Máximo (para consultas)
    # ------------------------------------------------------------------

    def minimo(self):
        """Retorna el valor mínimo del árbol."""
        if self.esta_vacio():
            raise ValueError("El árbol está vacío")
        return self.__minimo_nodo(self.__raiz).get_dato()

    def maximo(self):
        """Retorna el valor máximo del árbol."""
        if self.esta_vacio():
            raise ValueError("El árbol está vacío")
        actual = self.__raiz
        while actual.get_derecho() is not None:
            actual = actual.get_derecho()
        return actual.get_dato()

    # ================================================================
    # EXPRESIONES (ya lo tenías)
    # ================================================================

    def construir_desde_infija(self, expresion):
        """Construye árbol desde expresión infija. Ej: a + b * c"""
        tokens = list(expresion.replace(" ", ""))
        postfija = self._infija_a_postfija(tokens)
        self.__raiz = self._arbol_desde_postfija(postfija)
        self.__cantidad = self._contar(self.__raiz)

    def _infija_a_postfija(self, tokens):
        """Convierte infija a postfija con PILA"""
        prec = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
        salida, pila = [], []

        for t in tokens:
            if t.isalnum():
                salida.append(t)
            elif t == '(':
                pila.append(t)
            elif t == ')':
                while pila and pila[-1] != '(':
                    salida.append(pila.pop())
                pila.pop()
            elif t in prec:
                while (pila and pila[-1] != '('
                       and prec.get(pila[-1], 0) >= prec[t]):
                    salida.append(pila.pop())
                pila.append(t)

        while pila:
            salida.append(pila.pop())
        return salida

    def _arbol_desde_postfija(self, postfija):
        """Construye árbol desde postfija con PILA"""
        pila = []
        for t in postfija:
            if t.isalnum():
                pila.append(Nodo(t))
            else:
                nodo = Nodo(t)
                nodo.set_derecho(pila.pop())
                nodo.set_izquierdo(pila.pop())
                pila.append(nodo)
        return pila[-1] if pila else None

    def _contar(self, nodo):
        if nodo is None:
            return 0
        return 1 + self._contar(nodo.get_izquierdo()) \
            + self._contar(nodo.get_derecho())

    def obtener_postfija(self):
        return " ".join(self.post_orden())

    def obtener_prefija(self):
        return " ".join(self.pre_orden())

    def obtener_infija(self):
        return self.__infija_rec(self.__raiz)

    def __infija_rec(self, nodo):
        if nodo is None:
            return ""
        if nodo.es_hoja():
            return str(nodo.get_dato())
        return (f"({self.__infija_rec(nodo.get_izquierdo())} "
                f"{nodo.get_dato()} "
                f"{self.__infija_rec(nodo.get_derecho())})")

    # ------------------------------------------------------------------
    # Imprimir
    # ------------------------------------------------------------------

    def imprimir(self) -> None:
        self.__imprimir_rec(self.__raiz, 0)

    def __imprimir_rec(self, nodo, nivel) -> None:
        if nodo:
            self.__imprimir_rec(nodo.get_derecho(), nivel + 1)
            print("    " * nivel + f"[{nodo.get_dato()}]")
            self.__imprimir_rec(nodo.get_izquierdo(), nivel + 1)