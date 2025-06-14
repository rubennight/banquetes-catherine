from flask import jsonify
from model.UsuarioModel import UsuarioModel

class UsuarioService:

    @staticmethod
    def registrar_usuario(data):
        """
        Registra un nuevo usuario en el sistema
        """
        try:
            response, status = UsuarioModel.insertar_usuario(data)
            return jsonify(response), status
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def listar_usuarios():
        """
        Obtiene la lista de todos los usuarios
        """
        try:
            usuarios, status = UsuarioModel.obtener_usuarios()
            return jsonify(usuarios), status
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def login(usuario, password):
        """
        Autentica un usuario en el sistema
        """
        if not usuario or not password:
            return jsonify({"error": "Faltan credenciales", "codigo": 400}), 400

        try:
            response, status = UsuarioModel.autenticar_usuario(usuario, password)
            return jsonify(response), status
        except Exception as e:
            return jsonify({"error": str(e)}), 500
