from flask import Blueprint, request, jsonify
from api.model.EventoModel import Evento
from api.service.EventoService import EventoService
from api.util.Database import Database

evento_controller = Blueprint('evento_controller', __name__)
evento_service = EventoService(Database())

@evento_controller.route('/eventos', methods=['POST'])
def crear_evento():
    data = request.json
    evento = Evento(
        id_evento=data['id_evento'],
        fecha_evento=data['fecha_evento'],
        hora_evento=data['hora_evento'],
        tipo_evento=data['tipo_evento'],
        descripcion=data['descripcion'],
        total_precio=data['total_precio']
    )
    evento_service.crear_evento(evento)
    return jsonify({'mensaje': 'Evento creado correctamente'}), 201

@evento_controller.route('/eventos/<int:id_evento>', methods=['GET'])
def obtener_evento(id_evento):
    evento = evento_service.obtener_evento_por_id(id_evento)
    if evento:
        return jsonify(evento), 200
    return jsonify({'mensaje': 'Evento no encontrado'}), 404

@evento_controller.route('/eventos', methods=['GET'])
def obtener_todos():
    eventos = evento_service.obtener_todos_los_eventos()
    return jsonify(eventos), 200

@evento_controller.route('/eventos/<int:id_evento>', methods=['PUT'])
def actualizar_evento(id_evento):
    datos = request.json
    actualizado = evento_service.actualizar_evento(id_evento, datos)
    if actualizado:
        return jsonify({'mensaje': 'Evento actualizado correctamente'}), 200
    return jsonify({'mensaje': 'Evento no encontrado'}), 404

@evento_controller.route('/eventos/<int:id_evento>', methods=['DELETE'])
def eliminar_evento(id_evento):
    eliminado = evento_service.eliminar_evento(id_evento)
    if eliminado:
        return jsonify({'mensaje': 'Evento eliminado correctamente'}), 200
    return jsonify({'mensaje': 'Evento no encontrado'}), 404
