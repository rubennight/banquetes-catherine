# model/UsuarioModel.py
from util.Database import obtener_conexion

import oracledb;

def insertar_usuario(usuario, password, email, tipo_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    id_usuario_var = cursor.var(oracledb.NUMBER)

    cursor.execute("""
        INSERT INTO usuarios (usuario, password, email, tipo_usuario)
        VALUES (:1, :2, :3, :4)
        RETURNING id_usuario INTO :5
    """, [usuario, password, email, tipo_usuario, id_usuario_var])
    
    conexion.commit()
    return id_usuario_var.getvalue()[0]

def usuario_existe(usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE usuario = :1", [usuario])
    return cursor.fetchone()[0] > 0

def email_existe(email):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE email = :1", [email])
    return cursor.fetchone()[0] > 0

def obtener_usuarios():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios")
    columnas = [col[0].lower() for col in cursor.description]
    return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
