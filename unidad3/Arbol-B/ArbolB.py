"""Árbol-B de orden m (Unidad III).

Un Árbol-B es un árbol M-Vías que siempre se mantiene balanceado:
    - Cada nodo guarda como máximo m - 1 claves ordenadas.
    - Cada nodo que no es la raíz guarda como mínimo ceil(m/2) - 1 claves.
    - Un nodo interno con k claves tiene exactamente k + 1 hijos.
    - Todas las hojas están en el mismo nivel.

Operaciones: buscar, insertar (con división o "split") y eliminar
(con préstamo o fusión). Todas son O(log n).

Ejecutar:  python ArbolB.py
"""

from collections import deque


class NodoB:
    """Nodo del Árbol-B: una lista de claves y una lista de hijos."""

    def __init__(self, es_hoja=True):
        self.claves = []
        self.hijos = []
        self.es_hoja = es_hoja

    def __repr__(self):
        return f"NodoB({self.claves})"


class ArbolB:
    """Árbol-B con buscar, insertar, eliminar, recorridos y consultas."""

    def __init__(self, orden):
        if orden < 3:
            raise ValueError("El orden debe ser al menos 3")
        self.orden = orden
        self.max_claves = orden - 1
        # ceil(orden / 2) - 1, escrito con división entera.
        self.min_claves = (orden + 1) // 2 - 1
        self.raiz = None
        # Descripción de lo que pasó en la última inserción o eliminación.
        self.pasos = []

    def esta_vacio(self):
        return self.raiz is None

    # ------------------------------------------------------------------
    # Buscar
    # ------------------------------------------------------------------

    def _posicion(self, nodo, clave):
        """Primera posición cuya clave es mayor o igual a 'clave'.
        Si la clave no está en el nodo, es el hijo por donde se baja."""
        posicion = 0
        # Se avanza mientras queden claves y la buscada sea mayor.
        # Se detiene en la primera clave >= 'clave' (o al final).
        while posicion < len(nodo.claves) and clave > nodo.claves[posicion]:
            posicion += 1
        return posicion

    def buscar(self, clave):
        """True si la clave está en el árbol."""
        nodo = self.raiz
        while nodo is not None:
            posicion = self._posicion(nodo, clave)
            # Primero se revisa que la posición exista (no se pasó del
            # final) y luego si en esa posición está la clave.
            if posicion < len(nodo.claves) and nodo.claves[posicion] == clave:
                return True
            # En una hoja no hay más donde bajar: no existe.
            if nodo.es_hoja:
                return False
            # La misma posición indica por qué hijo bajar.
            nodo = nodo.hijos[posicion]
        return False

    def camino_busqueda(self, clave):
        """Lista con las claves de cada nodo visitado al buscar.
        Sirve para trazar la búsqueda a mano."""
        camino = []
        nodo = self.raiz
        while nodo is not None:
            # list() guarda una copia de las claves de este nodo.
            camino.append(list(nodo.claves))
            posicion = self._posicion(nodo, clave)
            if posicion < len(nodo.claves) and nodo.claves[posicion] == clave:
                break
            if nodo.es_hoja:
                break
            nodo = nodo.hijos[posicion]
        return camino

    # ------------------------------------------------------------------
    # Insertar
    # ------------------------------------------------------------------

    def insertar(self, clave):
        """Inserta la clave. Devuelve False si ya existía."""
        self.pasos = []
        if self.buscar(clave):
            self.pasos.append(f"{clave} ya existe, no se inserta")
            return False

        if self.raiz is None:
            self.raiz = NodoB(es_hoja=True)
            self.raiz.claves.append(clave)
            self.pasos.append(f"{clave} es la primera clave (nueva raíz)")
            return True

        # Si la raíz se dividió, 'promocion' trae lo que sube; si no,
        # trae None.
        promocion = self._insertar_recursivo(self.raiz, clave)

        # Si la raíz se dividió, se crea una raíz nueva encima:
        # así el árbol crece hacia arriba y las hojas siguen al mismo nivel.
        if promocion is not None:
            clave_media, nodo_derecho = promocion   # se separa la tupla
            nueva_raiz = NodoB(es_hoja=False)
            nueva_raiz.claves = [clave_media]
            # Hijo izquierdo: la raíz vieja (ya recortada por _dividir).
            # Hijo derecho: el nodo nuevo con la otra mitad.
            nueva_raiz.hijos = [self.raiz, nodo_derecho]
            self.raiz = nueva_raiz
            self.pasos.append(f"se crea una raíz nueva con {clave_media}")
        return True

    def _insertar_recursivo(self, nodo, clave):
        """Baja hasta la hoja, inserta y, al volver, divide los nodos
        que quedaron con demasiadas claves.

        Devuelve None si no hubo división, o (clave_media, nodo_derecho)
        para que el padre reciba la clave que sube."""
        posicion = self._posicion(nodo, clave)

        if nodo.es_hoja:
            # insert() mete la clave en esa posición y corre las demás
            # a la derecha, así la lista sigue ordenada.
            nodo.claves.insert(posicion, clave)
            self.pasos.append(f"{clave} se inserta en la hoja {nodo.claves}")
        else:
            # Se baja al hijo que corresponde. Cuando la llamada vuelve,
            # se sabe si ese hijo se dividió.
            promocion = self._insertar_recursivo(nodo.hijos[posicion], clave)
            if promocion is not None:
                clave_media, nodo_derecho = promocion
                # La clave que sube queda en el lugar por donde se bajó,
                # y el nodo nuevo queda justo a la derecha del hijo.
                nodo.claves.insert(posicion, clave_media)
                nodo.hijos.insert(posicion + 1, nodo_derecho)

        # Al volver de la recursión: si este nodo quedó con una clave de
        # más, se divide y se le avisa al padre (que hará lo mismo).
        if len(nodo.claves) > self.max_claves:
            return self._dividir(nodo)
        return None

    def _dividir(self, nodo):
        """Split: parte el nodo desbordado en dos y devuelve la clave
        del medio (que sube al padre) y el nodo de la derecha."""
        medio = len(nodo.claves) // 2
        clave_media = nodo.claves[medio]

        nodo_derecho = NodoB(es_hoja=nodo.es_hoja)
        # Ejemplo con [5, 10, 12, 13, 15] y medio = 2:
        #   claves[medio + 1:] = [13, 15]  -> van al nodo derecho
        #   claves[:medio]     = [5, 10]   -> se quedan en este nodo
        #   claves[medio]      = 12        -> sube al padre
        nodo_derecho.claves = nodo.claves[medio + 1:]
        nodo.claves = nodo.claves[:medio]

        # Si no es hoja, los hijos también se reparten: el izquierdo se
        # queda con medio + 1 hijos (uno más que sus claves) y el
        # derecho con el resto.
        if not nodo.es_hoja:
            nodo_derecho.hijos = nodo.hijos[medio + 1:]
            nodo.hijos = nodo.hijos[:medio + 1]

        self.pasos.append(
            f"split: {nodo.claves} | sube {clave_media} | "
            f"{nodo_derecho.claves}")
        return clave_media, nodo_derecho

    # ------------------------------------------------------------------
    # Eliminar
    # ------------------------------------------------------------------

    def eliminar(self, clave):
        """Elimina la clave. Devuelve False si no existía."""
        self.pasos = []
        if not self.buscar(clave):
            self.pasos.append(f"{clave} no existe")
            return False

        self._eliminar_recursivo(self.raiz, clave)

        # Si la raíz se quedó sin claves, el árbol baja un nivel.
        # 'not lista' es True cuando la lista está vacía.
        if not self.raiz.claves:
            if self.raiz.es_hoja:
                self.raiz = None
                self.pasos.append("el árbol quedó vacío")
            else:
                # Una raíz sin claves tiene un solo hijo: ese sube.
                self.raiz = self.raiz.hijos[0]
                self.pasos.append("la raíz quedó vacía: el árbol baja "
                                  "un nivel")
        return True

    def _eliminar_recursivo(self, nodo, clave):
        posicion = self._posicion(nodo, clave)
        # True si la clave está en este nodo (misma idea que buscar).
        esta_aqui = (posicion < len(nodo.claves)
                     and nodo.claves[posicion] == clave)

        if esta_aqui and nodo.es_hoja:
            # Caso A: la clave está en una hoja, se quita directamente.
            nodo.claves.pop(posicion)   # pop() quita por posición
            self.pasos.append(f"{clave} se quita de la hoja")
            return

        if esta_aqui:
            # Caso B: nodo interno. Se reemplaza por su sucesor inorden
            # (la menor clave del subárbol derecho, siempre en una hoja)
            # y luego se elimina el sucesor de ese subárbol.
            sucesor = self._minimo_desde(nodo.hijos[posicion + 1])
            nodo.claves[posicion] = sucesor
            self.pasos.append(f"{clave} se reemplaza por su sucesor "
                              f"{sucesor}")
            # Ahora hay que borrar el sucesor, que está en el hijo de
            # la derecha (posicion + 1).
            posicion += 1
            clave = sucesor

        # La clave (o el sucesor) está en el hijo 'posicion'.
        self._eliminar_recursivo(nodo.hijos[posicion], clave)
        # Al volver: ese hijo pudo quedar con menos claves que el
        # mínimo, entonces se arregla desde aquí (el padre).
        self._corregir_hijo(nodo, posicion)

    def _corregir_hijo(self, padre, posicion):
        """Si el hijo quedó con menos claves que el mínimo, se arregla
        pidiendo prestado a un hermano o fusionándolo con uno."""
        hijo = padre.hijos[posicion]
        if len(hijo.claves) >= self.min_claves:
            return

        # Hermanos vecinos. El primer hijo no tiene hermano izquierdo y
        # el último no tiene derecho: en esos casos se usa None.
        izquierdo = padre.hijos[posicion - 1] if posicion > 0 else None
        derecho = (padre.hijos[posicion + 1]
                   if posicion + 1 < len(padre.hijos) else None)

        # Un hermano puede prestar solo si tiene MÁS que el mínimo
        # (después de prestar sigue cumpliendo la regla).
        if izquierdo is not None and len(izquierdo.claves) > self.min_claves:
            self._prestar_de_izquierdo(padre, posicion)
        elif derecho is not None and len(derecho.claves) > self.min_claves:
            self._prestar_de_derecho(padre, posicion)
        # Nadie puede prestar: se fusiona. _fusionar(padre, i) une los
        # hijos i e i + 1, por eso con el izquierdo se pasa posicion - 1.
        elif izquierdo is not None:
            self._fusionar(padre, posicion - 1)
        else:
            self._fusionar(padre, posicion)

    def _prestar_de_izquierdo(self, padre, posicion):
        """Rotación a la derecha: la clave del padre baja al hijo y la
        mayor clave del hermano izquierdo sube al padre."""
        hijo = padre.hijos[posicion]
        izquierdo = padre.hijos[posicion - 1]

        # La clave del padre que separa a los dos hermanos es
        # claves[posicion - 1]; baja al inicio del hijo.
        hijo.claves.insert(0, padre.claves[posicion - 1])
        # pop() sin número saca la última (la mayor) del izquierdo, y
        # esa ocupa el lugar que dejó libre el padre.
        padre.claves[posicion - 1] = izquierdo.claves.pop()
        # El último hijo del hermano pasa a ser el primero del nodo.
        if not hijo.es_hoja:
            hijo.hijos.insert(0, izquierdo.hijos.pop())
        self.pasos.append(f"préstamo del hermano izquierdo: sube "
                          f"{padre.claves[posicion - 1]}")

    def _prestar_de_derecho(self, padre, posicion):
        """Rotación a la izquierda: la clave del padre baja al hijo y la
        menor clave del hermano derecho sube al padre."""
        hijo = padre.hijos[posicion]
        derecho = padre.hijos[posicion + 1]

        # La clave del padre que los separa es claves[posicion]; baja
        # al final del hijo.
        hijo.claves.append(padre.claves[posicion])
        # pop(0) saca la primera (la menor) del derecho y sube al padre.
        padre.claves[posicion] = derecho.claves.pop(0)
        # El primer hijo del hermano pasa a ser el último del nodo.
        if not hijo.es_hoja:
            hijo.hijos.append(derecho.hijos.pop(0))
        self.pasos.append(f"préstamo del hermano derecho: sube "
                          f"{padre.claves[posicion]}")

    def _fusionar(self, padre, posicion):
        """Une hijos[posicion] + claves[posicion] del padre +
        hijos[posicion + 1] en un solo nodo."""
        izquierdo = padre.hijos[posicion]
        # pop() saca al hermano derecho y la clave que los separaba:
        # el padre queda con un hijo y una clave menos.
        derecho = padre.hijos.pop(posicion + 1)
        clave_padre = padre.claves.pop(posicion)

        # Todo se junta en el izquierdo, en orden:
        # claves del izquierdo + clave del padre + claves del derecho.
        izquierdo.claves = izquierdo.claves + [clave_padre] + derecho.claves
        izquierdo.hijos = izquierdo.hijos + derecho.hijos
        self.pasos.append(f"fusión: baja {clave_padre}, queda "
                          f"{izquierdo.claves}")

    # ------------------------------------------------------------------
    # Recorridos
    # ------------------------------------------------------------------

    def en_orden(self):
        """Claves de menor a mayor: hijo, clave, hijo, clave, ..., hijo."""
        resultado = []
        self._en_orden(self.raiz, resultado)
        return resultado

    def _en_orden(self, nodo, resultado):
        if nodo is None:
            return
        # enumerate() da la posición y la clave a la vez.
        for posicion, clave in enumerate(nodo.claves):
            # Antes de cada clave van las menores: las de su hijo
            # izquierdo (el que tiene su misma posición).
            if not nodo.es_hoja:
                self._en_orden(nodo.hijos[posicion], resultado)
            resultado.append(clave)
        # Al final, el último hijo ([-1]) tiene las mayores de todas.
        if not nodo.es_hoja:
            self._en_orden(nodo.hijos[-1], resultado)

    def pre_orden(self):
        """Primero las claves del nodo, luego cada hijo."""
        resultado = []
        self._pre_orden(self.raiz, resultado)
        return resultado

    def _pre_orden(self, nodo, resultado):
        if nodo is None:
            return
        resultado.extend(nodo.claves)
        for hijo in nodo.hijos:
            self._pre_orden(hijo, resultado)

    def post_orden(self):
        """Primero cada hijo, luego las claves del nodo."""
        resultado = []
        self._post_orden(self.raiz, resultado)
        return resultado

    def _post_orden(self, nodo, resultado):
        if nodo is None:
            return
        for hijo in nodo.hijos:
            self._post_orden(hijo, resultado)
        resultado.extend(nodo.claves)

    def por_niveles(self):
        """Lista de niveles; cada nivel es una lista de nodos (claves)."""
        if self.raiz is None:
            return []
        niveles = []
        # La cola guarda parejas (nodo, nivel en el que está).
        cola = deque([(self.raiz, 0)])
        while cola:
            nodo, nivel = cola.popleft()
            # Primer nodo de un nivel nuevo: se crea su lista.
            if nivel == len(niveles):
                niveles.append([])
            niveles[nivel].append(list(nodo.claves))
            # Los hijos están un nivel más abajo.
            for hijo in nodo.hijos:
                cola.append((hijo, nivel + 1))
        return niveles

    # ------------------------------------------------------------------
    # Consultas
    # ------------------------------------------------------------------

    def altura(self):
        """Niveles debajo de la raíz. Vacío o solo raíz: 0.
        Como todas las hojas están al mismo nivel, basta bajar siempre
        por el primer hijo."""
        if self.raiz is None:
            return 0
        altura = 0
        nodo = self.raiz
        while not nodo.es_hoja:
            altura += 1
            nodo = nodo.hijos[0]
        return altura

    def _minimo_desde(self, nodo):
        """Menor clave del subárbol: siempre a la izquierda."""
        while not nodo.es_hoja:
            nodo = nodo.hijos[0]
        return nodo.claves[0]

    def minimo(self):
        # Si el árbol está vacío no hay mínimo.
        return None if self.raiz is None else self._minimo_desde(self.raiz)

    def maximo(self):
        """Mayor clave: siempre a la derecha."""
        if self.raiz is None:
            return None
        nodo = self.raiz
        while not nodo.es_hoja:
            nodo = nodo.hijos[-1]
        return nodo.claves[-1]

    def cantidad_claves(self):
        return len(self.en_orden())

    def cantidad_nodos(self):
        return sum(len(nivel) for nivel in self.por_niveles())

    def es_valido(self):
        """Revisa las 5 propiedades del Árbol-B. Devuelve True o False."""
        if self.raiz is None:
            return True
        # Aquí se anotan los niveles donde aparecen hojas. Un set no
        # guarda repetidos: si al final tiene 1 solo valor, todas las
        # hojas están en el mismo nivel.
        niveles_hojas = set()
        if not self._es_valido(self.raiz, 0, None, None, niveles_hojas):
            return False
        # Propiedad 4: todas las hojas en el mismo nivel.
        return len(niveles_hojas) == 1

    def _es_valido(self, nodo, nivel, menor, mayor, niveles_hojas):
        claves = nodo.claves
        # Cantidad de claves permitida (la raíz puede tener solo 1).
        minimo = 1 if nodo is self.raiz else self.min_claves
        if not minimo <= len(claves) <= self.max_claves:
            return False
        # Claves ordenadas y dentro del rango que da el padre.
        # any() es True si algún par de claves seguidas está desordenado.
        if any(claves[i] >= claves[i + 1] for i in range(len(claves) - 1)):
            return False
        if menor is not None and claves[0] <= menor:
            return False
        if mayor is not None and claves[-1] >= mayor:
            return False

        if nodo.es_hoja:
            niveles_hojas.add(nivel)
            # Una hoja no debe tener hijos: True si la lista está vacía.
            return not nodo.hijos
        # Un nodo interno con k claves tiene k + 1 hijos.
        if len(nodo.hijos) != len(claves) + 1:
            return False
        # Rangos de cada hijo. Ej.: claves [30, 70] dentro de (10, 90)
        # da limites [10, 30, 70, 90]: hijo 0 entre 10 y 30, hijo 1
        # entre 30 y 70, hijo 2 entre 70 y 90.
        limites = [menor] + claves + [mayor]
        for posicion, hijo in enumerate(nodo.hijos):
            if not self._es_valido(hijo, nivel + 1, limites[posicion],
                                   limites[posicion + 1], niveles_hojas):
                return False
        return True

    def imprimir(self):
        """Muestra el árbol por niveles en la consola."""
        if self.raiz is None:
            print("(árbol vacío)")
            return
        for nivel, nodos in enumerate(self.por_niveles()):
            print(f"Nivel {nivel}: " + "  ".join(str(n) for n in nodos))


# ----------------------------------------------------------------------
# Demostración
# ----------------------------------------------------------------------

if __name__ == "__main__":
    print("=== Árbol-B de orden 5 (máx 4 claves, mín 2) ===")
    arbol = ArbolB(5)
    valores = [3, 7, 1, 14, 5, 11, 17, 13, 6, 23, 12, 20, 26, 4, 16,
               18, 24, 25, 19]
    for valor in valores:
        arbol.insertar(valor)
    arbol.imprimir()
    print("Altura:", arbol.altura())
    print("En orden:", arbol.en_orden())
    print("Válido:", arbol.es_valido())
    for clave in [14, 25, 99]:
        print(f"Buscar {clave}: {arbol.buscar(clave)}")

    print("\n=== Inserción con split (orden 3) ===")
    arbol3 = ArbolB(3)
    for valor in [10, 20, 30, 40, 50]:
        arbol3.insertar(valor)
        print(f"Insertar {valor}: " + "; ".join(arbol3.pasos))
        arbol3.imprimir()

    print("\n=== Eliminación con préstamo (orden 5) ===")
    arbol_prestamo = ArbolB(5)
    for valor in [30, 60, 10, 20, 40, 50, 70, 80, 90]:
        arbol_prestamo.insertar(valor)
    arbol_prestamo.imprimir()
    arbol_prestamo.eliminar(40)
    print("Eliminar 40: " + "; ".join(arbol_prestamo.pasos))
    arbol_prestamo.imprimir()

    print("\n=== Eliminación con fusión (orden 3) ===")
    arbol_fusion = ArbolB(3)
    for valor in [10, 20, 30, 40, 50]:
        arbol_fusion.insertar(valor)
    arbol_fusion.imprimir()
    arbol_fusion.eliminar(10)
    print("Eliminar 10: " + "; ".join(arbol_fusion.pasos))
    arbol_fusion.imprimir()
