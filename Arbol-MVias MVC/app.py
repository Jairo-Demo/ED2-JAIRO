# =====================================================================
# Arbol-MVias MVC - app.py (Controlador Web MVC)
# =====================================================================
import os
import sys

# Asegurar que la carpeta actual esté en sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, redirect, url_for, flash
from models.arbol_mvias import ArbolMVias

app = Flask(__name__)
app.secret_key = "clave-secreta-mvias"

# Instancia global del árbol M-Vías (por defecto orden 3)
arbol_mvias = ArbolMVias(3)


def nodo_mvias_a_dict(nodo):
    """
    Convierte un NodoMVias y sus ramas en un diccionario recursivo
    para que la plantilla Jinja2 lo pueda renderizar fácilmente.
    """
    if nodo is None:
        return None
    claves = list(nodo.get_claves())
    hijos = nodo.get_hijos()
    tiene_hijos = any(h is not None for h in hijos)
    
    hijos_dict = []
    if tiene_hijos:
        total = max(len(hijos), len(claves) + 1)
        for i in range(total):
            h = hijos[i] if i < len(hijos) else None
            hijos_dict.append(nodo_mvias_a_dict(h))
            
    return {
        "claves": claves,
        "tiene_hijos": tiene_hijos,
        "hijos": hijos_dict
    }


def parsear_claves(texto):
    """
    Convierte una cadena de números (uno solo o varios separados por comas/espacios)
    en una lista de enteros.
    """
    if not texto:
        return []
    partes = texto.replace(";", ",").replace(" ", ",").split(",")
    resultado = []
    for p in partes:
        p = p.strip()
        if p:
            try:
                resultado.append(int(p))
            except ValueError:
                pass
    return resultado


@app.route("/")
def index():
    raiz_dict = nodo_mvias_a_dict(arbol_mvias.raiz)
    recorrido_en_orden = arbol_mvias.en_orden()
    
    contexto = {
        "orden": arbol_mvias.orden,
        "raiz": raiz_dict,
        "vacio": arbol_mvias.esta_vacio(),
        "total_claves": len(recorrido_en_orden),
        "altura": arbol_mvias.altura(),
        "minimo": arbol_mvias.minimo(),
        "maximo": arbol_mvias.maximo(),
        "en_orden": recorrido_en_orden,
        "pre_orden": arbol_mvias.pre_orden(),
        "post_orden": arbol_mvias.post_orden(),
        "por_niveles": arbol_mvias.por_niveles(),
        "niveles_texto": arbol_mvias.obtener_niveles_texto(),
    }
    return render_template("index.html", **contexto)


@app.route("/insertar", methods=["POST"])
def insertar():
    valor_txt = request.form.get("valor", "")
    claves = parsear_claves(valor_txt)
    
    if not claves:
        flash("Ingresa un número entero válido (o varios separados por comas).", "error")
    else:
        for c in claves:
            arbol_mvias.insertar(c)
        if len(claves) == 1:
            flash(f"Clave {claves[0]} insertada con éxito.", "ok")
        else:
            flash(f"{len(claves)} claves insertadas: {claves}", "ok")
            
    return redirect(url_for("index"))


@app.route("/buscar", methods=["POST"])
def buscar():
    valor_txt = request.form.get("valor", "")
    claves = parsear_claves(valor_txt)
    
    if not claves:
        flash("Ingresa un número entero para buscar.", "error")
    else:
        c = claves[0]
        if arbol_mvias.buscar(c):
            flash(f"La clave {c} SÍ existe en el árbol M-Vías.", "ok")
        else:
            flash(f"La clave {c} NO existe en el árbol M-Vías.", "error")
            
    return redirect(url_for("index"))


@app.route("/orden", methods=["POST"])
def cambiar_orden():
    global arbol_mvias
    orden_txt = request.form.get("orden", "")
    try:
        nuevo_orden = int(orden_txt)
        if nuevo_orden < 2:
            flash("El orden M debe ser al menos 2.", "error")
        else:
            arbol_mvias = ArbolMVias(nuevo_orden)
            flash(f"Árbol M-Vías reiniciado con nuevo orden M = {nuevo_orden}.", "ok")
    except ValueError:
        flash("Orden inválido.", "error")
        
    return redirect(url_for("index"))


@app.route("/reiniciar", methods=["POST"])
def reiniciar():
    global arbol_mvias
    arbol_mvias = ArbolMVias(arbol_mvias.orden)
    flash(f"Árbol M-Vías (orden {arbol_mvias.orden}) ha sido reiniciado.", "ok")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)

