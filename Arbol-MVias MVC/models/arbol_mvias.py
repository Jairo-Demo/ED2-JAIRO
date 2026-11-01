try:
    from .nodo_mvias import NodoMVias
except (ImportError, ValueError):
    from nodo_mvias import NodoMVias


class ArbolMVias:
    """
    Clase que representa el Árbol M-Vías (Separado en su propia clase).
    Contiene la implementación de los métodos vistos en Árboles Binarios (Requerimiento 2).
    """
    def __init__(self, orden: int):
        if orden < 2:
            raise ValueError("El orden debe ser al menos 2")
        self.orden = orden
        self.raiz = None
    
    def esta_vacio(self) -> bool:
        return self.raiz is None
    
    # ------------------------------------------------------------------
    # 1. BÚSQUEDA
    # ------------------------------------------------------------------
    def buscar(self, clave) -> bool:
        return self._buscar_rec(self.raiz, clave)
    
    def _buscar_rec(self, nodo: NodoMVias, clave) -> bool:
        if nodo is None:
            return False
        
        claves = nodo.get_claves()
        hijos = nodo.get_hijos()
        
        for i, k in enumerate(claves):
            if clave == k:
                return True
            if clave < k:
                if i < len(hijos):
                    return self._buscar_rec(hijos[i], clave)
                return False
        
        if len(hijos) > len(claves):
            return self._buscar_rec(hijos[-1], clave)
        return False
    
    # ------------------------------------------------------------------
    # 2. INSERCIÓN
    # ------------------------------------------------------------------
    def insertar(self, clave) -> None:
        if self.raiz is None:
            self.raiz = NodoMVias(self.orden)
            self.raiz.get_claves().append(clave)
            return
        self._insertar_rec(self.raiz, clave)
    
    def _insertar_rec(self, nodo: NodoMVias, clave) -> None:
        claves = nodo.get_claves()
        hijos = nodo.get_hijos()
        
        # Si el nodo no está lleno, lo insertamos aquí
        if not nodo.esta_lleno():
            self._insertar_ordenado(claves, clave)
            return
        
        # Si está lleno, bajamos por el hijo correspondiente
        i = 0
        while i < len(claves) and clave > claves[i]:
            i += 1

        while len(hijos) < len(claves) + 1:
            hijos.append(None)
        
        if i < len(hijos) and hijos[i] is not None:
            self._insertar_rec(hijos[i], clave)
        else:
            nuevo = NodoMVias(self.orden)
            nuevo.get_claves().append(clave)
            while len(hijos) <= i:
                hijos.append(None)
            hijos[i] = nuevo
    
    def _insertar_ordenado(self, lista: list, valor) -> None:
        i = 0
        while i < len(lista) and valor > lista[i]:
            i += 1
        lista.insert(i, valor)

    # ------------------------------------------------------------------
    # 3. RECORRIDOS (Todos los de ABB)
    # ------------------------------------------------------------------
    def en_orden(self) -> list:
        resultado = []
        self._en_orden_rec(self.raiz, resultado)
        return resultado
    
    def _en_orden_rec(self, nodo: NodoMVias, resultado: list) -> None:
        if nodo is None:
            return
        claves = nodo.get_claves()
        hijos = nodo.get_hijos()
        
        for i in range(len(claves)):
            if i < len(hijos):
                self._en_orden_rec(hijos[i], resultado)
            resultado.append(claves[i])
            
        if len(hijos) > len(claves):
            self._en_orden_rec(hijos[len(claves)], resultado)

    def pre_orden(self) -> list:
        resultado = []
        self._pre_orden_rec(self.raiz, resultado)
        return resultado
        
    def _pre_orden_rec(self, nodo: NodoMVias, resultado: list) -> None:
        if nodo is None:
            return
        claves = nodo.get_claves()
        hijos = nodo.get_hijos()
        
        # En pre-orden, primero visitamos todas las claves del nodo
        for k in claves:
            resultado.append(k)
        # Luego visitamos todos los hijos
        for hijo in hijos:
            if hijo is not None:
                self._pre_orden_rec(hijo, resultado)

    def post_orden(self) -> list:
        resultado = []
        self._post_orden_rec(self.raiz, resultado)
        return resultado

    def _post_orden_rec(self, nodo: NodoMVias, resultado: list) -> None:
        if nodo is None:
            return
        claves = nodo.get_claves()
        hijos = nodo.get_hijos()
        
        # En post-orden, primero visitamos todos los hijos
        for hijo in hijos:
            if hijo is not None:
                self._post_orden_rec(hijo, resultado)
        # Luego visitamos todas las claves del nodo
        for k in claves:
            resultado.append(k)

    def por_niveles(self) -> list:
        if self.esta_vacio():
            return []
        
        from collections import deque
        cola = deque([self.raiz])
        resultado = []
        
        while cola:
            nodo = cola.popleft()
            for k in nodo.get_claves():
                resultado.append(k)
            for hijo in nodo.get_hijos():
                if hijo is not None:
                    cola.append(hijo)
        return resultado

    # ------------------------------------------------------------------
    # 4. ALTURA, MÍNIMO Y MÁXIMO (Métodos de ABB)
    # ------------------------------------------------------------------
    def altura(self) -> int:
        return self._altura_rec(self.raiz)
        
    def _altura_rec(self, nodo: NodoMVias) -> int:
        if nodo is None:
            return 0 # o -1 dependiendo de la convención de la clase
        
        hijos = nodo.get_hijos()
        if not hijos or all(h is None for h in hijos):
            return 1 # o 0
            
        alturas_hijos = []
        for hijo in hijos:
            if hijo is not None:
                alturas_hijos.append(self._altura_rec(hijo))
                
        return 1 + max(alturas_hijos)

    def minimo(self):
        if self.esta_vacio():
            return None
        nodo = self.raiz
        while nodo.get_hijos() and nodo.get_hijos()[0] is not None:
            nodo = nodo.get_hijos()[0]
        return nodo.get_claves()[0]

    def maximo(self):
        if self.esta_vacio():
            return None
        nodo = self.raiz
        while nodo.get_hijos() and nodo.get_hijos()[-1] is not None:
            nodo = nodo.get_hijos()[-1]
        return nodo.get_claves()[-1]

    # --- Estructura para la vista (Mantiene el MVC) ---
    def obtener_niveles_texto(self) -> list:
        if self.esta_vacio():
            return ["(árbol vacío)"]
        
        from collections import deque
        cola = deque([(self.raiz, 0)])
        nivel_actual = 0
        linea = []
        resultado = []
        
        while cola:
            nodo, nivel = cola.popleft()
            if nivel != nivel_actual:
                resultado.append(f"Nivel {nivel_actual}: " + "  |  ".join(str(c) for c in linea))
                linea = []
                nivel_actual = nivel
            
            linea.append(nodo.get_claves())
            for hijo in nodo.get_hijos():
                if hijo is not None:
                    cola.append((hijo, nivel + 1))
        
        if linea:
            resultado.append(f"Nivel {nivel_actual}: " + "  |  ".join(str(c) for c in linea))
        return resultado
