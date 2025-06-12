from util.Database import obtener_conexion

def empleados_por_evento(id_evento):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT e.id_empleado, e.nombre, e.apellido, e.puesto
        FROM evento_empleados ee
        JOIN empleados e ON ee.id_empleado = e.id_empleado
        WHERE ee.id_evento = :1
    """, (id_evento,))
    empleados = [
        {
            "idEmpleado": row[0],
            "nombre": row[1],
            "apellido": row[2],
            "puesto": row[3]
        } for row in cursor.fetchall()
    ]
    cursor.close()
    conexion.close()
    return empleados

def empleados_disponibles(cursor, fecha_evento, id_evento):
    cursor.execute("""
        SELECT id_empleado, nombre, apellido, puesto 
        FROM empleados 
        WHERE id_empleado NOT IN (
            SELECT id_empleado FROM evento_empleados ee
            JOIN eventos ev ON ee.id_evento = ev.id_evento
            WHERE ev.fecha_evento = :1
        )
    """, (fecha_evento,))
    return [
        {
            "idEmpleado": row[0],
            "nombre": row[1],
            "apellido": row[2],
            "puesto": row[3]
        } for row in cursor.fetchall()
    ]