from flask import Blueprint, request, jsonify
from app.models import db, Evento  # Cambiado a Evento

# Blueprint solo con endpoints de prueba para eventos
main = Blueprint('main', __name__)

@main.route('/')  # Ambas rutas llevan al mismo lugar
@main.route('/dashboard')
def index():
    """
    Página de inicio pública (home).
    """
    return '<h1>Corriendo en Modo de Prueba.</h1>'

@main.route('/eventos', methods=['GET'])
def listar_eventos():
    """
    Retorna una lista de eventos (JSON).
    """
    eventos = Evento.query.all()

    data = [
        {'id': evento.id, 'nombre': evento.nombre, 'descripcion': evento.descripcion, 'organizador_id': evento.organizador_id}
        for evento in eventos
    ]
    return jsonify(data), 200

@main.route('/eventos/<int:id>', methods=['GET'])
def listar_un_evento(id):
    """
    Retorna un solo evento por su ID (JSON).
    """
    evento = Evento.query.get_or_404(id)

    data = {
        'id': evento.id,
        'nombre': evento.nombre,
        'descripcion': evento.descripcion,
        'organizador_id': evento.organizador_id
    }

    return jsonify(data), 200

@main.route('/eventos', methods=['POST'])
def crear_evento():
    """
    Crea un evento sin validación.
    Espera JSON con 'nombre', 'descripcion' y 'organizador_id'.
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    evento = Evento(
        nombre=data.get('nombre'),
        descripcion=data.get('descripcion'),
        organizador_id=data.get('organizador_id')  # sin validación de usuario
    )

    db.session.add(evento)
    db.session.commit()

    return jsonify({'message': 'Evento creado', 'id': evento.id, 'organizador_id': evento.organizador_id}), 201

@main.route('/eventos/<int:id>', methods=['PUT'])
def actualizar_evento(id):
    """
    Actualiza un evento sin validación de usuario o permisos.
    """
    evento = Evento.query.get_or_404(id)
    data = request.get_json()

    evento.nombre = data.get('nombre', evento.nombre)
    evento.descripcion = data.get('descripcion', evento.descripcion)
    evento.organizador_id = data.get('organizador_id', evento.organizador_id)

    db.session.commit()

    return jsonify({'message': 'Evento actualizado', 'id': evento.id}), 200

@main.route('/eventos/<int:id>', methods=['DELETE'])
def eliminar_evento(id):
    """
    Elimina un evento sin validación de permisos.
    """
    evento = Evento.query.get_or_404(id)
    db.session.delete(evento)
    db.session.commit()

    return jsonify({'message': 'Evento eliminado', 'id': evento.id}), 200
