"""Grafo pesado y sus algoritmos clásicos (Unidad V).

Un grafo pesado guarda un número (peso o costo) en cada arista.
Algoritmos:
    - Dijkstra:        camino más corto desde un origen (pesos >= 0).
    - Floyd-Warshall:  camino más corto entre todos los pares.
    - Warshall:        cierre transitivo (¿hay algún camino de i a j?).
    - Prim y Kruskal:  árbol de expansión mínima (MST).

Ejecutar:  python GrafoPesado.py
"""

import heapq

INFINITO = float("inf")


class UnionFind:
    """Conjuntos disjuntos: dice rápido si dos vértices ya están en el
    mismo grupo. Lo usa Kruskal para no formar ciclos."""

    def __init__(self, elementos):
        # Al inicio cada elemento es su propio grupo (su propio jefe).
        self.padre = {elemento: elemento for elemento in elementos}
        self.rango = {elemento: 0 for elemento in elementos}

    def encontrar(self, elemento):
        """Jefe (representante) del grupo. Comprime el camino para que
        las próximas búsquedas sean más rápidas."""
        if self.padre[elemento] != elemento:
            # Sube hasta el jefe y lo conecta directo.
            self.padre[elemento] = self.encontrar(self.padre[elemento])
        return self.padre[elemento]

    def unir(self, primero, segundo):
        """Une los dos grupos. Devuelve False si ya estaban juntos."""
        jefe_1 = self.encontrar(primero)
        jefe_2 = self.encontrar(segundo)
        if jefe_1 == jefe_2:
            return False  # mismo grupo: formaría ciclo
        # El árbol más bajo se cuelga del más alto.
        if self.rango[jefe_1] < self.rango[jefe_2]:
            jefe_1, jefe_2 = jefe_2, jefe_1
        self.padre[jefe_2] = jefe_1
        if self.rango[jefe_1] == self.rango[jefe_2]:
            self.rango[jefe_1] += 1
        return True


class GrafoPesado:
    """Lista de adyacencia: vértice -> lista de (vecino, peso)."""

    def __init__(self, dirigido=False):
        self.dirigido = dirigido
        self.adyacencia = {}

    # ------------------------------------------------------------------
    # Construcción y consultas
    # ------------------------------------------------------------------

    def agregar_vertice(self, vertice):
        if vertice not in self.adyacencia:
            self.adyacencia[vertice] = []

    def agregar_arista(self, origen, destino, peso):
        """Agrega la arista con su peso (y la de vuelta si no es
        dirigido)."""
        self.agregar_vertice(origen)
        self.agregar_vertice(destino)
        self.adyacencia[origen].append((destino, peso))
        if not self.dirigido:
            self.adyacencia[destino].append((origen, peso))

    def vertices(self):
        """Vértices ordenados (si se pueden comparar), para que las
        tablas y matrices salgan siempre en el mismo orden."""
        try:
            return sorted(self.adyacencia)
        except TypeError:
            return list(self.adyacencia)

    def aristas(self):
        """Lista de (origen, destino, peso). En un no dirigido cada
        arista aparece una sola vez."""
        resultado = []
        vistas = set()
        for origen, vecinos in self.adyacencia.items():
            for destino, peso in vecinos:
                if not self.dirigido:
                    # A-B y B-A son la misma arista.
                    clave = frozenset((origen, destino))
                    if clave in vistas:
                        continue
                    vistas.add(clave)
                resultado.append((origen, destino, peso))
        return resultado

    def imprimir(self):
        flecha = "->" if self.dirigido else "--"
        for origen, vecinos in self.adyacencia.items():
            texto = ", ".join(f"{destino}({peso})"
                              for destino, peso in vecinos)
            print(f"{origen} {flecha} {texto}")

    # ------------------------------------------------------------------
    # Dijkstra
    # ------------------------------------------------------------------

    def dijkstra(self, origen, mostrar_pasos=False):
        """Distancia mínima desde el origen a cada vértice.

        Usa una cola de prioridad (heapq) que siempre entrega el vértice
        no visitado más cercano. Ese vértice ya tiene su distancia
        definitiva; luego se "relajan" sus aristas: si pasar por él
        mejora la distancia de un vecino, se actualiza.

        Devuelve (distancia, anterior). 'anterior' sirve para
        reconstruir los caminos.
        """
        distancia = {vertice: INFINITO for vertice in self.vertices()}
        anterior = {vertice: None for vertice in self.vertices()}
        distancia[origen] = 0
        visitados = set()
        cola = [(0, origen)]

        while cola:
            distancia_actual, actual = heapq.heappop(cola)  # el más cercano
            if actual in visitados:
                continue  # entrada vieja de la cola
            visitados.add(actual)

            for vecino, peso in self.adyacencia[actual]:
                nueva_distancia = distancia_actual + peso
                # Relajar: si por aquí es más corto, se actualiza.
                if nueva_distancia < distancia[vecino]:
                    distancia[vecino] = nueva_distancia
                    anterior[vecino] = actual
                    heapq.heappush(cola, (nueva_distancia, vecino))

            if mostrar_pasos:
                tabla = "  ".join(f"{v}={_texto(d)}"
                                  for v, d in distancia.items())
                print(f"   visita {actual}: {tabla}")
        return distancia, anterior

    def camino_dijkstra(self, origen, destino):
        """Devuelve (camino, costo). Camino vacío si no se llega."""
        distancia, anterior = self.dijkstra(origen)
        if distancia[destino] == INFINITO:
            return [], INFINITO
        camino = []
        actual = destino
        # Se sube por 'anterior' desde el destino hasta el origen.
        while actual is not None:
            camino.append(actual)
            actual = anterior[actual]
        return camino[::-1], distancia[destino]

    # ------------------------------------------------------------------
    # Floyd-Warshall y Warshall
    # ------------------------------------------------------------------

    def matriz_pesos(self):
        """Matriz inicial D0: 0 en la diagonal, el peso si hay arista
        directa e INFINITO si no hay."""
        vertices = self.vertices()
        matriz = {i: {j: (0 if i == j else INFINITO) for j in vertices}
                  for i in vertices}
        for origen, destino, peso in self.aristas():
            matriz[origen][destino] = min(matriz[origen][destino], peso)
            if not self.dirigido:
                matriz[destino][origen] = matriz[origen][destino]
        return matriz

    def floyd_warshall(self, mostrar_pasos=False):
        """Distancia mínima entre todos los pares de vértices.

        Para cada vértice intermedio k se pregunta: ¿ir de i a j
        pasando por k es más corto que lo que ya tengo?
            D[i][j] = min(D[i][j], D[i][k] + D[k][j])

        Devuelve (distancia, siguiente). siguiente[i][j] es el primer
        paso del camino de i a j.
        """
        vertices = self.vertices()
        distancia = self.matriz_pesos()
        # Primer paso de i a j (al inicio, la arista directa).
        siguiente = {i: {j: (j if distancia[i][j] < INFINITO else None)
                         for j in vertices} for i in vertices}
        if mostrar_pasos:
            imprimir_matriz(distancia, "D0")

        # k = vértice intermedio que se prueba.
        for numero, k in enumerate(vertices, start=1):
            for i in vertices:
                for j in vertices:
                    por_k = distancia[i][k] + distancia[k][j]  # i -> k -> j
                    if por_k < distancia[i][j]:
                        distancia[i][j] = por_k
                        siguiente[i][j] = siguiente[i][k]
            if mostrar_pasos:
                imprimir_matriz(distancia, f"D{numero} (pasando por {k})")
        return distancia, siguiente

    def camino_floyd(self, siguiente, origen, destino):
        """Arma el camino usando la tabla 'siguiente'."""
        if siguiente[origen][destino] is None:
            return []
        camino = [origen]
        while origen != destino:
            origen = siguiente[origen][destino]
            camino.append(origen)
        return camino

    def warshall(self):
        """Cierre transitivo: alcanzable[i][j] es True si existe algún
        camino de i a j. Es Floyd-Warshall con True/False:
            A[i][j] = A[i][j] or (A[i][k] and A[k][j])
        """
        vertices = self.vertices()
        alcanzable = {i: {j: False for j in vertices} for i in vertices}
        for origen, destino, _ in self.aristas():
            alcanzable[origen][destino] = True
            if not self.dirigido:
                alcanzable[destino][origen] = True

        for k in vertices:
            for i in vertices:
                for j in vertices:
                    # Si i llega a k y k llega a j, i llega a j.
                    if alcanzable[i][k] and alcanzable[k][j]:
                        alcanzable[i][j] = True
        return alcanzable

    # ------------------------------------------------------------------
    # Árbol de expansión mínima (solo grafos no dirigidos)
    # ------------------------------------------------------------------

    def prim(self, inicio, mostrar_pasos=False):
        """Prim: el árbol crece desde 'inicio'. En cada paso agrega la
        arista más barata que sale del árbol hacia un vértice nuevo.
        Devuelve la lista de aristas (origen, destino, peso)."""
        en_arbol = {inicio}
        arbol = []
        cola = [(peso, inicio, vecino)
                for vecino, peso in self.adyacencia[inicio]]
        heapq.heapify(cola)

        while cola and len(en_arbol) < len(self.adyacencia):
            peso, origen, destino = heapq.heappop(cola)  # la más barata
            if destino in en_arbol:
                if mostrar_pasos:
                    print(f"   descarta {origen}-{destino} ({peso}): "
                          f"formaría ciclo")
                continue
            en_arbol.add(destino)
            arbol.append((origen, destino, peso))
            if mostrar_pasos:
                print(f"   agrega {origen}-{destino} ({peso})")
            for vecino, peso_vecino in self.adyacencia[destino]:
                if vecino not in en_arbol:
                    heapq.heappush(cola, (peso_vecino, destino, vecino))
        return arbol

    def kruskal(self, mostrar_pasos=False):
        """Kruskal: ordena todas las aristas de menor a mayor peso y las
        agrega si no forman ciclo (lo revisa Union-Find)."""
        grupos = UnionFind(self.vertices())
        arbol = []
        for origen, destino, peso in sorted(self.aristas(),
                                            key=lambda arista: arista[2]):
            if grupos.unir(origen, destino):  # True si no hace ciclo
                arbol.append((origen, destino, peso))
                if mostrar_pasos:
                    print(f"   agrega {origen}-{destino} ({peso})")
            elif mostrar_pasos:
                print(f"   descarta {origen}-{destino} ({peso}): "
                      f"formaría ciclo")
            # Un árbol de V vértices tiene V - 1 aristas.
            if len(arbol) == len(self.adyacencia) - 1:
                break
        return arbol


# ----------------------------------------------------------------------
# Funciones de apoyo para mostrar resultados
# ----------------------------------------------------------------------

def _texto(valor):
    """INFINITO se muestra como 'inf'."""
    return "inf" if valor == INFINITO else str(valor)


def imprimir_matriz(matriz, titulo=""):
    """Muestra una matriz guardada como diccionario de diccionarios."""
    if titulo:
        print(f"{titulo}:")
    vertices = list(matriz)
    ancho = max(4, max(len(str(v)) for v in vertices) + 1)
    print(" " * ancho + "".join(f"{str(v):>{ancho}}" for v in vertices))
    for i in vertices:
        fila = "".join(f"{_texto(matriz[i][j]):>{ancho}}" for j in vertices)
        print(f"{str(i):<{ancho}}" + fila)


def peso_total(arbol):
    return sum(peso for _, _, peso in arbol)


# ----------------------------------------------------------------------
# Demostración
# ----------------------------------------------------------------------

if __name__ == "__main__":
    print("=== Grafo dirigido con pesos ===")
    grafo = GrafoPesado(dirigido=True)
    for origen, destino, peso in [("A", "B", 4), ("A", "C", 2),
                                  ("C", "B", 1), ("B", "D", 5),
                                  ("C", "D", 8), ("D", "E", 3)]:
        grafo.agregar_arista(origen, destino, peso)
    grafo.imprimir()

    print("\nDijkstra desde A:")
    distancia, _ = grafo.dijkstra("A", mostrar_pasos=True)
    for destino in grafo.vertices():
        camino, costo = grafo.camino_dijkstra("A", destino)
        print(f"   A -> {destino}: costo {_texto(costo)}, camino {camino}")

    print("\nFloyd-Warshall:")
    distancia, siguiente = grafo.floyd_warshall()
    imprimir_matriz(distancia)
    print("Camino A -> E:", grafo.camino_floyd(siguiente, "A", "E"))

    print("\nWarshall (1 = hay camino):")
    alcanzable = grafo.warshall()
    imprimir_matriz({i: {j: int(alcanzable[i][j]) for j in alcanzable[i]}
                     for i in alcanzable})

    print("\n=== Grafo no dirigido: árbol de expansión mínima ===")
    red = GrafoPesado()
    for origen, destino, peso in [("A", "B", 2), ("A", "C", 3),
                                  ("B", "C", 1), ("B", "D", 4),
                                  ("C", "D", 5), ("D", "E", 6)]:
        red.agregar_arista(origen, destino, peso)
    print("Prim desde A:")
    arbol_prim = red.prim("A", mostrar_pasos=True)
    print("   Peso total:", peso_total(arbol_prim))
    print("Kruskal:")
    arbol_kruskal = red.kruskal(mostrar_pasos=True)
    print("   Peso total:", peso_total(arbol_kruskal))
