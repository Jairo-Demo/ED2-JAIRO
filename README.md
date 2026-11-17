# Estructuras de Datos II - Árboles

Este proyecto contiene las implementaciones en arquitectura **MVC (Modelo - Vista - Controlador)** independientes para **Árbol Binario de Búsqueda** y **Árbol M-Vías de Búsqueda**, además del **Árbol AVL**, el **Árbol-B** y los **Grafos** de las unidades 4 y 5 (solo código, sin página web).

El Árbol Binario y el M-Vías tienen su propia aplicación web dentro de su carpeta.

---

## Estructura del Proyecto

```text
ED2-JAIRO/
│
├── unidad1/                        <-- Unidad I: Árboles Binarios
│   ├── Arbol-AVL/
│   │   └── ArbolAVL.py
│   └── Arbol-Binario MVC/          <-- Aplicación Web MVC: Árbol Binario
│       ├── models/
│       │   └── modelo.py
│       ├── templates/
│       │   └── index.html
│       ├── static/
│       │   └── style.css
│       └── app.py                  (Servidor Web en puerto 5000)
│
├── unidad2/                        <-- Unidad II: Árboles M-Vías
│   └── Arbol-MVias MVC/            <-- Aplicación Web MVC: Árbol M-Vías
│       ├── models/
│       │   ├── nodo_mvias.py
│       │   └── arbol_mvias.py
│       ├── controllers/
│       │   └── controlador.py      (Consola)
│       ├── views/
│       │   └── vista.py            (Consola)
│       ├── templates/
│       │   └── index.html
│       ├── static/
│       │   └── style.css
│       ├── app.py                  (Servidor Web en puerto 5001)
│       └── main.py                 (Lanzador de consola)
│
├── unidad3/                        <-- Unidad III: Árboles-B
│   └── Arbol-B/
│       └── ArbolB.py               (Árbol-B: insertar, buscar, eliminar)
│
├── unidad4/                        <-- Unidad IV: Grafos
│   └── Grafos/
│       └── Grafo.py                (BFS, DFS, ciclos, orden topológico)
│
└── unidad5/                        <-- Unidad V: Grafos Pesados
    └── Grafos-Pesados/
        └── GrafoPesado.py          (Dijkstra, Floyd-Warshall, Warshall, Prim, Kruskal)
```

---

## Cómo ejecutar cada Árbol

### 1. Ejecutar la Web del Árbol Binario
Abre una terminal y entra en la carpeta del Árbol Binario:
```bash
cd "unidad1/Arbol-Binario MVC"
python app.py
```
Abre en tu navegador: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

### 2. Ejecutar la Web del Árbol M-Vías
Abre otra terminal y entra en la carpeta del Árbol M-Vías:
```bash
cd "unidad2/Arbol-MVias MVC"
python app.py
```
Abre en tu navegador: [http://127.0.0.1:5001/](http://127.0.0.1:5001/)

Nota: como usan puertos distintos (5000 y 5001), se pueden tener las dos páginas abiertas al mismo tiempo.

---

### 3. Ejecutar el Árbol-B (consola)
```bash
cd unidad3/Arbol-B
python ArbolB.py
```

---

### 4. Ejecutar los Grafos (consola)
```bash
cd unidad4/Grafos
python Grafo.py
```

### 5. Ejecutar los Grafos Pesados (consola)
```bash
cd unidad5/Grafos-Pesados
python GrafoPesado.py
```
