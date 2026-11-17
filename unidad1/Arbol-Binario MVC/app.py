"""Controlador web (Flask) del Árbol Binario de Búsqueda.

Recibe los formularios de la página, llama a los métodos de
ArbolBinario (el Modelo) y vuelve a mostrar la página (la Vista).

Ejecutar desde esta carpeta:  python app.py
Abrir en el navegador:        http://127.0.0.1:5000/
"""

from flask import Flask, flash, redirect, render_template, request, url_for

from models.modelo import ArbolBinario

app = Flask(__name__)
# Necesaria para mostrar mensajes con flash().
app.secret_key = "clave-secreta-desarrollo"

# Un solo árbol compartido por todas las peticiones mientras el
# servidor esté encendido.
arbol = ArbolBinario()


def nodo_a_diccionario(nodo):
    """Convierte un Nodo y sus hijos en diccionarios para la plantilla."""
    if nodo is None:
        return None
    return {
        "valor": nodo.get_dato(),
        "izquierdo": nodo_a_diccionario(nodo.get_izquierdo()),
        "derecho": nodo_a_diccionario(nodo.get_derecho()),
    }


def leer_entero(texto):
    """Convierte el texto del formulario a int, o None si no es válido."""
    try:
        return int(texto)
    except (TypeError, ValueError):
        return None


@app.route("/")
def index():
    """Muestra la página con el árbol y sus datos."""
    vacio = arbol.esta_vacio()
    datos_pagina = {
        "raiz": nodo_a_diccionario(arbol.get_raiz()),
        "vacio": vacio,
        "cantidad": arbol.get_cantidad(),
        "altura": arbol.altura(),
        "hojas": arbol.contar_hojas(),
        "es_balanceado": arbol.es_balanceado(),
        "es_valido": arbol.es_abb_valido(),
        "por_niveles": arbol.por_niveles(),
        "in_orden": arbol.in_orden(),
        "pre_orden": arbol.pre_orden(),
        "post_orden": arbol.post_orden(),
        # minimo() y maximo() fallan con el árbol vacío.
        "minimo": None if vacio else arbol.minimo(),
        "maximo": None if vacio else arbol.maximo(),
    }
    return render_template("index.html", **datos_pagina)


@app.route("/insertar", methods=["POST"])
def insertar():
    valor = leer_entero(request.form.get("valor"))
    if valor is None:
        flash("Escribe un número entero válido para insertar.", "error")
    else:
        arbol.insertar(valor)
        flash(f"Se insertó {valor} en el árbol.", "ok")
    # Volver a la página principal (evita reenviar el formulario).
    return redirect(url_for("index"))


@app.route("/buscar", methods=["POST"])
def buscar():
    valor = leer_entero(request.form.get("valor"))
    if valor is None:
        flash("Escribe un número entero válido para buscar.", "error")
    elif arbol.buscar(valor):
        flash(f"{valor} SÍ está en el árbol.", "ok")
    else:
        flash(f"{valor} NO está en el árbol.", "error")
    return redirect(url_for("index"))


@app.route("/sucesor", methods=["POST"])
def buscar_sucesor():
    valor = leer_entero(request.form.get("valor"))
    if valor is None:
        flash("Escribe un número entero válido para buscar su sucesor.",
              "error")
        return redirect(url_for("index"))

    sucesor = arbol.sucesor(valor)
    if sucesor is not None:
        flash(f"El sucesor inorden de {valor} es {sucesor}.", "ok")
    elif not arbol.buscar(valor):
        flash(f"El valor {valor} no existe en el árbol.", "error")
    else:
        flash(f"El valor {valor} es el máximo del árbol "
              "(no tiene sucesor).", "ok")
    return redirect(url_for("index"))


@app.route("/eliminar", methods=["POST"])
def eliminar():
    valor = leer_entero(request.form.get("valor"))
    if valor is None:
        flash("Escribe un número entero válido para eliminar.", "error")
    elif arbol.eliminar(valor):
        flash(f"Se eliminó {valor} del árbol.", "ok")
    else:
        flash(f"{valor} no estaba en el árbol, no se eliminó nada.", "error")
    return redirect(url_for("index"))


@app.route("/reiniciar", methods=["POST"])
def reiniciar():
    """Reemplaza el árbol por uno vacío."""
    global arbol  # se asigna un objeto nuevo a la variable global
    arbol = ArbolBinario()
    flash("El árbol fue reiniciado.", "ok")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
