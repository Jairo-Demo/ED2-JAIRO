# app.py
# =====================================================================
# CONTROLADOR (capa "C" de MVC, versión web)
# ---------------------------------------------------------------------
# Este archivo es el ÚNICO que conoce tanto al Modelo (models/modelo.py)
# como a la Vista (templates/index.html + static/style.css).
#
# Su trabajo es:
#   1. Recibir la petición HTTP (por ejemplo, cuando el usuario envía
#      el formulario "Insertar").
#   2. Leer los datos que mandó el usuario (request.form).
#   3. Llamar al método correspondiente de ArbolBinario (el Modelo).
#   4. Volver a mostrar la página (la Vista) con el resultado.
#
# IMPORTANTE: no se modificó ni una sola línea de models/modelo.py.
# Este archivo solo lo IMPORTA y USA sus métodos ya existentes:
# insertar(), buscar(), eliminar(), in_orden(), pre_orden(), post_orden(),
# get_raiz(), get_cantidad(), esta_vacio(), minimo(), maximo().
# =====================================================================

from flask import Flask, render_template, request, redirect, url_for, flash

# Importamos la clase ArbolBinario tal cual está en el Modelo.
from models.modelo import ArbolBinario

# Creamos la aplicación Flask. __name__ le dice a Flask en qué carpeta
# buscar las carpetas "templates/" y "static/".
app = Flask(__name__)

# La secret_key es obligatoria para poder usar flash() (los mensajes
# de "se insertó X" o "error") porque Flask los guarda cifrados en una
# cookie de sesión. En un proyecto real esto NO se deja así en texto
# plano, pero para un proyecto académico es suficiente.
app.secret_key = "clave-secreta-desarrollo"

# ---------------------------------------------------------------------
# ESTADO DEL ÁRBOL
# ---------------------------------------------------------------------
# A diferencia de la versión de escritorio (Tkinter), en la web no hay
# "una sola ejecución" del programa: cada clic del usuario es una
# petición HTTP nueva e independiente. Por eso el árbol se guarda aquí,
# como una variable global del módulo, y así todas las peticiones
# comparten el mismo árbol mientras el servidor de Flask siga corriendo.
arbol = ArbolBinario()


def nodo_a_dict(nodo):
    """
    Convierte un Nodo (y, recursivamente, todos sus hijos) en un
    diccionario simple, con esta forma:

        {"valor": 50,
         "izquierdo": {"valor": 30, "izquierdo": None, "derecho": None},
         "derecho": None}

    ¿Por qué hacer esto? Porque la plantilla HTML (Jinja2) no puede
    llamar a los métodos privados de Nodo directamente de forma
    cómoda; es más simple para la Vista recorrer un diccionario/lista
    que un objeto Python con getters. Este método es el "traductor"
    entre el Modelo y la Vista, y por eso vive en el Controlador.
    """
    if nodo is None:
        return None
    return {
        "valor": nodo.get_dato(),
        "izquierdo": nodo_a_dict(nodo.get_izquierdo()),
        "derecho": nodo_a_dict(nodo.get_derecho()),
    }


def leer_entero(texto):
    """
    Intenta convertir a int el texto que llega del formulario HTML.

    Los campos de un formulario siempre llegan como texto (str), así
    que aquí validamos que realmente sea un número entero antes de
    pasárselo al Modelo. Si no lo es (por ejemplo, el usuario dejó el
    campo vacío o escribió letras), devolvemos None para que la ruta
    que llamó a esta función pueda mostrar un mensaje de error.
    """
    try:
        return int(texto)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------
# RUTA PRINCIPAL: muestra la página completa
# ---------------------------------------------------------------------
@app.route("/")
def index():
    """
    Ruta GET "/". Se ejecuta cada vez que el navegador pide la página
    (al entrar por primera vez, o después de cada redirect() de las
    otras rutas).

    Arma un diccionario "contexto" con todo lo que la Vista necesita
    mostrar, y se lo pasa a render_template. Fíjate que aquí es donde
    se llama a los métodos de consulta del Modelo:
        arbol.get_raiz(), arbol.esta_vacio(), arbol.get_cantidad(),
        arbol.in_orden(), arbol.pre_orden(), arbol.post_orden(),
        arbol.minimo(), arbol.maximo()
    """
    # Convertimos el árbol de objetos Nodo a un diccionario anidado
    # para que la plantilla lo pueda dibujar con su macro recursivo.
    raiz = nodo_a_dict(arbol.get_raiz())

    contexto = {
        "raiz": raiz,
        "vacio": arbol.esta_vacio(),
        "cantidad": arbol.get_cantidad(),
        "in_orden": arbol.in_orden(),
        "pre_orden": arbol.pre_orden(),
        "post_orden": arbol.post_orden(),
        # minimo()/maximo() lanzan ValueError si el árbol está vacío,
        # así que los evitamos por completo cuando no hay nodos.
        "minimo": None if arbol.esta_vacio() else arbol.minimo(),
        "maximo": None if arbol.esta_vacio() else arbol.maximo(),
    }
    # render_template busca "index.html" dentro de la carpeta
    # templates/, y le inyecta cada clave del contexto como una
    # variable disponible en el HTML (ej: {{ cantidad }}).
    return render_template("index.html", **contexto)


# ---------------------------------------------------------------------
# RUTA: Insertar un valor
# ---------------------------------------------------------------------
@app.route("/insertar", methods=["POST"])
def insertar():
    """
    Se activa cuando el usuario envía el formulario "Insertar" de
    index.html (method="post", action="/insertar").

    Flujo: leer el valor del formulario -> validarlo -> llamar a
    arbol.insertar(valor) -> redirigir de vuelta a "/" para refrescar
    la página con el árbol actualizado.
    """
    # request.form es un diccionario con los datos que mandó el
    # formulario. "valor" es el name="valor" del <input> en el HTML.
    valor = leer_entero(request.form.get("valor"))

    if valor is None:
        # flash() guarda un mensaje que se muestra una sola vez, en
        # la siguiente página que se renderice (aquí, tras el redirect).
        flash("Escribe un número entero válido para insertar.", "error")
    else:
        # AQUÍ es la línea clave: se llama al método real del Modelo.
        arbol.insertar(valor)
        flash(f"Se insertó {valor} en el árbol.", "ok")

    # redirect + url_for evita reenviar el formulario si el usuario
    # recarga la página (patrón "Post/Redirect/Get").
    return redirect(url_for("index"))


# ---------------------------------------------------------------------
# RUTA: Buscar un valor
# ---------------------------------------------------------------------
@app.route("/buscar", methods=["POST"])
def buscar():
    """
    Se activa con el formulario "Buscar". Llama a arbol.buscar(valor),
    que devuelve True/False, y lo traduce en un mensaje para el
    usuario.
    """
    valor = leer_entero(request.form.get("valor"))

    if valor is None:
        flash("Escribe un número entero válido para buscar.", "error")
    elif arbol.buscar(valor):
        flash(f"{valor} SÍ está en el árbol.", "ok")
    else:
        flash(f"{valor} NO está en el árbol.", "error")

    return redirect(url_for("index"))


# ---------------------------------------------------------------------
# RUTA: Eliminar un valor
# ---------------------------------------------------------------------
@app.route("/eliminar", methods=["POST"])
def eliminar():
    """
    Se activa con el formulario "Eliminar". Llama a
    arbol.eliminar(valor), que internamente usa el sucesor inorden
    (tal como está implementado en el Modelo) y devuelve True/False
    según si el valor existía.
    """
    valor = leer_entero(request.form.get("valor"))

    if valor is None:
        flash("Escribe un número entero válido para eliminar.", "error")
    elif arbol.eliminar(valor):
        flash(f"Se eliminó {valor} del árbol.", "ok")
    else:
        flash(f"{valor} no estaba en el árbol, no se eliminó nada.", "error")

    return redirect(url_for("index"))


# ---------------------------------------------------------------------
# RUTA: Reiniciar el árbol completo
# ---------------------------------------------------------------------
@app.route("/reiniciar", methods=["POST"])
def reiniciar():
    """
    Reemplaza el árbol global por uno nuevo y vacío. Se usa "global"
    porque estamos reasignando la variable "arbol" definida fuera de
    esta función (si solo llamáramos a sus métodos, como arbol.insertar,
    no haría falta "global"; aquí sí, porque creamos un objeto nuevo).
    """
    global arbol
    arbol = ArbolBinario()
    flash("El árbol fue reiniciado.", "ok")
    return redirect(url_for("index"))


# ---------------------------------------------------------------------
# Punto de entrada: solo se ejecuta si corres "python app.py"
# directamente (no si Flask importa este archivo desde otro lado).
# debug=True recarga el servidor solo al guardar cambios y muestra
# errores detallados en el navegador; en producción se quita.
# ---------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
