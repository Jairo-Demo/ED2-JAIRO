class VistaConsola:
    """
    La VISTA: Se encarga exclusivamente de mostrar información al usuario
    y de capturar sus entradas (input). No tiene lógica de negocio.
    """
    
    def mostrar_menu(self):
        print("\n" + "="*35)
        print("    ÁRBOL M-VÍAS (Patrón MVC)    ")
        print("="*35)
        print("1. Insertar una clave")
        print("2. Insertar varias claves (ej: 10 20 30)")
        print("3. Buscar una clave")
        print("4. Mostrar recorrido En-Orden")
        print("5. Imprimir estructura del árbol")
        print("6. Salir")
        
    def pedir_opcion(self) -> str:
        return input("Elige una opción: ")
        
    def pedir_clave(self) -> int:
        while True:
            try:
                valor = input("Ingresa la clave (número): ")
                return int(valor)
            except ValueError:
                self.mostrar_error("Por favor, ingresa un número válido.")
                
    def pedir_multiples_claves(self) -> list:
        valores_str = input("Ingresa las claves separadas por espacio: ")
        claves = []
        for v in valores_str.split():
            if v.isdigit():
                claves.append(int(v))
        return claves

    def pedir_orden(self) -> int:
        while True:
            try:
                valor = input("¿De qué orden (m) será tu Árbol M-Vías? (ej. 3, 4, 5): ")
                orden = int(valor)
                if orden >= 2:
                    return orden
                else:
                    self.mostrar_error("El orden debe ser al menos 2.")
            except ValueError:
                self.mostrar_error("Por favor, ingresa un número entero válido.")

    def mostrar_mensaje(self, mensaje: str):
        print(f"\n[INFO] {mensaje}")
        
    def mostrar_error(self, mensaje: str):
        print(f"\n[ERROR] {mensaje}")
        
    def mostrar_arbol(self, niveles: list):
        print("\n--- ESTRUCTURA DEL ÁRBOL ---")
        for linea in niveles:
            print(linea)
        print("----------------------------")
