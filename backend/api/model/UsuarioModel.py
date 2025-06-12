# model/UsuarioModel.py
from util.Database import obtener_conexion
from flask import jsonify

def verificar_email_existe(email, cursor):
    cursor.execute("""
        SELECT COUNT(*)
        FROM usuarios
        WHERE email = :1
    """, (email,))
    count = cursor.fetchone()[0]
    return count > 0

def insertar_usuario(data):
    # Validar campos requeridos
    campos_requeridos = ['usuario', 'email', 'password', 'tipo_usuario']
    for campo in campos_requeridos:
        if campo not in data:
            return {"error": f"El campo {campo} es requerido"}, 400

    usuario = data.get("usuario")
    email = data.get("email")
    password = data.get("password")
    tipo_usuario = data.get("tipo_usuario")
    activo = data.get("activo", 'S')

    # Validar que activo sea 'S' o 'N'
    if activo not in ['S', 'N']:
        return {"error": "El campo activo solo puede ser 'S' o 'N'"}, 400

    # Validar tipo_usuario según los valores permitidos en la base de datos
    tipos_usuario_permitidos = ['CLIENTE', 'GERENTE_CUENTAS', 'GERENTE_EVENTOS', 'GERENTE_RH', 'ADMIN']
    if tipo_usuario not in tipos_usuario_permitidos:
        return {
            "error": f"Tipo de usuario no válido. Valores permitidos: {', '.join(tipos_usuario_permitidos)}"
        }, 400

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        # Verificar si el email ya existe
        if verificar_email_existe(email, cursor):
            return {"error": "El email ya está registrado"}, 409

        cursor.execute("""
            INSERT INTO usuarios (usuario, email, password, tipo_usuario, activo)
            VALUES (:1, :2, :3, :4, :5)
        """, (usuario, email, password, tipo_usuario, activo))

        conexion.commit()
        return {"mensaje": "Usuario creado correctamente"}, 201
    except Exception as e:
        conexion.rollback()
        return {"error": str(e)}, 500
    finally:
        cursor.close()
        conexion.close()

def obtener_usuarios():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_usuario, usuario, email, tipo_usuario, activo
        FROM usuarios
    """)

    usuarios = [
        {
            "id_usuario": row[0],
            "usuario": row[1],
            "email": row[2],
            "tipo_usuario": row[3],
            "activo": row[4]
        }
        for row in cursor.fetchall()
    ]

    cursor.close()
    conexion.close()
    return usuarios

def autenticar_usuario(usuario, password):
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
