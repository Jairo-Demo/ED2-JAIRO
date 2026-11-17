"""Vista de consola del Árbol M-Vías: solo muestra y lee datos."""


class VistaConsola:
    """Imprime el menú y los mensajes, y lee lo que escribe el usuario."""

    def mostrar_menu(self):
        print("\n" + "=" * 35)
        print("ÁRBOL M-VÍAS (MVC)")
        print("=" * 35)
        print("1. Insertar una clave")
        print("2. Insertar varias claves (ej: 10 20 30)")
        print("3. Buscar una clave")
        print("4. Mostrar recorrido en orden")
        print("5. Mostrar el árbol por niveles")
        print("6. Salir")

    def pedir_opcion(self):
        return input("Elige una opción: ").strip()

    def pedir_clave(self):
        """Pide un número hasta que el usuario escriba uno válido."""
        while True:
            try:
                return int(input("Clave (número): "))
            except ValueError:
                self.mostrar_error("Ingresa un número válido.")

    def pedir_varias_claves(self):
        """Lee números separados por espacios; ignora lo que no lo sea."""
        texto = input("Claves separadas por espacio: ")
        return [int(parte) for parte in texto.split() if parte.isdigit()]

    def pedir_orden(self):
        """Pide el orden del árbol (2 o más)."""
        while True:
            try:
                orden = int(input("Orden del árbol (ej. 3, 4, 5): "))
            except ValueError:
                self.mostrar_error("Ingresa un número entero.")
                continue
            if orden >= 2:
                return orden
            self.mostrar_error("El orden debe ser al menos 2.")

    def mostrar_mensaje(self, mensaje):
        print(f"\n[INFO] {mensaje}")

    def mostrar_error(self, mensaje):
        print(f"\n[ERROR] {mensaje}")

    def mostrar_arbol(self, lineas):
        print("\n--- ÁRBOL POR NIVELES ---")
        for linea in lineas:
            print(linea)
