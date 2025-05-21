from flask import Blueprint, request, jsonify
from app.models import db, Evento

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/dashboard')
def index():
    return '<h1>Corriendo en Modo de Prueba.</h1>'

@main.route('/eventos', methods=['GET'])
def listar_eventos():
    eventos = Evento.query.all()

    data = [
        {
            'id': evento.id,
            'nombre': evento.nombre,
            'ubicacion': evento.ubicacion,
            'fecha': evento.fecha,
            'descripcion': evento.descripcion,
            'organizador_id': evento.organizador_id
        }
        for evento in eventos
    ]
    return jsonify(data), 200

@main.route('/eventos/<int:id>', methods=['GET'])
def listar_un_evento(id):
    evento = Evento.query.get_or_404(id)

    data = {
        'id': evento.id,
        'nombre': evento.nombre,
        'ubicacion': evento.ubicacion,
        'fecha': evento.fecha,
        'descripcion': evento.descripcion,
        'organizador_id': evento.organizador_id
    }
    return jsonify(data), 200
