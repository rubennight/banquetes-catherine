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

def obtener_usuario_por_id(id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = :1", [id_usuario])
    resultado = cursor.fetchone()
    
    if resultado:
        columnas = [col[0].lower() for col in cursor.description]
        return dict(zip(columnas, resultado))
    return None

def actualizar_usuario(id_usuario, usuario, email, tipo_usuario, activo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    cursor.execute("""
        UPDATE usuarios 
        SET usuario = :1, email = :2, tipo_usuario = :3, activo = :4 
        WHERE id_usuario = :5
    """, [usuario, email, tipo_usuario, activo, id_usuario])
    
    filas_afectadas = cursor.rowcount
    conexion.commit()
    return filas_afectadas > 0

def cambiar_password(id_usuario, nuevo_password):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    cursor.execute("""
        UPDATE usuarios 
        SET password = :1 
        WHERE id_usuario = :2
    """, [nuevo_password, id_usuario])
    
    filas_afectadas = cursor.rowcount
    conexion.commit()
    return filas_afectadas > 0

def eliminar_usuario(id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    cursor.execute("UPDATE usuarios SET activo = 'N' WHERE id_usuario = :1", [id_usuario])
    
    filas_afectadas = cursor.rowcount
    conexion.commit()
    return filas_afectadas > 0

def verificar_credenciales(usuario, password):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    cursor.execute("""
        SELECT id_usuario, tipo_usuario 
        FROM usuarios 
        WHERE usuario = :1 AND password = :2 AND activo = 'S'
    """, [usuario, password])
    
    resultado = cursor.fetchone()
    if resultado:
        return {"id_usuario": resultado[0], "tipo_usuario": resultado[1]}
    return None
