
from flask import Blueprint, request, jsonify
from service.CrearPlatilloService import CrearPlatilloService

crear_platillo_controller = Blueprint('crear_platillo_controller', __name__)

@crear_platillo_controller.route('/platillos/crear', methods=['POST'])
def registrar_platillo():
    data = request.get_json()

    if not data:
        return jsonify({"codigo": 400, "error": "No se recibió información para registrar el platillo"}), 400

    return CrearPlatilloService.registrar_platillo(data)
