"""Controlador web (Flask) del Árbol M-Vías.

Recibe los formularios, llama a los métodos de ArbolMVias (el Modelo)
y vuelve a mostrar la página (la Vista).

Ejecutar desde esta carpeta:  python app.py
Abrir en el navegador:        http://127.0.0.1:5001/
"""

from flask import Flask, flash, redirect, render_template, request, url_for

from models.arbol_mvias import ArbolMVias

app = Flask(__name__)
# Necesaria para mostrar mensajes con flash().
app.secret_key = "clave-secreta-mvias"

# Árbol compartido mientras el servidor esté encendido (orden 3).
arbol = ArbolMVias(3)


def nodo_a_diccionario(nodo):
    """Convierte un NodoMVias y sus hijos en diccionarios para la
    plantilla. Si el nodo tiene hijos, se completan los lugares vacíos
    con None para dibujar cada hijo en su posición."""
    if nodo is None:
        return None
    hijos = nodo.get_hijos()
    tiene_hijos = any(hijo is not None for hijo in hijos)

    hijos_diccionario = []
    if tiene_hijos:
        total_hijos = max(len(hijos), len(nodo.get_claves()) + 1)
        for posicion in range(total_hijos):
            hijo = hijos[posicion] if posicion < len(hijos) else None
            hijos_diccionario.append(nodo_a_diccionario(hijo))

    return {
        "claves": list(nodo.get_claves()),
        "tiene_hijos": tiene_hijos,
        "hijos": hijos_diccionario,
    }


def leer_claves(texto):
    """Convierte '50' o '10, 20 30' en una lista de enteros.
    Lo que no sea número se ignora."""
    if not texto:
        return []
    partes = texto.replace(";", ",").replace(" ", ",").split(",")
    claves = []
    for parte in partes:
        parte = parte.strip()
        if parte:
            try:
                claves.append(int(parte))
            except ValueError:
                pass
    return claves


@app.route("/")
def index():
    """Muestra la página con el árbol y sus datos."""
    recorrido_en_orden = arbol.en_orden()
    datos_pagina = {
        "orden": arbol.orden,
        "raiz": nodo_a_diccionario(arbol.raiz),
        "vacio": arbol.esta_vacio(),
        "total_claves": len(recorrido_en_orden),
        "altura": arbol.altura(),
        "minimo": arbol.minimo(),
        "maximo": arbol.maximo(),
        "en_orden": recorrido_en_orden,
        "pre_orden": arbol.pre_orden(),
        "post_orden": arbol.post_orden(),
        "por_niveles": arbol.por_niveles(),
        "niveles_texto": arbol.obtener_niveles_texto(),
    }
    return render_template("index.html", **datos_pagina)


@app.route("/insertar", methods=["POST"])
def insertar():
    claves = leer_claves(request.form.get("valor", ""))
    if not claves:
        flash("Ingresa un número entero (o varios separados por comas).",
              "error")
    else:
        for clave in claves:
            arbol.insertar(clave)
        if len(claves) == 1:
            flash(f"Clave {claves[0]} insertada.", "ok")
        else:
            flash(f"{len(claves)} claves insertadas: {claves}", "ok")
    return redirect(url_for("index"))


@app.route("/buscar", methods=["POST"])
def buscar():
    claves = leer_claves(request.form.get("valor", ""))
    if not claves:
        flash("Ingresa un número entero para buscar.", "error")
    elif arbol.buscar(claves[0]):
        flash(f"La clave {claves[0]} SÍ existe en el árbol.", "ok")
    else:
        flash(f"La clave {claves[0]} NO existe en el árbol.", "error")
    return redirect(url_for("index"))


@app.route("/orden", methods=["POST"])
def cambiar_orden():
    """Crea un árbol vacío con el nuevo orden."""
    global arbol  # se asigna un objeto nuevo a la variable global
    try:
        nuevo_orden = int(request.form.get("orden", ""))
    except ValueError:
        flash("Orden inválido.", "error")
        return redirect(url_for("index"))

    if nuevo_orden < 2:
        flash("El orden debe ser al menos 2.", "error")
    else:
        arbol = ArbolMVias(nuevo_orden)
        flash(f"Árbol reiniciado con orden {nuevo_orden}.", "ok")
    return redirect(url_for("index"))


@app.route("/reiniciar", methods=["POST"])
def reiniciar():
    """Vacía el árbol manteniendo el mismo orden."""
    global arbol
    arbol = ArbolMVias(arbol.orden)
    flash(f"Árbol de orden {arbol.orden} reiniciado.", "ok")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
