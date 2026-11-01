class NodoMVias:
    """
    Clase que representa un Nodo de un árbol M-Vías.
    (Separado en su propia clase según requerimiento)
    """
    def __init__(self, orden: int):
        self._orden = orden          
        self._claves = []            
        self._hijos = []             
    
    # ==========================================
    # MÉTODOS GETTER Y SETTER (Requerimiento 1)
    # ==========================================
    def get_orden(self) -> int:
        return self._orden
        
    def set_orden(self, orden: int) -> None:
        self._orden = orden
        
    def get_claves(self) -> list:
        return self._claves
        
    def set_claves(self, claves: list) -> None:
        self._claves = claves
        
    def get_hijos(self) -> list:
        return self._hijos
        
    def set_hijos(self, hijos: list) -> None:
        self._hijos = hijos
        
    # ==========================================
    # MÉTODOS AUXILIARES
    # ==========================================
    def es_hoja(self) -> bool:
        """Retorna True si el nodo no tiene hijos reales."""
        return all(h is None for h in self.get_hijos()) or len(self.get_hijos()) == 0
    
    def esta_lleno(self) -> bool:
        """Retorna True si el nodo tiene m-1 claves (máximo permitido)."""
        return len(self.get_claves()) >= self.get_orden() - 1
    
    def __repr__(self) -> str:
        return f"NodoMVias(claves={self.get_claves()})"
