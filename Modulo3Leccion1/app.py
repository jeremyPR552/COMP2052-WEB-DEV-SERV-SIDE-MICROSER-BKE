from flask import Flask, render_template, redirect, url_for, request, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secreto'

# Base de datos simulada
usuarios = {
    "admin": {
        "password": generate_password_hash("admin123"),
        "rol": "admin"
    },
    "usuario": {
        "password": generate_password_hash("usuario123"),
        "rol": "user"
    }
}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['username']
        contraseña = request.form['password']
        if usuario in usuarios and check_password_hash(usuarios[usuario]['password'], contraseña):
            session['usuario'] = usuario
            return redirect(url_for('dashboard'))
        else:
            return "Credenciales inválidas"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario' in session:
        usuario = session['usuario']
        rol = usuarios[usuario]['rol']
        return render_template('dashboard.html', usuario=usuario, rol=rol)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
