from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Inicialización de Flask
app = Flask(__name__)
app.secret_key = 'secreto_extremo'

# Configuración de LoginManager
login = LoginManager()
login.init_app(app)
login.login_view = 'acceso'

# Simulación de base de datos
datos_usuarios = {
    'Alex': {'id': '1', 'nombre': 'Alex', 'clave': generate_password_hash('pass123'), 'nivel': 'admin'},
    'Chris': {'id': '2', 'nombre': 'Chris', 'clave': generate_password_hash('mypassword'), 'nivel': 'user'}
}

# Modelo de usuario
class Cuenta(UserMixin):
    def __init__(self, id, nombre, clave, nivel):
        self.id = id
        self.nombre = nombre
        self.clave = clave
        self.nivel = nivel

    def es_admin(self):
        return self.nivel == 'admin'

def encontrar_usuario(nombre):
    usuario = datos_usuarios.get(nombre)
    if usuario:
        return Cuenta(usuario['id'], usuario['nombre'], usuario['clave'], usuario['nivel'])
    return None

def encontrar_por_id(id):
    for usuario in datos_usuarios.values():
        if usuario['id'] == id:
            return Cuenta(usuario['id'], usuario['nombre'], usuario['clave'], usuario['nivel'])
    return None

@login.user_loader
def cargar_cuenta(id_usuario):
    return encontrar_por_id(id_usuario)

# Rutas
@app.route('/')
def principal():
    return render_template('inicio.html')

@app.route('/acceso', methods=['GET', 'POST'])
def acceso():
    if request.method == 'POST':
        nombre = request.form['nombre']
        clave = request.form['clave']
        usuario = encontrar_usuario(nombre)
        
        if usuario and check_password_hash(usuario.clave, clave):
            login_user(usuario)
            return redirect(url_for('panel_principal'))
        else:
            return render_template('login.html', error='Usuario o contraseña inválidos')
    return render_template('login.html')

@app.route('/panel')
@login_required
def panel_principal():
    if current_user.es_admin():
        return render_template('panel_admin.html', nombre=current_user.nombre)
    else:
        return render_template('panel_usuario.html', nombre=current_user.nombre)

@app.route('/cerrar')
@login_required
def cerrar():
    logout_user()
    return redirect(url_for('principal'))

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
