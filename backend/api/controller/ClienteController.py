from flask import Blueprint, request, jsonify
from service.ClienteService import ClienteService

# Crear el Blueprint para las rutas de cliente
cliente_bp = Blueprint("cliente_bp", __name__, url_prefix="/clientes")

@cliente_bp.route("", methods=["POST"])
def crear_cliente():
    """
    Endpoint para crear un nuevo cliente.
    El cuerpo del request debe ser un JSON con:
    - id_usuario (int, obligatorio): ID del usuario existente.
    - nombre (str, obligatorio): Nombre del cliente.
    - apellido (str, obligatorio): Apellido del cliente.
    - telefono (str, opcional): Teléfono del cliente.
    - rfc (str, opcional): RFC del cliente (debe ser único si se provee).
    - direccion (str, opcional): Dirección del cliente.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Cuerpo del request vacío o no es JSON válido"}), 400
        
        return ClienteService.registrar_cliente(data)
    except Exception as e:
        return jsonify({"error": f"Error en el controlador al crear cliente: {str(e)}"}), 500