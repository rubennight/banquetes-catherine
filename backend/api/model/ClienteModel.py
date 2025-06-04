from util.Database import obtener_conexion

import oracledb;

def insertar_cliente(id_usuario, nombre, apellido, telefono, rfc, direccion):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO clientes (id_usuario, nombre, apellido, telefono, rfc, direccion)
        VALUES (:1, :2, :3, :4, :5, :6)
    """, (id_usuario, nombre, apellido, telefono, rfc, direccion))
    conexion.commit()