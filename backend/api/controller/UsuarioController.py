# controller/UsuarioController.py
from flask import Blueprint, request, jsonify
from service.UsuarioService import UsuarioService

# Crear el Blueprint para las rutas de usuario
usuario_bp = Blueprint("usuario_bp", __name__, url_prefix="/usuarios")

@usuario_bp.route("", methods=["POST"])
def crear_usuario():
    """
    Endpoint para crear un nuevo usuario
    """
    try:
        data = request.get_json(force=True)
        return UsuarioService.registrar_usuario(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@usuario_bp.route("", methods=["GET"])
def listar_usuarios():
    """
    Endpoint para listar todos los usuarios
    """
    try:
        return UsuarioService.listar_usuarios()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@usuario_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint para autenticar un usuario
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se proporcionaron datos", "codigo": 400}), 400

        usuario = data.get('usuario')
        password = data.get('password')
        return UsuarioService.login(usuario, password)
    except Exception as e:
        return jsonify({"error": str(e)}), 500