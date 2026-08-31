# Main.py

from ArbolBinario import ArbolBinario


def main():
    valores = [50, 30, 70, 20, 40, 60, 80]
    
    arbol = ArbolBinario()
    print(f"Insertando: {valores}")
    
    for valor in valores:
        arbol.insertar(valor)
    
    print("\nÁrbol (leer de abajo hacia arriba):")
    arbol.imprimir()
    
    print(f"\nCantidad de nodos: {len(arbol)}")
    print(f"¿Está vacío? {arbol.esta_vacio()}")


if __name__ == "__main__":
    main()