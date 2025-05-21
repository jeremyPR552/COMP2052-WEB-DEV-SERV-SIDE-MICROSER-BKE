from flask import Blueprint, request, jsonify
from app.models import db, Evento
  # Aquí el modelo se sigue llamando Curso para no cambiar nombre de archivos/clases

# Blueprint solo con endpoints de prueba para eventos
main = Blueprint('main', __name__)

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return jsonify({'message': 'Ruta de login aún no implementada'}), 200

@auth.route('/logout')
def logout():
    return jsonify({'message': 'Ruta de logout aún no implementada'}), 200

@main.route('/') # Ambas rutas llevan al mismo lugar
@main.route('/dashboard')
def index():
    """
    Página de inicio pública (home).
    """
    return '<h1>Corriendo en Modo de Prueba.</h1>'

@main.route('/cursos', methods=['GET'])
def listar_eventos():
    """
    Retorna una lista de eventos (JSON).
    """
    eventos = Evento.query.all()

    data = [
        {'id': evento.id, 'titulo': evento.titulo, 'descripcion': evento.descripcion, 'organizador_id': evento.profesor_id}
        for evento in eventos
    ]
    return jsonify(data), 200

@main.route('/cursos/<int:id>', methods=['GET'])
def listar_un_evento(id):
    """
    Retorna un solo evento por su ID (JSON).
    """
    evento = Evento.query.get_or_404(id)

    data = {
        'id': evento.id,
        'titulo': evento.titulo,
        'descripcion': evento.descripcion,
        'organizador_id': evento.profesor_id
    }

    return jsonify(data), 200

@main.route('/cursos', methods=['POST'])
def crear_evento():
    """
    Crea un evento sin validación.
    Espera JSON con 'titulo', 'descripcion' y 'organizador_id'.
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    evento = Evento(
        titulo=data.get('titulo'),
        descripcion=data.get('descripcion'),
        profesor_id=data.get('organizador_id')  # sin validación de usuario
    )

    db.session.add(evento)
    db.session.commit()

    return jsonify({'message': 'Evento creado', 'id': evento.id, 'organizador_id': evento.profesor_id}), 201

@main.route('/cursos/<int:id>', methods=['PUT'])
def actualizar_evento(id):
    """
    Actualiza un evento sin validación de usuario o permisos.
    """
    evento = Evento.query.get_or_404(id)
    data = request.get_json()

    evento.titulo = data.get('titulo', evento.titulo)
    evento.descripcion = data.get('descripcion', evento.descripcion)
    evento.profesor_id = data.get('organizador_id', evento.profesor_id)

    db.session.commit()

    return jsonify({'message': 'Evento actualizado', 'id': evento.id}), 200

@main.route('/cursos/<int:id>', methods=['DELETE'])
def eliminar_evento(id):
    """
    Elimina un evento sin validación de permisos.
    """
    evento = Evento.query.get_or_404(id)
    db.session.delete(evento)
    db.session.commit()

    return jsonify({'message': 'Evento eliminado', 'id': evento.id}), 200
