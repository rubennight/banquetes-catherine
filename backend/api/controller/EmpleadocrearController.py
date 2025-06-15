from flask import Blueprint, request, jsonify
from service.EmpleadocrearService import EmpleadocrearService

empleado_crear_controller = Blueprint('empleado_crear_controller', __name__)

@empleado_crear_controller.route('/empleados/registrar', methods=['POST'])
def registrar_empleado():
    data = request.get_json()

    if not data:
        return jsonify({"codigo": 400, "error": "No se recibió información para registrar el empleado"}), 400

    return EmpleadocrearService.registrar_empleado(data)
