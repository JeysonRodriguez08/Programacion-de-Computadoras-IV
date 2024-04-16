from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulación de datos de recetas
recetas = [
    {"id": 1, "nombre": "Tarta de manzana", "ingredientes": ["manzanas", "harina", "azúcar"], "pasos": "1. Pelar las manzanas..."},
    {"id": 2, "nombre": "Pasta Alfredo", "ingredientes": ["pasta", "crema", "queso parmesano"], "pasos": "1. Cocinar la pasta..."}
]

# Rutas de la API

# Obtener todas las recetas
@app.route('/api/recetas', methods=['GET'])
def get_recetas():
    return jsonify(recetas)

# Obtener una receta por su ID
@app.route('/api/recetas/<int:id>', methods=['GET'])
def get_receta(id):
    receta = next((receta for receta in recetas if receta['id'] == id), None)
    if receta:
        return jsonify(receta)
    else:
        return jsonify({"message": "Receta no encontrada"}), 404

# Crear una nueva receta
@app.route('/api/recetas', methods=['POST'])
def create_receta():
    data = request.json
    nueva_receta = {
        "id": len(recetas) + 1,
        "nombre": data.get('nombre'),
        "ingredientes": data.get('ingredientes'),
        "pasos": data.get('pasos')
    }
    recetas.append(nueva_receta)
    return jsonify({"message": "Receta creada correctamente"}), 201

# Actualizar una receta existente
@app.route('/api/recetas/<int:id>', methods=['PUT'])
def update_receta(id):
    data = request.json
    receta = next((receta for receta in recetas if receta['id'] == id), None)
    if receta:
        receta.update(data)
        return jsonify({"message": "Receta actualizada correctamente"})
    else:
        return jsonify({"message": "Receta no encontrada"}), 404

# Eliminar una receta existente
@app.route('/api/recetas/<int:id>', methods=['DELETE'])
def delete_receta(id):
    global recetas
    recetas = [receta for receta in recetas if receta['id'] != id]
    return jsonify({"message": "Receta eliminada correctamente"})

if __name__ == '__main__':
    app.run(debug=True)
