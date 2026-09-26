# ================================================================
# ArbolAVL.py
# Árbol AVL con INSERTAR, ELIMINAR y BALANCEAR
# ================================================================

from __future__ import annotations
from typing import Optional, List


class NodoAVL:
    """Nodo de un Árbol AVL."""

    def __init__(self, valor: int) -> None:
        self.valor: int = valor
        self.izquierdo: Optional[NodoAVL] = None
        self.derecho: Optional[NodoAVL] = None
        self.altura: int = 1  # hoja = 1

    def factor_equilibrio(self) -> int:
        """FE = altura(izq) - altura(der)."""
        alt_izq = self.izquierdo.altura if self.izquierdo else 0
        alt_der = self.derecho.altura if self.derecho else 0
        return alt_izq - alt_der

    def __repr__(self) -> str:
        return f"NodoAVL(valor={self.valor}, altura={self.altura})"


class ArbolAVL:
    """Árbol AVL con insertar, eliminar y balancear."""

    def __init__(self) -> None:
        self.raiz: Optional[NodoAVL] = None

    # ============================================================
    # UTILIDADES INTERNAS
    # ============================================================
    def _altura(self, nodo: Optional[NodoAVL]) -> int:
        return nodo.altura if nodo else 0

    def _actualizar_altura(self, nodo: NodoAVL) -> None:
        """Actualiza la altura del nodo según sus hijos."""
        nodo.altura = 1 + max(self._altura(nodo.izquierdo), self._altura(nodo.derecho))

    def _min_nodo(self, nodo: NodoAVL) -> NodoAVL:
        """Retorna el nodo con el valor mínimo del subárbol."""
        actual = nodo
        while actual.izquierdo:
            actual = actual.izquierdo
        return actual

    # ============================================================
    # ROTACIONES (para balancear)
    # ============================================================
    def _rotar_derecha(self, y: NodoAVL) -> NodoAVL:
        """
        Rotación a la derecha (caso LL).
              y                      x
             / \                    / \
            x   T3   ->            T1  y
           / \                        / \
          T1  T2                     T2  T3
        """
        x = y.izquierdo
        assert x is not None
        T2 = x.derecho

        x.derecho = y
        y.izquierdo = T2

        self._actualizar_altura(y)
        self._actualizar_altura(x)
        return x

    def _rotar_izquierda(self, x: NodoAVL) -> NodoAVL:
        """
        Rotación a la izquierda (caso RR).
            x                         y
           / \                       / \
          T1  y        ->           x  T3
             / \                   / \
            T2 T3                 T1 T2
        """
        y = x.derecho
        assert y is not None
        T2 = y.izquierdo

        y.izquierdo = x
        x.derecho = T2

        self._actualizar_altura(x)
        self._actualizar_altura(y)
        return y

    # ============================================================
    # BALANCEAR 
    # ============================================================
    def _balancear(self, nodo: NodoAVL) -> NodoAVL:
        """
        Balancea un nodo aplicando la rotación necesaria.
        Este es el método principal que pide el profesor.

        Casos:
            LL: FE > 1 y FE(izq) >= 0  → rotar derecha
            LR: FE > 1 y FE(izq) < 0   → rotar izquierda(izq) + derecha
            RR: FE < -1 y FE(der) <= 0 → rotar izquierda
            RL: FE < -1 y FE(der) > 0  → rotar derecha(der) + izquierda
        """
        fe = nodo.factor_equilibrio()

        # CASO LL: rotación a la derecha
        if fe > 1 and nodo.izquierdo and nodo.izquierdo.factor_equilibrio() >= 0:
            return self._rotar_derecha(nodo)

        # CASO LR: rotación doble (izquierda + derecha)
        if fe > 1 and nodo.izquierdo and nodo.izquierdo.factor_equilibrio() < 0:
            nodo.izquierdo = self._rotar_izquierda(nodo.izquierdo)
            return self._rotar_derecha(nodo)

        # CASO RR: rotación a la izquierda
        if fe < -1 and nodo.derecho and nodo.derecho.factor_equilibrio() <= 0:
            return self._rotar_izquierda(nodo)

        # CASO RL: rotación doble (derecha + izquierda)
        if fe < -1 and nodo.derecho and nodo.derecho.factor_equilibrio() > 0:
            nodo.derecho = self._rotar_derecha(nodo.derecho)
            return self._rotar_izquierda(nodo)

        # Ya está balanceado
        return nodo

    # ============================================================
    # INSERTAR (con balanceo)
    # ============================================================
    def insertar(self, valor: int) -> None:
        """Inserta un valor y rebalancea el camino a la raíz."""
        self.raiz = self._insertar(self.raiz, valor)

    def _insertar(self, nodo: Optional[NodoAVL], valor: int) -> NodoAVL:
        if nodo is None:
            return NodoAVL(valor)

        if valor < nodo.valor:
            nodo.izquierdo = self._insertar(nodo.izquierdo, valor)
        else:
            nodo.derecho = self._insertar(nodo.derecho, valor)

        # Actualizar altura y balancear
        self._actualizar_altura(nodo)
        return self._balancear(nodo)  # ← Aquí se usa el balanceo

    # ============================================================
    # ELIMINAR (con balanceo) 
    # ============================================================
    def eliminar(self, valor: int) -> None:
        """
        ELIMINA un valor del árbol y lo rebalancea.
        Este es el método principal que pide el profesor.
        
        Pasos:
        1. Buscar el nodo a eliminar (como en ABB)
        2. Aplicar los 3 casos de eliminación
        3. Actualizar alturas
        4. Balancear el árbol
        """
        self.raiz = self._eliminar(self.raiz, valor)

    def _eliminar(self, nodo: Optional[NodoAVL], valor: int) -> Optional[NodoAVL]:
        """
        ELIMINACIÓN RECURSIVA con balanceo.
        Este es el método que pide el profesor.
        """
        if nodo is None:
            return None

        # ---- 1. BÚSQUEDA DEL NODO A ELIMINAR (como en ABB) ----
        if valor < nodo.valor:
            nodo.izquierdo = self._eliminar(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            nodo.derecho = self._eliminar(nodo.derecho, valor)
        else:
            # ---- 2. NODO ENCONTRADO: APLICAR CASOS ----

            # CASO 1: Nodo es HOJA (sin hijos)
            if nodo.izquierdo is None and nodo.derecho is None:
                return None

            # CASO 2a: Solo tiene hijo DERECHO
            if nodo.izquierdo is None:
                return nodo.derecho

            # CASO 2b: Solo tiene hijo IZQUIERDO
            if nodo.derecho is None:
                return nodo.izquierdo

            # CASO 3: Tiene DOS HIJOS
            # Buscar el SUCESOR INORDEN (mínimo del subárbol derecho)
            sucesor = self._min_nodo(nodo.derecho)
            nodo.valor = sucesor.valor  # Copiar valor del sucesor
            # Eliminar el sucesor (que ahora es hoja o tiene 1 hijo)
            nodo.derecho = self._eliminar(nodo.derecho, sucesor.valor)

        # ---- 3. ACTUALIZAR ALTURA Y BALANCEAR ----
        self._actualizar_altura(nodo)           # ← Actualizar altura
        return self._balancear(nodo)            # ← BALANCEAR (el método clave)

    # ============================================================
    # BÚSQUEDA (como en ABB normal)
    # ============================================================
    def buscar(self, valor: int) -> bool:
        """Busca un valor en el árbol."""
        n = self.raiz
        while n:
            if valor == n.valor:
                return True
            n = n.izquierdo if valor < n.valor else n.derecho
        return False

    def altura(self) -> int:
        """Retorna la altura del árbol."""
        return self.raiz.altura if self.raiz else 0

    # ============================================================
    # RECORRIDOS
    # ============================================================
    def inorden(self) -> List[int]:
        res: List[int] = []
        def _in(n: Optional[NodoAVL]) -> None:
            if n:
                _in(n.izquierdo)
                res.append(n.valor)
                _in(n.derecho)
        _in(self.raiz)
        return res

    def preorden(self) -> List[int]:
        res: List[int] = []
        def _pre(n: Optional[NodoAVL]) -> None:
            if n:
                res.append(n.valor)
                _pre(n.izquierdo)
                _pre(n.derecho)
        _pre(self.raiz)
        return res

    def postorden(self) -> List[int]:
        res: List[int] = []
        def _post(n: Optional[NodoAVL]) -> None:
            if n:
                _post(n.izquierdo)
                _post(n.derecho)
                res.append(n.valor)
        _post(self.raiz)
        return res

    # ============================================================
    # VISUALIZACIÓN EN CONSOLA
    # ============================================================
    def imprimir(self) -> None:
        """Imprime el árbol en consola (horizontal)."""
        self._imprimir_rec(self.raiz, 0)

    def _imprimir_rec(self, nodo: Optional[NodoAVL], nivel: int) -> None:
        if nodo:
            self._imprimir_rec(nodo.derecho, nivel + 1)
            fe = nodo.factor_equilibrio()
            print("    " * nivel + f"[{nodo.valor} h={nodo.altura} FE={fe}]")
            self._imprimir_rec(nodo.izquierdo, nivel + 1)


# ============================================================
# PRUEBA COMPLETA
# ============================================================
if __name__ == "__main__":
   
    # Crear un nuevo árbol para el ejemplo
    avl_balanceo = ArbolAVL()

    # Insertar valores que causan desbalance
    valores_balanceo = [30, 20, 40, 10, 25, 22]
    print(f"\n📥 Insertando: {valores_balanceo}")
    print("(La inserción de 22 causará un desbalance LR)\n")

    for v in valores_balanceo:
        print(f"\n--- Insertando {v} ---")
        avl_balanceo.insertar(v)
        avl_balanceo.imprimir()
        print(f"Altura del árbol: {avl_balanceo.altura()}")
        print(f"Inorden: {avl_balanceo.inorden()}")

    print("\n" + "=" * 60)
    print("✅ El árbol se mantiene balanceado automáticamente")
    print("   La altura es O(log n) gracias a las rotaciones")
    print("=" * 60)


    avl = ArbolAVL()

    # Insertar valores
    for v in [50, 30, 70, 20, 40, 60, 80]:
        avl.insertar(v)

    print("Árbol inicial:")
    avl.imprimir()
    print(f"Inorden: {avl.inorden()}\n")

    # Eliminar un valor
    avl.eliminar(30)
    print("Después de eliminar 30:")
    avl.imprimir()
    print(f"Inorden: {avl.inorden()}\n")

    # Eliminar otro valor
    avl.eliminar(50)
    print("Después de eliminar 50:")
    avl.imprimir()
    print(f"Inorden: {avl.inorden()}")