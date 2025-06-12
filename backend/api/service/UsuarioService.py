from flask import jsonify
from model.UsuarioModel import insertar_usuario, obtener_usuarios, autenticar_usuario

class UsuarioService:

    @staticmethod
    def registrar_usuario(data):
        return insertar_usuario(data)

    @staticmethod
    def listar_usuarios():
        return obtener_usuarios()

    @staticmethod
    def login(usuario, password):
        if not usuario or not password:
            return jsonify({"error": "Faltan credenciales", "codigo": 400}), 400

        return autenticar_usuario(usuario, password)
