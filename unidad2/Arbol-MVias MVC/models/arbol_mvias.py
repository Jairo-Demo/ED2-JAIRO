"""Árbol M-Vías de búsqueda.

Cada nodo guarda hasta (orden - 1) claves. Una clave nueva se guarda en
el primer nodo con espacio libre del camino; si el nodo está lleno, se
baja por el hijo que le corresponde.
"""

from collections import deque

from models.nodo_mvias import NodoMVias


class ArbolMVias:
    """Árbol M-Vías con buscar, insertar, recorridos, altura,
    mínimo y máximo."""

    def __init__(self, orden):
        if orden < 2:
            raise ValueError("El orden debe ser al menos 2")
        self.orden = orden
        self.raiz = None

    def esta_vacio(self):
        return self.raiz is None

    # --- Buscar ---

    def buscar(self, clave):
        """True si la clave está en el árbol."""
        return self._buscar_recursivo(self.raiz, clave)

    def _buscar_recursivo(self, nodo, clave):
        if nodo is None:
            return False
        claves = nodo.get_claves()
        hijos = nodo.get_hijos()

        for posicion, clave_nodo in enumerate(claves):
            if clave == clave_nodo:
                return True
            if clave < clave_nodo:
                # Es menor: está en el hijo de la izquierda de esa clave.
                if posicion < len(hijos):
                    return self._buscar_recursivo(hijos[posicion], clave)
                return False

        # Es mayor que todas: está en el último hijo.
        if len(hijos) > len(claves):
            return self._buscar_recursivo(hijos[-1], clave)
        return False

    # --- Insertar ---

    def insertar(self, clave):
        """Inserta la clave (si ya existe se vuelve a agregar)."""
        if self.raiz is None:
            self.raiz = NodoMVias(self.orden)
            self.raiz.get_claves().append(clave)
            return
        self._insertar_recursivo(self.raiz, clave)

    def _insertar_recursivo(self, nodo, clave):
        claves = nodo.get_claves()
        hijos = nodo.get_hijos()

        # Si hay espacio en este nodo, la clave se queda aquí.
        if not nodo.esta_lleno():
            self._insertar_ordenado(claves, clave)
            return

        # Nodo lleno: buscar por qué hijo bajar.
        posicion = 0
        while posicion < len(claves) and clave > claves[posicion]:
            posicion += 1

        # Asegurar que exista un lugar para cada hijo posible.
        while len(hijos) < len(claves) + 1:
            hijos.append(None)

        if hijos[posicion] is not None:
            self._insertar_recursivo(hijos[posicion], clave)
        else:
            # No hay hijo en esa posición: se crea uno nuevo.
            nuevo_nodo = NodoMVias(self.orden)
            nuevo_nodo.get_claves().append(clave)
            hijos[posicion] = nuevo_nodo

    def _insertar_ordenado(self, lista, valor):
        """Inserta el valor en la lista manteniéndola ordenada."""
        posicion = 0
        while posicion < len(lista) and valor > lista[posicion]:
            posicion += 1
        lista.insert(posicion, valor)

    # --- Recorridos ---

    def en_orden(self):
        """Claves de menor a mayor: hijo, clave, hijo, clave, ..."""
        resultado = []
        self._en_orden_recursivo(self.raiz, resultado)
        return resultado

    def _en_orden_recursivo(self, nodo, resultado):
        if nodo is None:
            return
        claves = nodo.get_claves()
        hijos = nodo.get_hijos()
        for posicion, clave in enumerate(claves):
            if posicion < len(hijos):
                self._en_orden_recursivo(hijos[posicion], resultado)
            resultado.append(clave)
        # Último hijo (claves mayores que todas las del nodo).
        if len(hijos) > len(claves):
            self._en_orden_recursivo(hijos[len(claves)], resultado)

    def pre_orden(self):
        """Primero las claves del nodo, después sus hijos."""
        resultado = []
        self._pre_orden_recursivo(self.raiz, resultado)
        return resultado

    def _pre_orden_recursivo(self, nodo, resultado):
        if nodo is None:
            return
        resultado.extend(nodo.get_claves())
        for hijo in nodo.get_hijos():
            self._pre_orden_recursivo(hijo, resultado)

    def post_orden(self):
        """Primero los hijos, después las claves del nodo."""
        resultado = []
        self._post_orden_recursivo(self.raiz, resultado)
        return resultado

    def _post_orden_recursivo(self, nodo, resultado):
        if nodo is None:
            return
        for hijo in nodo.get_hijos():
            self._post_orden_recursivo(hijo, resultado)
        resultado.extend(nodo.get_claves())

    def por_niveles(self):
        """Claves nivel por nivel, usando una cola."""
        if self.esta_vacio():
            return []
        cola = deque([self.raiz])
        resultado = []
        while cola:
            nodo = cola.popleft()
            resultado.extend(nodo.get_claves())
            for hijo in nodo.get_hijos():
                if hijo is not None:
                    cola.append(hijo)
        return resultado

    # --- Altura, mínimo y máximo ---

    def altura(self):
        """0 si está vacío; 1 si solo existe la raíz."""
        return self._altura_recursiva(self.raiz)

    def _altura_recursiva(self, nodo):
        if nodo is None:
            return 0
        alturas_hijos = [self._altura_recursiva(hijo)
                         for hijo in nodo.get_hijos() if hijo is not None]
        return 1 + max(alturas_hijos, default=0)

    def minimo(self):
        """Primera clave del nodo de más a la izquierda."""
        if self.esta_vacio():
            return None
        nodo = self.raiz
        while nodo.get_hijos() and nodo.get_hijos()[0] is not None:
            nodo = nodo.get_hijos()[0]
        return nodo.get_claves()[0]

    def maximo(self):
        """Última clave del nodo de más a la derecha."""
        if self.esta_vacio():
            return None
        nodo = self.raiz
        while nodo.get_hijos() and nodo.get_hijos()[-1] is not None:
            nodo = nodo.get_hijos()[-1]
        return nodo.get_claves()[-1]

    # --- Texto para mostrar el árbol por niveles ---

    def obtener_niveles_texto(self):
        """Lista de líneas 'Nivel n: [claves] | [claves] ...'."""
        if self.esta_vacio():
            return ["(árbol vacío)"]

        cola = deque([(self.raiz, 0)])
        nivel_actual = 0
        nodos_del_nivel = []
        lineas = []

        while cola:
            nodo, nivel = cola.popleft()
            if nivel != nivel_actual:
                # Empieza un nivel nuevo: guardar la línea anterior.
                lineas.append(self._linea_nivel(nivel_actual,
                                                nodos_del_nivel))
                nodos_del_nivel = []
                nivel_actual = nivel
            nodos_del_nivel.append(nodo.get_claves())
            for hijo in nodo.get_hijos():
                if hijo is not None:
                    cola.append((hijo, nivel + 1))

        lineas.append(self._linea_nivel(nivel_actual, nodos_del_nivel))
        return lineas

    def _linea_nivel(self, nivel, nodos):
        return f"Nivel {nivel}: " + "  |  ".join(str(claves)
                                                 for claves in nodos)
