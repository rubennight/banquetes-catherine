# controller/UsuarioController.py
from flask import Blueprint, request, jsonify
from service.PlatillosService import PlatillosService

# Crear el Blueprint para las rutas de usuario
platillo_bp = Blueprint("platillo_controller", __name__, url_prefix="/platillos")

@platillo_bp.route("", methods=["GET"])
def listar_platillos():
    """
    Endpoint para listar todos los usuarios
    """
    try:
        return PlatillosService.listar_platillos()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
