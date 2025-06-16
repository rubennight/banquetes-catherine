from flask import Blueprint, request, jsonify
from service.EmpleadoServiceClass import EmpleadoService
from service.EventoEmpleadoService import EventoEmpleadoService
from util.Database import obtener_conexion
from datetime import datetime


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


@empleado_controller.route('/empleados/registrar', methods=['POST'])
def registrar_empleado():
    data = request.get_json()
    print("DATA RECIBIDA:", data)
    if not data:
        return jsonify({"codigo": 400, "error": "No se recibió información para registrar el empleado"}), 400

    return EmpleadoService.registrar_empleado(data)
