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

    print("\n--- Recorridos ---")
    print(f"InOrden   : {arbol.in_orden()}")
    print(f"PreOrden  : {arbol.pre_orden()}")
    print(f"PostOrden : {arbol.post_orden()}")


    print("=" * 40)
    print("ARBOL DE EXPRESIONES")
    print("Infija -> Postfija")
    print("=" * 40)
    print("Escribe 'salir' para terminar")
    print("-" * 40)

    while True:
        exp = input("Expresion infija: ")
        
        if exp == "salir":
            break
        
        arbol = ArbolBinario()
        arbol.construir_desde_infija(exp)
        
        print("Postfija:", arbol.obtener_postfija())
        print("Prefija:", arbol.obtener_prefija())
        print("")
        arbol.imprimir()
        print("-" * 30)


if __name__ == "__main__":
    main()