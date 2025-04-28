from flask import Flask, request, jsonify

app = Flask(__name__)

# Ruta que maneja peticiones GET a la URL '/info'
@app.route('/info')
def info():
    return "Esta es una aplicacion Flask simple."

# Ruta que maneja peticiones POST a la URL '/mensaje'
@app.route('/mensaje', methods=['POST'])
def mensaje():
    data = request.get_json()
    return jsonify({"respuesta": data.get('mensaje', '')})

if __name__ == '__main__':
    app.run()
