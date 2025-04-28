from flask import Flask, redirect, url_for, request, jsonify, render_template, session
from flask_principal import Principal, Permission, RoleNeed, Identity, identity_changed, identity_loaded, AnonymousIdentity

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Inicializar Principal
principals = Principal(app)

# Definir roles
admin_permission = Permission(RoleNeed('admin'))
user_permission = Permission(RoleNeed('user'))

# Diccionario simulado de usuarios
users = {
    'admin_user': {'password': 'admin123', 'roles': ['admin']},
    'normal_user': {'password': 'user123', 'roles': ['user']}
}

# Cargar identidad
@app.before_request
def load_identity():
    if 'user' in session:
        identity_changed.send(app, identity=Identity(session['user']))
    else:
        identity_changed.send(app, identity=AnonymousIdentity())

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    username = identity.id
    user = users.get(username)
    if user:
        for role in user['roles']:
            identity.provides.add(RoleNeed(role))

# Rutas
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and user['password'] == password:
            session['user'] = username
            return redirect(url_for('home'))
        else:
            return "Credenciales incorrectas", 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/admin')
@admin_permission.require(http_exception=403)
def admin_page():
    return render_template('admin.html')

@app.route('/user')
@user_permission.require(http_exception=403)
def user_page():
    return render_template('user.html')

@app.errorhandler(403)
def access_denied(e):
    return render_template('denied.html'), 403

if __name__ == '__main__':
    app.run(debug=True)
