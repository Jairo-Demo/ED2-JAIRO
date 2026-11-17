"""Grafo con lista de adyacencia (Unidad IV).

Sirve para grafos dirigidos y no dirigidos (sin pesos).
Incluye: agregar y eliminar vértices y aristas, grados, matriz de
adyacencia, recorridos BFS y DFS, camino más corto (en aristas),
componentes conexas, detección de ciclos y orden topológico.

Ejecutar:  python Grafo.py
"""

from collections import deque


class Grafo:
    """Grafo guardado como diccionario: vértice -> lista de vecinos."""

    def __init__(self, dirigido=False):
        self.dirigido = dirigido
        self.adyacencia = {}

    # ------------------------------------------------------------------
    # Construcción
    # ------------------------------------------------------------------

    def agregar_vertice(self, vertice):
        """Agrega el vértice si todavía no existe."""
        if vertice not in self.adyacencia:
            self.adyacencia[vertice] = []

    def agregar_arista(self, origen, destino):
        """Une origen con destino. Si no es dirigido, también al revés.
        Crea los vértices si no existen y no repite aristas."""
        self.agregar_vertice(origen)
        self.agregar_vertice(destino)
        if destino not in self.adyacencia[origen]:
            self.adyacencia[origen].append(destino)
        if not self.dirigido and origen not in self.adyacencia[destino]:
            self.adyacencia[destino].append(origen)

    def eliminar_arista(self, origen, destino):
        """Quita la arista. Devuelve False si no existía."""
        if not self.existe_arista(origen, destino):
            return False
        self.adyacencia[origen].remove(destino)
        if not self.dirigido:
            self.adyacencia[destino].remove(origen)
        return True

    def eliminar_vertice(self, vertice):
        """Quita el vértice y todas las aristas que lo tocan."""
        if vertice not in self.adyacencia:
            return False
        del self.adyacencia[vertice]
        for vecinos in self.adyacencia.values():
            if vertice in vecinos:
                vecinos.remove(vertice)
        return True

    # ------------------------------------------------------------------
    # Consultas
    # ------------------------------------------------------------------

    def vertices(self):
        return list(self.adyacencia)

    def vecinos(self, vertice):
        return self.adyacencia.get(vertice, [])

    def existe_arista(self, origen, destino):
        return destino in self.adyacencia.get(origen, [])

    def cantidad_vertices(self):
        return len(self.adyacencia)

    def cantidad_aristas(self):
        """En un no dirigido cada arista aparece dos veces en la lista."""
        total = sum(len(vecinos) for vecinos in self.adyacencia.values())
        return total if self.dirigido else total // 2

    def grado(self, vertice):
        """No dirigido: cantidad de vecinos.
        Dirigido: grado de entrada + grado de salida."""
        if self.dirigido:
            return self.grado_entrada(vertice) + self.grado_salida(vertice)
        return len(self.vecinos(vertice))

    def grado_salida(self, vertice):
        """Aristas que salen del vértice."""
        return len(self.vecinos(vertice))

    def grado_entrada(self, vertice):
        """Aristas que llegan al vértice."""
        return sum(1 for vecinos in self.adyacencia.values()
                   if vertice in vecinos)

    def matriz_adyacencia(self):
        """Devuelve (lista de vértices, matriz) con 1 si hay arista."""
        vertices = self.vertices()
        indice = {vertice: i for i, vertice in enumerate(vertices)}
        matriz = [[0] * len(vertices) for _ in vertices]
        for origen, vecinos in self.adyacencia.items():
            for destino in vecinos:
                matriz[indice[origen]][indice[destino]] = 1
        return vertices, matriz

    # ------------------------------------------------------------------
    # Recorrido en amplitud (BFS): usa una cola
    # ------------------------------------------------------------------

    def bfs(self, inicio):
        """Orden de visita por niveles desde 'inicio'."""
        orden, _, _ = self.bfs_completo(inicio)
        return orden

    def bfs_completo(self, inicio):
        """BFS que además devuelve la distancia (en aristas) a cada
        vértice y el padre de cada uno en el árbol BFS."""
        if inicio not in self.adyacencia:
            return [], {}, {}
        orden = []
        distancia = {inicio: 0}
        padre = {inicio: None}
        cola = deque([inicio])
        while cola:
            actual = cola.popleft()
            orden.append(actual)
            for vecino in self.adyacencia[actual]:
                # Se marca al encolar para no encolarlo dos veces.
                if vecino not in distancia:
                    distancia[vecino] = distancia[actual] + 1  # un nivel más
                    padre[vecino] = actual
                    cola.append(vecino)
        return orden, distancia, padre

    def camino_mas_corto(self, inicio, fin):
        """Camino con menos aristas de inicio a fin, o None si no hay.
        BFS lo encuentra porque visita primero lo más cercano."""
        _, _, padre = self.bfs_completo(inicio)
        if fin not in padre:
            return None
        camino = []
        actual = fin
        # Se sube por los padres desde 'fin' hasta el inicio.
        while actual is not None:
            camino.append(actual)
            actual = padre[actual]
        return camino[::-1]  # se invierte: de inicio a fin

    # ------------------------------------------------------------------
    # Recorrido en profundidad (DFS): recursión o pila
    # ------------------------------------------------------------------

    def dfs(self, inicio):
        """DFS recursivo: baja lo más profundo posible antes de volver."""
        orden = []
        if inicio in self.adyacencia:
            self._dfs(inicio, set(), orden)
        return orden

    def _dfs(self, vertice, visitados, orden):
        visitados.add(vertice)
        orden.append(vertice)
        for vecino in self.adyacencia[vertice]:
            if vecino not in visitados:
                self._dfs(vecino, visitados, orden)  # baja por el vecino

    def dfs_iterativo(self, inicio):
        """DFS con una pila. Los vecinos se apilan al revés para que
        salgan en el mismo orden que en la versión recursiva."""
        if inicio not in self.adyacencia:
            return []
        orden = []
        visitados = set()
        pila = [inicio]
        while pila:
            actual = pila.pop()  # sale el último que entró
            if actual in visitados:
                continue
            visitados.add(actual)
            orden.append(actual)
            for vecino in reversed(self.adyacencia[actual]):
                if vecino not in visitados:
                    pila.append(vecino)
        return orden

    # ------------------------------------------------------------------
    # Conexidad
    # ------------------------------------------------------------------

    def es_conexo(self):
        """True si desde un vértice se llega a todos (ignorando la
        dirección de las aristas si es dirigido)."""
        if not self.adyacencia:
            return True
        return len(self.componentes_conexas()) == 1

    def componentes_conexas(self):
        """Grupos de vértices conectados entre sí (con BFS)."""
        grafo = self if not self.dirigido else self._version_no_dirigida()
        componentes = []
        visitados = set()
        for vertice in grafo.vertices():
            if vertice not in visitados:
                # Vértice nuevo: el BFS trae todo su grupo.
                componente = grafo.bfs(vertice)
                visitados.update(componente)
                componentes.append(componente)
        return componentes

    def _version_no_dirigida(self):
        copia = Grafo(dirigido=False)
        for origen, vecinos in self.adyacencia.items():
            copia.agregar_vertice(origen)
            for destino in vecinos:
                copia.agregar_arista(origen, destino)
        return copia

    # ------------------------------------------------------------------
    # Ciclos
    # ------------------------------------------------------------------

    def tiene_ciclo(self):
        """True si hay al menos un ciclo."""
        if self.dirigido:
            return self._ciclo_dirigido()
        return self._ciclo_no_dirigido()

    def _ciclo_no_dirigido(self):
        """DFS recordando el padre: si se encuentra un vecino ya visitado
        que NO es el padre, hay un ciclo."""
        visitados = set()

        # Devuelve True si encuentra un ciclo desde 'vertice'.
        def dfs(vertice, padre):
            visitados.add(vertice)
            for vecino in self.adyacencia[vertice]:
                if vecino not in visitados:
                    # Baja al vecino; 'vertice' pasa a ser su padre.
                    if dfs(vecino, vertice):
                        return True
                elif vecino != padre:
                    # Ya visitado y no es el padre: hay ciclo.
                    return True
            return False

        # Un DFS por cada parte del grafo que falte visitar.
        for vertice in self.adyacencia:
            if vertice not in visitados and dfs(vertice, None):
                return True
        return False

    def _ciclo_dirigido(self):
        """DFS con tres colores:
        BLANCO = sin visitar, GRIS = en el camino actual,
        NEGRO = terminado. Llegar a un GRIS es volver atrás: ciclo."""
        blanco, gris, negro = 0, 1, 2
        color = {vertice: blanco for vertice in self.adyacencia}

        def dfs(vertice):
            color[vertice] = gris
            for vecino in self.adyacencia[vertice]:
                if color[vecino] == gris:
                    return True  # vuelve al camino actual: ciclo
                if color[vecino] == blanco and dfs(vecino):
                    return True
            color[vertice] = negro  # terminado
            return False

        # Un DFS desde cada vértice que siga sin visitar.
        return any(color[vertice] == blanco and dfs(vertice)
                   for vertice in self.adyacencia)

    # ------------------------------------------------------------------
    # Orden topológico. Solo para grafos dirigidos.
    # ------------------------------------------------------------------

    def orden_topologico(self):
        """Algoritmo de Kahn. Devuelve la lista o None si hay ciclo.

        1. Contar las aristas que llegan a cada vértice (grado de entrada).
        2. Poner en una cola los que tienen grado 0.
        3. Sacar uno, agregarlo al resultado y "borrar" sus aristas;
           los vecinos que queden en 0 entran a la cola.
        """
        # Paso 1: contar aristas que llegan a cada vértice.
        grado_entrada = {vertice: 0 for vertice in self.adyacencia}
        for vecinos in self.adyacencia.values():
            for destino in vecinos:
                grado_entrada[destino] += 1

        # Paso 2: empiezan los que no dependen de nadie.
        cola = deque(vertice for vertice, grado in grado_entrada.items()
                     if grado == 0)
        resultado = []
        while cola:
            actual = cola.popleft()
            resultado.append(actual)
            # Paso 3: sus vecinos tienen un requisito menos.
            for vecino in self.adyacencia[actual]:
                grado_entrada[vecino] -= 1
                if grado_entrada[vecino] == 0:
                    cola.append(vecino)

        # Si faltan vértices es porque están en un ciclo.
        if len(resultado) != len(self.adyacencia):
            return None
        return resultado

    def orden_topologico_dfs(self):
        """Otra forma: al terminar un vértice en el DFS se agrega al
        inicio de la lista. Devuelve None si hay ciclo."""
        if self.tiene_ciclo():
            return None
        visitados = set()
        resultado = []

        def dfs(vertice):
            visitados.add(vertice)
            for vecino in self.adyacencia[vertice]:
                if vecino not in visitados:
                    dfs(vecino)
            resultado.insert(0, vertice)  # al terminar, va adelante

        for vertice in self.adyacencia:
            if vertice not in visitados:
                dfs(vertice)
        return resultado

    # ------------------------------------------------------------------
    # Mostrar
    # ------------------------------------------------------------------

    def imprimir(self):
        """Muestra la lista de adyacencia."""
        flecha = "->" if self.dirigido else "--"
        for vertice, vecinos in self.adyacencia.items():
            print(f"{vertice} {flecha} {vecinos}")

    def imprimir_matriz(self):
        """Muestra la matriz de adyacencia."""
        vertices, matriz = self.matriz_adyacencia()
        print("    " + "  ".join(str(v) for v in vertices))
        for vertice, fila in zip(vertices, matriz):
            print(f"{vertice}   " + "  ".join(str(celda) for celda in fila))


# ----------------------------------------------------------------------
# Demostración
# ----------------------------------------------------------------------

if __name__ == "__main__":
    print("=== Grafo no dirigido ===")
    grafo = Grafo()
    for origen, destino in [("A", "B"), ("A", "C"), ("B", "D"),
                            ("C", "D"), ("D", "E")]:
        grafo.agregar_arista(origen, destino)
    grafo.imprimir()
    print("Matriz de adyacencia:")
    grafo.imprimir_matriz()
    print("Vértices:", grafo.cantidad_vertices(),
          "| Aristas:", grafo.cantidad_aristas())
    print("BFS desde A:", grafo.bfs("A"))
    print("DFS desde A:", grafo.dfs("A"))
    print("DFS iterativo desde A:", grafo.dfs_iterativo("A"))
    print("Camino más corto A -> E:", grafo.camino_mas_corto("A", "E"))
    print("¿Es conexo?", grafo.es_conexo())
    print("¿Tiene ciclo?", grafo.tiene_ciclo())

    print("\n=== Grafo dirigido (tareas) ===")
    tareas = Grafo(dirigido=True)
    for origen, destino in [("levantarse", "ducharse"),
                            ("levantarse", "desayunar"),
                            ("ducharse", "vestirse"),
                            ("desayunar", "salir"),
                            ("vestirse", "salir")]:
        tareas.agregar_arista(origen, destino)
    tareas.imprimir()
    print("¿Tiene ciclo?", tareas.tiene_ciclo())
    print("Orden topológico (Kahn):", tareas.orden_topologico())
    print("Orden topológico (DFS): ", tareas.orden_topologico_dfs())

    tareas.agregar_arista("salir", "levantarse")
    print("Con la arista salir -> levantarse:")
    print("¿Tiene ciclo?", tareas.tiene_ciclo())
    print("Orden topológico:", tareas.orden_topologico())
