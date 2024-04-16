from flask import Flask, jsonify
import requests

app = Flask(__name__)

# URL de la API del Banco Mundial para los datos de vacunación contra el sarampión en Panamá
url_api = 'http://api.worldbank.org/v2/country/PAN/indicator/SH.IMM.MEAS?date=2000:2018&format=json'

def obtener_datos_vacunacion_desde_api(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Los datos se devuelven como una lista de diccionarios en formato JSON
            data = response.json()[1]
            # Filtrar los datos para obtener solo los relacionados con la vacunación en niños de 12 a 23 meses
            filtered_data = [item for item in data if int(item['date']) >= 2000 and int(item['date']) <= 2018]
            return filtered_data
        else:
            print(f'Error al obtener los datos: {response.status_code}')
            return None
    except Exception as e:
        print(f'Error de conexión: {e}')
        return None

datos_vacunacion = obtener_datos_vacunacion_desde_api(url_api)

@app.route('/', methods=['GET'])
def get_vacunacion_sarampion_panama():
    if datos_vacunacion:
        # Filtrar los datos para obtener solo los relacionados con la vacunación en niños de 12 a 23 meses
        filtered_data = [item for item in datos_vacunacion if int(item['date']) >= 2000 and int(item['date']) <= 2018]
        return jsonify(filtered_data)
    else:
        return jsonify({'error': 'No se pudieron obtener los datos de vacunación.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
