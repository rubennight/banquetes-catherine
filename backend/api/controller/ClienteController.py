from flask import Blueprint, request, jsonify
from service.ClienteService import ClienteService

# Crear el Blueprint para las rutas de cliente
cliente_bp = Blueprint("cliente_bp", __name__, url_prefix="/clientes")

@cliente_bp.route("/registrar", methods=["POST"])
def crear_cliente():
    """
    Endpoint para crear un nuevo cliente.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Cuerpo del request vacío o no es JSON válido"}), 400
        
        return ClienteService.registrar_cliente(data)
    except Exception as e:
        return jsonify({"error": f"Error en el controlador al crear cliente: {str(e)}"}), 500