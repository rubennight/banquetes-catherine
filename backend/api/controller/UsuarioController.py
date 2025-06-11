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

    if not usuario or not password:
        return jsonify({"error": "Faltan credenciales", "codigo": 400}), 400

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_usuario, usuario, email, tipo_usuario, activo
        FROM usuarios
        WHERE usuario = :1 AND password = :2
    """, (usuario, password))

    fila = cursor.fetchone()
    cursor.close()
    conexion.close()

    if fila:
        return jsonify({
            "id_usuario": fila[0],
            "usuario": fila[1],
            "email": fila[2],
            "tipo_usuario": fila[3],
            "activo": fila[4]
        }), 200
    else:
        return jsonify({"error": "Usuario o contraseña incorrectos", "codigo": 401}), 401