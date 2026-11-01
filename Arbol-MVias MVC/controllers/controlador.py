try:
    from models.arbol_mvias import ArbolMVias
    from views.vista import VistaConsola
except (ImportError, ValueError):
    from arbol_mvias import ArbolMVias
    from vista import VistaConsola

class Controlador:
    """
    EL CONTROLADOR: Hace de intermediario entre la Vista y el Modelo.
    Recibe la entrada de la vista, actualiza el modelo, y le pide a la vista 
    que muestre los resultados.
    """
    def __init__(self):
        self.vista = VistaConsola()
        self.arbol = None
        
    def iniciar(self):
        # 1. Configurar el modelo al arrancar
        self.vista.mostrar_mensaje("Bienvenido. Primero debemos inicializar el árbol.")
        orden = self.vista.pedir_orden()
        self.arbol = ArbolMVias(orden)
        self.vista.mostrar_mensaje(f"Árbol M-Vías de orden {orden} creado con éxito.")
        
        # 2. Bucle principal de la aplicación
        corriendo = True
        while corriendo:
            self.vista.mostrar_menu()
            opcion = self.vista.pedir_opcion()
            
            if opcion == "1":
                self._opcion_insertar()
            elif opcion == "2":
                self._opcion_insertar_varios()
            elif opcion == "3":
                self._opcion_buscar()
            elif opcion == "4":
                self._opcion_recorrido()
            elif opcion == "5":
                self._opcion_imprimir()
            elif opcion == "6":
                self.vista.mostrar_mensaje("¡Hasta luego!")
                corriendo = False
            else:
                self.vista.mostrar_error("Opción inválida. Intenta de nuevo.")

    def _opcion_insertar(self):
        clave = self.vista.pedir_clave()
        self.arbol.insertar(clave)
        self.vista.mostrar_mensaje(f"Clave {clave} insertada.")

    def _opcion_insertar_varios(self):
        claves = self.vista.pedir_multiples_claves()
        if not claves:
            self.vista.mostrar_error("No se ingresaron claves válidas.")
            return
            
        for clave in claves:
            self.arbol.insertar(clave)
        self.vista.mostrar_mensaje(f"Se insertaron {len(claves)} claves.")

    def _opcion_buscar(self):
        if self.arbol.esta_vacio():
            self.vista.mostrar_error("El árbol está vacío.")
            return
            
        clave = self.vista.pedir_clave()
        encontrado = self.arbol.buscar(clave)
        if encontrado:
            self.vista.mostrar_mensaje(f"¡La clave {clave} SÍ existe en el árbol!")
        else:
            self.vista.mostrar_mensaje(f"La clave {clave} NO fue encontrada.")

    def _opcion_recorrido(self):
        if self.arbol.esta_vacio():
            self.vista.mostrar_error("El árbol está vacío.")
        else:
            elementos = self.arbol.en_orden()
            self.vista.mostrar_mensaje(f"Recorrido En-Orden: {elementos}")

    def _opcion_imprimir(self):
        niveles = self.arbol.obtener_niveles_texto()
        self.vista.mostrar_arbol(niveles)
