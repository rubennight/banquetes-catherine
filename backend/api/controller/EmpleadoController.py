from flask import Blueprint, request, jsonify
from util.Database import obtener_conexion
from datetime import datetime
from service.EventoEmpleadoService import EventoEmpleadoService

empleado_controller = Blueprint('empleado_controller', __name__)


@empleado_controller.route('/empleados/porEvento', methods=['GET'])
def obtener_empleados_por_evento():
    id_evento = request.args.get('idEvento')

    if not id_evento:
        return jsonify({"error": "Falta el parámetro idEvento", "codigo": 400}), 400

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Validar si el evento existe
    cursor.execute(
        "SELECT COUNT(*) FROM eventos WHERE id_evento = :1", (id_evento,))
    if cursor.fetchone()[0] == 0:
        cursor.close()
        conexion.close()
        return jsonify({"error": "Evento no existe", "codigo": 404}), 404

    # Obtener empleados asignados
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

    return jsonify({
        "idEvento": int(id_evento),
        "empleados": empleados
    }), 200

@empleado_controller.route('/empleados/porDisponibilidad', methods=['GET'])
def obtener_empleados_por_disponibilidad():
    id_evento = request.args.get('idEvento')

    if not id_evento:
        return jsonify({"error": "Falta el parámetro idEvento", "codigo": 400}), 400

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        # Validar si el evento existe y obtener su fecha
        cursor.execute("SELECT fecha_evento FROM eventos WHERE id_evento = :1", (id_evento,))
        evento = cursor.fetchone()
        if not evento:
            return jsonify({"error": "Evento no existe", "codigo": 404}), 404

        fecha_evento = evento[0]
        
        # Usar el servicio para obtener empleados disponibles
        empleados = EventoEmpleadoService.obtener_empleados_disponibles(fecha_evento, id_evento)
        
        return jsonify(empleados), 200
        
    except Exception as e:
        return jsonify({"error": f"Error al obtener empleados disponibles: {str(e)}", "codigo": 500}), 500
    finally:
        cursor.close()
        conexion.close()