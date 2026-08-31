# ArbolBinario.py

from Nodo import Nodo

class ArbolBinario:
    def __init__(self):
        self.__raiz = None
        self.__cantidad = 0

    # ------------------------------------------------------------------
    #Getters y Setters
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
            nodo.set_izquierdo(self.__insertar_rec(nodo.get_izquierdo(), dato))
        elif dato > nodo.get_dato():
            nodo.set_derecho(self.__insertar_rec(nodo.get_derecho(), dato))

        return nodo

    # ------------------------------------------------------------------
    # EsHoja
    # ------------------------------------------------------------------
 
    def es_hoja(self, nodo: Nodo) -> bool:
        """
        Retorna True si el nodo dado es una hoja
        (no tiene hijo izquierdo ni derecho).
        """
        if nodo is None:
            return False
        return nodo.es_hoja()

    # ------------------------------------------------------------------
    # Busqueda
    # ------------------------------------------------------------------
     
    def buscar(self, dato) -> bool:
        """
        Busca un dato en el árbol.
 
        Retorna:
            True si el dato existe, False en caso contrario.
 
        Complejidad: O(h)
        """
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
    # InOrden - Izquierdo → Raíz → Derecho
    # ------------------------------------------------------------------

    def in_orden(self) -> list:
        """Recorrido in-orden: izq → raíz → der."""
        resultado = []
        self.__in_orden_rec(self.__raiz, resultado)
        return resultado

    def __in_orden_rec(self, nodo, resultado) -> None:
        if nodo:
            self.__in_orden_rec(nodo.get_izquierdo(), resultado)
            resultado.append(nodo.get_dato())
            self.__in_orden_rec(nodo.get_derecho(), resultado)

    # ------------------------------------------------------------------
    # PreOrden - Raíz → Izquierdo → Derecho
    # ------------------------------------------------------------------

    def pre_orden(self) -> list:
        """Recorrido pre-orden: raíz → izq → der."""
        resultado = []
        self.__pre_orden_rec(self.__raiz, resultado)
        return resultado

    def __pre_orden_rec(self, nodo, resultado) -> None:
        if nodo:
            resultado.append(nodo.get_dato())
            self.__pre_orden_rec(nodo.get_izquierdo(), resultado)
            self.__pre_orden_rec(nodo.get_derecho(), resultado)

    # ------------------------------------------------------------------
    # PostOrden - Izquierdo → Derecho → Raíz
    # ------------------------------------------------------------------

    def post_orden(self) -> list:
        """Recorrido post-orden: izq → der → raíz."""
        resultado = []
        self.__post_orden_rec(self.__raiz, resultado)
        return resultado

    def __post_orden_rec(self, nodo, resultado) -> None:
        if nodo:
            self.__post_orden_rec(nodo.get_izquierdo(), resultado)
            self.__post_orden_rec(nodo.get_derecho(), resultado)
            resultado.append(nodo.get_dato())

    # ==========================================
    # CONSTRUIR DESDE EXPRESIÓN INFIJA (POSFIJA)
    # ==========================================
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
            if t.isalnum():  # Operando (letra o número)
                salida.append(t)
            elif t == '(':
                pila.append(t)
            elif t == ')':
                while pila and pila[-1] != '(':
                    salida.append(pila.pop())
                pila.pop()
            elif t in prec:  # Operador
                while pila and pila[-1] != '(' and prec.get(pila[-1], 0) >= prec[t]:
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
        return 0 if nodo is None else 1 + self._contar(nodo.get_izquierdo()) + self._contar(nodo.get_derecho())

    # ==========================================
    # EXPRESIONES (USAMOS LOS DE ORDEN)
    # ==========================================
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
        return f"({self.__infija_rec(nodo.get_izquierdo())} {nodo.get_dato()} {self.__infija_rec(nodo.get_derecho())})"


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