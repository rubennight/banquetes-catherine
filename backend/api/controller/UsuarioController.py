# controller/UsuarioController.py
from flask import Blueprint, request, jsonify
from service import UsuarioService
from util.Database import obtener_conexion

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

@usuario_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = data.get('usuario')
    password = data.get('password')
    return UsuarioService.login(usuario, password)