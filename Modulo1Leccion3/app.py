from flask import Flask, request, jsonify

app = Flask(__name__)

# Lista para guardar los usuarios en memoria
usuarios = []

# Ruta GET /info
@app.route('/info', methods=['GET'])
def info():
    return jsonify({"sistema": "Gestion de usuarios y productos"})

# Ruta POST /crear_usuario
@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    nombre = data.get('nombre')
    correo = data.get('correo')

    if not nombre or not correo:
        return jsonify({"error": "Faltan datos: nombre y correo son requeridos"}), 400

    usuario = {"nombre": nombre, "correo": correo}
    usuarios.append(usuario)
    return jsonify({"usuario": usuario})

# Ruta GET /usuarios
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    return jsonify(usuarios)

if __name__ == '__main__':
    app.run(debug=True)

