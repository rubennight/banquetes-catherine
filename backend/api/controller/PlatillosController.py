# controller/UsuarioController.py
from flask import Blueprint, request, jsonify
from service.PlatillosService import PlatillosService

# Crear el Blueprint para las rutas de usuario
platillo_bp = Blueprint("platillo_bp", __name__, url_prefix="/platillos")

@platillo_bp.route("", methods=["GET"])
def listar_platillos():
    try:
        resultados = PlatillosService.listar_platillos()

        platillos_json = [
            {
                "id_platillo": r[0],
                "descripcion": r[1],
                "tipo_platillo": r[2],
                "precio_100_personas": r[3],
                "url_imagen": r[4]
            }
            for r in resultados
        ]

        return jsonify(platillos_json)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
