from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ejercicios')
def ejercicios():
    lista_ejercicios = [
        {"nombre": "Sentadillas", "musculo": "Piernas", "nivel": "Intermedio"},
        {"nombre": "Press de banca", "musculo": "Pecho", "nivel": "Avanzado"},
        {"nombre": "Remo con barra", "musculo": "Espalda", "nivel": "Avanzado"},
        {"nombre": "Cinta de correr", "musculo": "Cardio", "nivel": "Básico"}
    ]
    return render_template('ejercicios.html', ejercicios=lista_ejercicios)

@app.route('/dietas')
def dietas():
    lista_dietas = [
        {"tipo": "Volumen", "calorias": 3000, "descripcion": "Alta en carbohidratos y proteínas."},
        {"tipo": "Definición", "calorias": 1800, "descripcion": "Baja en grasas y azúcares."},
        {"tipo": "Mantenimiento", "calorias": 2200, "descripcion": "Balanceada con todos los macros."}
    ]
    return render_template('dietas.html', dietas=lista_dietas)

if __name__ == '__main__':
    app.run(debug=True)
