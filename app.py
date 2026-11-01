# =====================================================================
# app.py (Panel Unificado - Árbol Binario & Árbol M-Vías)
# =====================================================================
import os
import sys
import importlib.util
from flask import Flask, render_template, request, redirect, url_for, flash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------
# Carga modular de modelos desde sus respectivas carpetas MVC
# ---------------------------------------------------------------------
# 1. Árbol Binario
binario_model_path = os.path.join(BASE_DIR, "Arbol-Binario MVC", "models", "modelo.py")
spec_binario = importlib.util.spec_from_file_location("modelo_binario", binario_model_path)
mod_binario = importlib.util.module_from_spec(spec_binario)
spec_binario.loader.exec_module(mod_binario)
ArbolBinario = mod_binario.ArbolBinario

# 2. Árbol M-Vías
mvias_nodo_path = os.path.join(BASE_DIR, "Arbol-MVias MVC", "models", "nodo_mvias.py")
spec_nodo = importlib.util.spec_from_file_location("nodo_mvias", mvias_nodo_path)
mod_nodo = importlib.util.module_from_spec(spec_nodo)
sys.modules["nodo_mvias"] = mod_nodo
spec_nodo.loader.exec_module(mod_nodo)

mvias_model_path = os.path.join(BASE_DIR, "Arbol-MVias MVC", "models", "arbol_mvias.py")
spec_mvias = importlib.util.spec_from_file_location("arbol_mvias", mvias_model_path)
mod_mvias = importlib.util.module_from_spec(spec_mvias)
spec_mvias.loader.exec_module(mod_mvias)
ArbolMVias = mod_mvias.ArbolMVias

# ---------------------------------------------------------------------
# Configuración de Flask
# ---------------------------------------------------------------------
app = Flask(__name__)
app.secret_key = "clave-dashboard-ed2-jairo"

# Estado de ambos árboles en memoria
arbol_binario = ArbolBinario()
arbol_mvias = ArbolMVias(3)


# ---------------------------------------------------------------------
# Funciones traductoras (Modelo -> Diccionario para Vista HTML)
# ---------------------------------------------------------------------
def nodo_binario_a_dict(nodo):
    if nodo is None:
        return None
    return {
        "valor": nodo.get_dato(),
        "izquierdo": nodo_binario_a_dict(nodo.get_izquierdo()),
        "derecho": nodo_binario_a_dict(nodo.get_derecho()),
    }


def nodo_mvias_a_dict(nodo):
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


def leer_entero(texto):
    try:
        return int(texto)
    except (TypeError, ValueError):
        return None


def parsear_enteros(texto):
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


# ---------------------------------------------------------------------
# RUTA PRINCIPAL (Una sola página con ambos árboles)
# ---------------------------------------------------------------------
@app.route("/")
def index():
    # Contexto Árbol Binario
    raiz_bin = nodo_binario_a_dict(arbol_binario.get_raiz())
    contexto_binario = {
        "raiz": raiz_bin,
        "vacio": arbol_binario.esta_vacio(),
        "cantidad": arbol_binario.get_cantidad(),
        "in_orden": arbol_binario.in_orden(),
        "pre_orden": arbol_binario.pre_orden(),
        "post_orden": arbol_binario.post_orden(),
        "minimo": None if arbol_binario.esta_vacio() else arbol_binario.minimo(),
        "maximo": None if arbol_binario.esta_vacio() else arbol_binario.maximo(),
    }

    # Contexto Árbol M-Vías
    raiz_mv = nodo_mvias_a_dict(arbol_mvias.raiz)
    recorrido_en_orden = arbol_mvias.en_orden()
    contexto_mvias = {
        "orden": arbol_mvias.orden,
        "raiz": raiz_mv,
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

    return render_template(
        "index.html",
        binario=contexto_binario,
        mvias=contexto_mvias
    )


# ---------------------------------------------------------------------
# ACCIONES: ÁRBOL BINARIO
# ---------------------------------------------------------------------
@app.route("/binario/insertar", methods=["POST"])
def binario_insertar():
    valor = leer_entero(request.form.get("valor"))
    if valor is None:
        flash("Árbol Binario: Ingresa un número entero válido.", "binario_error")
    else:
        arbol_binario.insertar(valor)
        flash(f"Árbol Binario: Se insertó el valor {valor}.", "binario_ok")
    return redirect(url_for("index") + "#panel-binario")


@app.route("/binario/buscar", methods=["POST"])
def binario_buscar():
    valor = leer_entero(request.form.get("valor"))
    if valor is None:
        flash("Árbol Binario: Ingresa un número entero para buscar.", "binario_error")
    elif arbol_binario.buscar(valor):
        flash(f"Árbol Binario: El valor {valor} SÍ está en el árbol.", "binario_ok")
    else:
        flash(f"Árbol Binario: El valor {valor} NO está en el árbol.", "binario_error")
    return redirect(url_for("index") + "#panel-binario")


@app.route("/binario/eliminar", methods=["POST"])
def binario_eliminar():
    valor = leer_entero(request.form.get("valor"))
    if valor is None:
        flash("Árbol Binario: Ingresa un número entero para eliminar.", "binario_error")
    elif arbol_binario.eliminar(valor):
        flash(f"Árbol Binario: Se eliminó el valor {valor}.", "binario_ok")
    else:
        flash(f"Árbol Binario: El valor {valor} no estaba en el árbol.", "binario_error")
    return redirect(url_for("index") + "#panel-binario")


@app.route("/binario/reiniciar", methods=["POST"])
def binario_reiniciar():
    global arbol_binario
    arbol_binario = ArbolBinario()
    flash("Árbol Binario: Ha sido reiniciado.", "binario_ok")
    return redirect(url_for("index") + "#panel-binario")


# ---------------------------------------------------------------------
# ACCIONES: ÁRBOL M-VÍAS
# ---------------------------------------------------------------------
@app.route("/mvias/insertar", methods=["POST"])
def mvias_insertar():
    claves = parsear_enteros(request.form.get("valor", ""))
    if not claves:
        flash("Árbol M-Vías: Ingresa un número válido (o varios ej: 10,20,30).", "mvias_error")
    else:
        for c in claves:
            arbol_mvias.insertar(c)
        if len(claves) == 1:
            flash(f"Árbol M-Vías: Clave {claves[0]} insertada.", "mvias_ok")
        else:
            flash(f"Árbol M-Vías: {len(claves)} claves insertadas: {claves}.", "mvias_ok")
    return redirect(url_for("index") + "#panel-mvias")


@app.route("/mvias/buscar", methods=["POST"])
def mvias_buscar():
    claves = parsear_enteros(request.form.get("valor", ""))
    if not claves:
        flash("Árbol M-Vías: Ingresa un número entero para buscar.", "mvias_error")
    else:
        c = claves[0]
        if arbol_mvias.buscar(c):
            flash(f"Árbol M-Vías: La clave {c} SÍ existe en el árbol.", "mvias_ok")
        else:
            flash(f"Árbol M-Vías: La clave {c} NO existe en el árbol.", "mvias_error")
    return redirect(url_for("index") + "#panel-mvias")


@app.route("/mvias/orden", methods=["POST"])
def mvias_orden():
    global arbol_mvias
    nuevo_orden = leer_entero(request.form.get("orden"))
    if nuevo_orden is None or nuevo_orden < 2:
        flash("Árbol M-Vías: El orden M debe ser un número entero >= 2.", "mvias_error")
    else:
        arbol_mvias = ArbolMVias(nuevo_orden)
        flash(f"Árbol M-Vías: Reiniciado con nuevo orden M = {nuevo_orden}.", "mvias_ok")
    return redirect(url_for("index") + "#panel-mvias")


@app.route("/mvias/reiniciar", methods=["POST"])
def mvias_reiniciar():
    global arbol_mvias
    arbol_mvias = ArbolMVias(arbol_mvias.orden)
    flash(f"Árbol M-Vías (orden {arbol_mvias.orden}): Ha sido reiniciado.", "mvias_ok")
    return redirect(url_for("index") + "#panel-mvias")


if __name__ == "__main__":
    print("Iniciando servidor web...")
    print("Abre tu navegador en: http://127.0.0.1:5000/")
    app.run(debug=True, port=5000)

