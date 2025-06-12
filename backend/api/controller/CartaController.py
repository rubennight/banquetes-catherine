from flask import Blueprint, jsonify
from util.Database import obtener_conexion
from service.CartaService import obtener_info_carta_service

carta_controller = Blueprint('carta_controller', __name__)

@carta_controller.route('/usuarios/infoCarta', methods=['GET'])
def obtener_info_carta():
    resultado = obtener_info_carta_service()
    return jsonify(resultado), 200
