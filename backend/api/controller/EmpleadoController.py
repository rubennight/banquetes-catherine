from flask import Blueprint, request, jsonify
from util.Database import obtener_conexion
from datetime import datetime
from service.EventoEmpleadoService import EventoEmpleadoService

empleado_controller = Blueprint('empleado_controller', __name__)

@empleado_controller.route('/empleados/porEvento', methods=['GET'])
def obtener_empleados_por_evento():
    id_evento = request.args.get('idEvento')
    if not id_evento:
        return jsonify({"error": "Falta el parámetro idEvento", "codigo": 400}), 400

    return EventoEmpleadoService.obtener_empleados_por_evento(id_evento)


@empleado_controller.route('/empleados/porDisponibilidad', methods=['GET'])
def obtener_empleados_por_disponibilidad():
    id_evento = request.args.get('idEvento')
    if not id_evento:
        return jsonify({"error": "Falta el parámetro idEvento", "codigo": 400}), 400

    return EventoEmpleadoService.obtener_empleados_disponibles_por_evento(id_evento)