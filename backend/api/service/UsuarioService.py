# service/UsuarioService.py
from model import ClienteModel
from model import UsuarioModel

def registrar_usuario(data):
    usuario = data["usuario"]
    password = data["password"]
    email = data["email"]
    tipo_usuario = data["tipo_usuario"]
    nombre = data["nombre"]
    apellido = data["apellido"]
    telefono = data.get("telefono")
    rfc = data.get("rfc")
    direccion = data.get("direccion")

    if UsuarioModel.usuario_existe(usuario):
        return {"error": "El nombre de usuario ya está en uso"}, 400

    if UsuarioModel.email_existe(email):
        return {"error": "El email ya está registrado"}, 400

    id_usuario = UsuarioModel.insertar_usuario(usuario, password, email, tipo_usuario)

    if tipo_usuario == "CLIENTE":
        ClienteModel.insertar_cliente(id_usuario, nombre, apellido, telefono, rfc, direccion)

    return {"mensaje": "Usuario registrado con éxito", "id_usuario": id_usuario}, 201

def listar_usuarios():
    return UsuarioModel.obtener_usuarios()
