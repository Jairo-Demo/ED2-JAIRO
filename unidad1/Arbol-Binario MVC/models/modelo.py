"""Modelo del Árbol Binario de Búsqueda (ABB).

Contiene la clase Nodo y la clase ArbolBinario con:
insertar, buscar, eliminar (con sucesor inorden), recorridos,
altura, hojas, balanceo, validación de ABB, sucesor inorden
y construcción de un árbol de expresiones desde notación infija.
"""

from collections import deque


class Nodo:
    """Nodo de un árbol binario: un dato y sus dos hijos."""

    def __init__(self, dato):
        self.__dato = dato
        self.__izquierdo = None
        self.__derecho = None

    # --- Getters y setters ---

    def get_dato(self):
        return self.__dato

    def set_dato(self, dato):
        self.__dato = dato

    def get_izquierdo(self):
        return self.__izquierdo

    def set_izquierdo(self, nodo):
        self.__izquierdo = nodo

    def get_derecho(self):
        return self.__derecho

    def set_derecho(self, nodo):
        self.__derecho = nodo

    def es_hoja(self):
        """True si el nodo no tiene hijos."""
        return self.__izquierdo is None and self.__derecho is None

    def __repr__(self):
        return f"Nodo({self.__dato})"


class ArbolBinario:
    """Árbol Binario de Búsqueda (también sirve para expresiones)."""

    def __init__(self):
        self.__raiz = None
        self.__cantidad = 0

    # --- Consultas básicas ---

    def get_raiz(self):
        return self.__raiz

    def get_cantidad(self):
        return self.__cantidad

    def esta_vacio(self):
        return self.__raiz is None

    def __len__(self):
        return self.__cantidad

    # --- Insertar ---

    def insertar(self, dato):
        """Inserta el dato respetando la regla del ABB (sin repetidos)."""
        self.__raiz = self.__insertar_recursivo(self.__raiz, dato)

    def __insertar_recursivo(self, nodo, dato):
        if nodo is None:
            # Lugar vacío encontrado: aquí va el nuevo nodo.
            self.__cantidad += 1
            return Nodo(dato)
        if dato < nodo.get_dato():
            nodo.set_izquierdo(
                self.__insertar_recursivo(nodo.get_izquierdo(), dato))
        elif dato > nodo.get_dato():
            nodo.set_derecho(
                self.__insertar_recursivo(nodo.get_derecho(), dato))
        # Si el dato ya existe, no se inserta de nuevo.
        return nodo

    def es_hoja(self, nodo):
        """True si el nodo existe y no tiene hijos."""
        if nodo is None:
            return False
        return nodo.es_hoja()

    # --- Buscar ---

    def buscar(self, dato):
        """True si el dato está en el árbol. Complejidad O(altura)."""
        return self.__buscar_recursivo(self.__raiz, dato)

    def __buscar_recursivo(self, nodo, dato):
        if nodo is None:
            return False
        if dato == nodo.get_dato():
            return True
        if dato < nodo.get_dato():
            return self.__buscar_recursivo(nodo.get_izquierdo(), dato)
        return self.__buscar_recursivo(nodo.get_derecho(), dato)

    # --- Recorridos ---

    def in_orden(self):
        """Izquierdo -> raíz -> derecho (da los datos ordenados)."""
        resultado = []
        self.__in_orden_recursivo(self.__raiz, resultado)
        return resultado

    def __in_orden_recursivo(self, nodo, resultado):
        if nodo:
            self.__in_orden_recursivo(nodo.get_izquierdo(), resultado)
            resultado.append(nodo.get_dato())
            self.__in_orden_recursivo(nodo.get_derecho(), resultado)

    def pre_orden(self):
        """Raíz -> izquierdo -> derecho."""
        resultado = []
        self.__pre_orden_recursivo(self.__raiz, resultado)
        return resultado

    def __pre_orden_recursivo(self, nodo, resultado):
        if nodo:
            resultado.append(nodo.get_dato())
            self.__pre_orden_recursivo(nodo.get_izquierdo(), resultado)
            self.__pre_orden_recursivo(nodo.get_derecho(), resultado)

    def post_orden(self):
        """Izquierdo -> derecho -> raíz."""
        resultado = []
        self.__post_orden_recursivo(self.__raiz, resultado)
        return resultado

    def __post_orden_recursivo(self, nodo, resultado):
        if nodo:
            self.__post_orden_recursivo(nodo.get_izquierdo(), resultado)
            self.__post_orden_recursivo(nodo.get_derecho(), resultado)
            resultado.append(nodo.get_dato())

    def por_niveles(self):
        """Recorrido por niveles (de arriba hacia abajo) con una cola."""
        if self.esta_vacio():
            return []
        cola = deque([self.__raiz])
        resultado = []
        while cola:
            nodo_actual = cola.popleft()
            resultado.append(nodo_actual.get_dato())
            if nodo_actual.get_izquierdo() is not None:
                cola.append(nodo_actual.get_izquierdo())
            if nodo_actual.get_derecho() is not None:
                cola.append(nodo_actual.get_derecho())
        return resultado

    # --- Eliminar ---

    def eliminar(self, dato):
        """Elimina el dato. Devuelve False si no existía.

        Casos: hoja (se quita), un hijo (el hijo ocupa su lugar) y
        dos hijos (se reemplaza por su sucesor inorden).
        """
        if not self.buscar(dato):
            return False
        self.__raiz = self.__eliminar_recursivo(self.__raiz, dato)
        self.__cantidad -= 1
        return True

    def __eliminar_recursivo(self, nodo, dato):
        if nodo is None:
            return None

        # 1. Buscar el nodo a eliminar.
        if dato < nodo.get_dato():
            nodo.set_izquierdo(
                self.__eliminar_recursivo(nodo.get_izquierdo(), dato))
        elif dato > nodo.get_dato():
            nodo.set_derecho(
                self.__eliminar_recursivo(nodo.get_derecho(), dato))
        else:
            # 2. Nodo encontrado.
            if nodo.es_hoja():
                return None                       # caso hoja
            if nodo.get_izquierdo() is None:
                return nodo.get_derecho()         # solo hijo derecho
            if nodo.get_derecho() is None:
                return nodo.get_izquierdo()       # solo hijo izquierdo

            # Dos hijos: copiar el sucesor inorden (el menor del
            # subárbol derecho) y luego eliminar ese sucesor.
            sucesor = self.__nodo_minimo(nodo.get_derecho())
            nodo.set_dato(sucesor.get_dato())
            nodo.set_derecho(self.__eliminar_recursivo(
                nodo.get_derecho(), sucesor.get_dato()))
        return nodo

    def __nodo_minimo(self, nodo):
        """Nodo con el menor dato del subárbol: el de más a la izquierda."""
        nodo_actual = nodo
        while nodo_actual.get_izquierdo() is not None:
            nodo_actual = nodo_actual.get_izquierdo()
        return nodo_actual

    # --- Mínimo y máximo ---

    def minimo(self):
        if self.esta_vacio():
            raise ValueError("El árbol está vacío")
        return self.__nodo_minimo(self.__raiz).get_dato()

    def maximo(self):
        """El máximo es el nodo de más a la derecha."""
        if self.esta_vacio():
            raise ValueError("El árbol está vacío")
        nodo_actual = self.__raiz
        while nodo_actual.get_derecho() is not None:
            nodo_actual = nodo_actual.get_derecho()
        return nodo_actual.get_dato()

    # --- Altura, hojas y balanceo ---

    def altura(self):
        """Altura del árbol: 0 si está vacío, 1 si solo hay raíz."""
        return self.__altura_recursiva(self.__raiz)

    def __altura_recursiva(self, nodo):
        if nodo is None:
            return 0
        return 1 + max(self.__altura_recursiva(nodo.get_izquierdo()),
                       self.__altura_recursiva(nodo.get_derecho()))

    def contar_hojas(self):
        """Cantidad de nodos sin hijos (Tarea 4)."""
        return self.__contar_hojas_recursivo(self.__raiz)

    def __contar_hojas_recursivo(self, nodo):
        if nodo is None:
            return 0
        if nodo.es_hoja():
            return 1
        return (self.__contar_hojas_recursivo(nodo.get_izquierdo())
                + self.__contar_hojas_recursivo(nodo.get_derecho()))

    def es_balanceado(self):
        """True si en cada nodo las alturas de sus hijos difieren en <= 1."""
        return self.__altura_si_balanceado(self.__raiz) != -1

    def __altura_si_balanceado(self, nodo):
        """Devuelve la altura del subárbol, o -1 si no está balanceado."""
        if nodo is None:
            return 0
        altura_izquierda = self.__altura_si_balanceado(nodo.get_izquierdo())
        if altura_izquierda == -1:
            return -1
        altura_derecha = self.__altura_si_balanceado(nodo.get_derecho())
        if altura_derecha == -1:
            return -1
        if abs(altura_izquierda - altura_derecha) > 1:
            return -1
        return 1 + max(altura_izquierda, altura_derecha)

    # --- Sucesor inorden (Tarea 5) ---

    def obtener_nodo(self, dato):
        """Devuelve el Nodo que contiene el dato, o None."""
        nodo_actual = self.__raiz
        while nodo_actual is not None and nodo_actual.get_dato() != dato:
            if dato < nodo_actual.get_dato():
                nodo_actual = nodo_actual.get_izquierdo()
            else:
                nodo_actual = nodo_actual.get_derecho()
        return nodo_actual

    def sucesor(self, dato):
        """Siguiente dato en el recorrido in-orden, o None si no hay."""
        nodo = self.obtener_nodo(dato)
        if nodo is None:
            return None

        # Caso A: tiene hijo derecho -> el menor de ese subárbol.
        if nodo.get_derecho() is not None:
            return self.__nodo_minimo(nodo.get_derecho()).get_dato()

        # Caso B: sin hijo derecho -> el último ancestro desde el que
        # se bajó hacia la izquierda.
        candidato = None
        nodo_actual = self.__raiz
        while nodo_actual is not None:
            if dato < nodo_actual.get_dato():
                candidato = nodo_actual.get_dato()
                nodo_actual = nodo_actual.get_izquierdo()
            elif dato > nodo_actual.get_dato():
                nodo_actual = nodo_actual.get_derecho()
            else:
                break
        return candidato

    # --- Validar ABB (Tarea 6) ---

    def es_abb_valido(self):
        """True si cada dato está dentro del rango que le permiten sus
        ancestros (menores a la izquierda, mayores a la derecha)."""
        return self.__es_valido_en_rango(self.__raiz, float("-inf"),
                                         float("inf"))

    def __es_valido_en_rango(self, nodo, minimo, maximo):
        if nodo is None:
            return True
        dato = nodo.get_dato()
        if not minimo < dato < maximo:
            return False
        return (self.__es_valido_en_rango(nodo.get_izquierdo(), minimo, dato)
                and self.__es_valido_en_rango(nodo.get_derecho(), dato,
                                              maximo))

    # --- Árbol de expresiones ---

    def construir_desde_infija(self, expresion):
        """Arma el árbol de una expresión infija. Ej: a+b*c.

        Cada operando debe ser de un solo carácter.
        """
        simbolos = list(expresion.replace(" ", ""))
        postfija = self.__infija_a_postfija(simbolos)
        self.__raiz = self.__arbol_desde_postfija(postfija)
        self.__cantidad = self.__contar_nodos(self.__raiz)

    def __infija_a_postfija(self, simbolos):
        """Convierte infija a postfija usando una pila de operadores."""
        precedencia = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
        salida = []
        pila_operadores = []

        for simbolo in simbolos:
            if simbolo.isalnum():
                salida.append(simbolo)              # operando
            elif simbolo == '(':
                pila_operadores.append(simbolo)
            elif simbolo == ')':
                # Sacar operadores hasta encontrar el '('.
                while pila_operadores and pila_operadores[-1] != '(':
                    salida.append(pila_operadores.pop())
                pila_operadores.pop()               # descarta el '('
            elif simbolo in precedencia:
                # Sacar los operadores de mayor o igual precedencia.
                while (pila_operadores and pila_operadores[-1] != '('
                       and precedencia.get(pila_operadores[-1], 0)
                       >= precedencia[simbolo]):
                    salida.append(pila_operadores.pop())
                pila_operadores.append(simbolo)

        while pila_operadores:
            salida.append(pila_operadores.pop())
        return salida

    def __arbol_desde_postfija(self, postfija):
        """Construye el árbol leyendo la postfija con una pila de nodos."""
        pila_nodos = []
        for simbolo in postfija:
            nodo = Nodo(simbolo)
            if not simbolo.isalnum():
                # Operador: sus hijos son los dos últimos nodos.
                nodo.set_derecho(pila_nodos.pop())
                nodo.set_izquierdo(pila_nodos.pop())
            pila_nodos.append(nodo)
        return pila_nodos[-1] if pila_nodos else None

    def __contar_nodos(self, nodo):
        if nodo is None:
            return 0
        return (1 + self.__contar_nodos(nodo.get_izquierdo())
                + self.__contar_nodos(nodo.get_derecho()))

    def obtener_postfija(self):
        return " ".join(self.post_orden())

    def obtener_prefija(self):
        return " ".join(self.pre_orden())

    def obtener_infija(self):
        """Infija con paréntesis alrededor de cada operación."""
        return self.__infija_recursiva(self.__raiz)

    def __infija_recursiva(self, nodo):
        if nodo is None:
            return ""
        if nodo.es_hoja():
            return str(nodo.get_dato())
        return (f"({self.__infija_recursiva(nodo.get_izquierdo())} "
                f"{nodo.get_dato()} "
                f"{self.__infija_recursiva(nodo.get_derecho())})")

    # --- Imprimir en consola ---

    def imprimir(self):
        """Dibuja el árbol de lado: la raíz a la izquierda."""
        self.__imprimir_recursivo(self.__raiz, 0)

    def __imprimir_recursivo(self, nodo, nivel):
        if nodo:
            self.__imprimir_recursivo(nodo.get_derecho(), nivel + 1)
            print("    " * nivel + f"[{nodo.get_dato()}]")
            self.__imprimir_recursivo(nodo.get_izquierdo(), nivel + 1)
