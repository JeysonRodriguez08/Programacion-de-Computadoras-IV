from flask import Flask, render_template, request, redirect, url_for
import json
from redis import StrictRedis

app = Flask(__name__)
DATABASE_URL = "redis://localhost:6379/0"
redis_client = StrictRedis.from_url(DATABASE_URL)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agregar_receta', methods=['POST'])
def agregar_receta():
    nombre = request.form['nombre']
    ingredientes = request.form['ingredientes']
    pasos = request.form['pasos']

    receta = {
        "nombre": nombre,
        "ingredientes": ingredientes,
        "pasos": pasos
    }

    redis_client.set(f"receta:{nombre}", json.dumps(receta))
    return redirect(url_for('index'))

@app.route('/actualizar_receta', methods=['POST'])
def actualizar_receta():
    nombre = request.form['nombre']
    receta_json = redis_client.get(f"receta:{nombre}")

    if receta_json:
        receta = json.loads(receta_json.decode('utf-8'))
        nuevos_datos = request.form.to_dict()

        for key, value in nuevos_datos.items():
            if value and key in receta:
                receta[key] = value

        redis_client.set(f"receta:{nombre}", json.dumps(receta))
    return redirect(url_for('index'))

@app.route('/eliminar_receta', methods=['POST'])
def eliminar_receta():
    nombre = request.form['nombre']
    redis_client.delete(f"receta:{nombre}")
    return redirect(url_for('index'))

@app.route('/ver_recetas')
def ver_recetas():
    keys = redis_client.keys("receta:*")
    recetas = []

    for key in keys:
        receta_json = redis_client.get(key)
        receta = json.loads(receta_json.decode('utf-8'))
        recetas.append(receta)

    return render_template('recetas.html', recetas=recetas)

@app.route('/buscar_receta', methods=['POST'])
def buscar_receta():
    keyword = request.form['keyword']
    keys = redis_client.keys("receta:*")
    resultados = []

    for key in keys:
        receta_json = redis_client.get(key)
        receta = json.loads(receta_json.decode('utf-8'))

        if keyword.lower() == receta["nombre"].lower():
            resultados.append(receta)

    if not resultados:
        return "No se encontraron recetas con ese nombre."
    else:
        return render_template('resultados_busqueda.html', resultados=resultados)

if __name__ == "__main__":
    app.run(debug=True)
