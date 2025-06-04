# controller/UsuarioController.py
from flask import Blueprint, request, jsonify
from service import UsuarioService

usuario_bp = Blueprint("usuario_bp", __name__, url_prefix="/usuarios")

@usuario_bp.route("", methods=["POST"])
def crear_usuario():
    data = request.get_json(force=True)
    response, status = UsuarioService.registrar_usuario(data)
    return jsonify(response), status

@usuario_bp.route("", methods=["GET"])
def listar_usuarios():
    usuarios = UsuarioService.listar_usuarios()
    return jsonify(usuarios), 200
