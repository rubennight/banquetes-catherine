# controller/UsuarioController.py
from flask import Blueprint, request, jsonify
from service.PlatillosService import PlatillosService

# Crear el Blueprint para las rutas de usuario
platillo_bp = Blueprint("platillo_bp", __name__, url_prefix="/platillos")

@platillo_bp.route("", methods=["GET"])
def listar_platillos():
    try:
        resultado = PlatillosService.listar_platillos()
        return jsonify(resultado)  # ✅ Esto ya es una lista de dicts
    except Exception as e:
        return jsonify({"error": str(e)}), 500

