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

@usuario_bp.route("/<int:id_usuario>", methods=["GET"])
def obtener_usuario(id_usuario):
    response, status = UsuarioService.obtener_detalle_usuario(id_usuario)
    return jsonify(response), status

@usuario_bp.route("/<int:id_usuario>", methods=["PUT"])
def actualizar_usuario(id_usuario):
    data = request.get_json(force=True)
    response, status = UsuarioService.actualizar_usuario(id_usuario, data)
    return jsonify(response), status

@usuario_bp.route("/<int:id_usuario>/password", methods=["PUT"])
def cambiar_password(id_usuario):
    data = request.get_json(force=True)
    response, status = UsuarioService.cambiar_password(id_usuario, data)
    return jsonify(response), status

@usuario_bp.route("/<int:id_usuario>", methods=["DELETE"])
def eliminar_usuario(id_usuario):
    response, status = UsuarioService.eliminar_usuario(id_usuario)
    return jsonify(response), status

@usuario_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True)
    response, status = UsuarioService.login(data)
    return jsonify(response), status
