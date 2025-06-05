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

def obtener_detalle_usuario(id_usuario):
    usuario = UsuarioModel.obtener_usuario_por_id(id_usuario)
    if usuario:
        return usuario, 200
    return {"error": "Usuario no encontrado"}, 404

def actualizar_usuario(id_usuario, data):
    usuario_actual = UsuarioModel.obtener_usuario_por_id(id_usuario)
    
    if not usuario_actual:
        return {"error": "Usuario no encontrado"}, 404
    
    # Verificar si el nuevo nombre de usuario ya existe
    if "usuario" in data and data["usuario"] != usuario_actual["usuario"]:
        if UsuarioModel.usuario_existe(data["usuario"]):
            return {"error": "El nombre de usuario ya está en uso"}, 400
    
    # Verificar si el nuevo email ya existe
    if "email" in data and data["email"] != usuario_actual["email"]:
        if UsuarioModel.email_existe(data["email"]):
            return {"error": "El email ya está registrado"}, 400
    
    # Actualizar usuario
    usuario = data.get("usuario", usuario_actual["usuario"])
    email = data.get("email", usuario_actual["email"])
    tipo_usuario = data.get("tipo_usuario", usuario_actual["tipo_usuario"])
    activo = data.get("activo", usuario_actual["activo"])
    
    actualizado = UsuarioModel.actualizar_usuario(id_usuario, usuario, email, tipo_usuario, activo)
    
    if actualizado:
        return {"mensaje": "Usuario actualizado con éxito"}, 200
    return {"error": "Error al actualizar el usuario"}, 500

def cambiar_password(id_usuario, data):
    if "password" not in data:
        return {"error": "La contraseña es requerida"}, 400
    
    usuario = UsuarioModel.obtener_usuario_por_id(id_usuario)
    
    if not usuario:
        return {"error": "Usuario no encontrado"}, 404
    
    actualizado = UsuarioModel.cambiar_password(id_usuario, data["password"])
    
    if actualizado:
        return {"mensaje": "Contraseña actualizada con éxito"}, 200
    return {"error": "Error al actualizar la contraseña"}, 500

def eliminar_usuario(id_usuario):
    usuario = UsuarioModel.obtener_usuario_por_id(id_usuario)
    
    if not usuario:
        return {"error": "Usuario no encontrado"}, 404
    
    eliminado = UsuarioModel.eliminar_usuario(id_usuario)
    
    if eliminado:
        return {"mensaje": "Usuario desactivado con éxito"}, 200
    return {"error": "Error al desactivar el usuario"}, 500

def login(data):
    if "usuario" not in data or "password" not in data:
        return {"error": "Usuario y contraseña son requeridos"}, 400
    
    usuario = data["usuario"]
    password = data["password"]
    
    resultado = UsuarioModel.verificar_credenciales(usuario, password)
    
    if resultado:
        return {
            "mensaje": "Inicio de sesión exitoso",
            "id_usuario": resultado["id_usuario"],
            "tipo_usuario": resultado["tipo_usuario"]
        }, 200
    
    return {"error": "Credenciales inválidas"}, 401