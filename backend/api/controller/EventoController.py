from flask import Blueprint, request, jsonify
from util.Database import obtener_conexion
from datetime import datetime
from service.EventoService import EventoService

evento_controller = Blueprint('evento_controller', __name__)

@evento_controller.route('/eventos/asignarEmpleados', methods=['POST'])
def asignar_empleados_evento():
    data = request.get_json()
    return EventoService.asignar_empleados_evento(data)

@evento_controller.route('/eventos/listar', methods=['GET'])
def listar_eventos():
    return EventoService.listar_eventos()

@evento_controller.route('/eventos/buscarPorFecha', methods=['GET'])
def buscar_eventos_por_fecha():
    fecha_str = request.args.get('fecha')
    return EventoService.buscar_eventos_por_fecha(fecha_str)

@evento_controller.route('/eventos/registrar', methods=['POST'])
def registrar_evento():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No se recibieron datos", "codigo": 400}), 400
        return EventoService.registrar_evento(data)
    except Exception as e:
        return jsonify({"error": str(e), "codigo": 500}), 500