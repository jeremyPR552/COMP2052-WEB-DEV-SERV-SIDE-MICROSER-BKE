from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/info')
def info():
    return "Esta es una aplicación Flask simple."

@app.route('/mensaje', methods=['POST'])
def mensaje():
    data = request.get_json()
    return jsonify({"respuesta": data.get('mensaje', '')})

if __name__ == '__main__':
    app.run()
