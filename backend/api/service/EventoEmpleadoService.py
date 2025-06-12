from flask import jsonify
from model.EventoModel import evento_existe, obtener_fecha_evento
from model.EmpleadoModel import empleados_por_evento, empleados_disponibles
from util.Database import obtener_conexion

class EventoEmpleadoService:

    @staticmethod
    def obtener_empleados_por_evento(id_evento):
        if not evento_existe(id_evento):
            return jsonify({"error": "Evento no existe", "codigo": 404}), 404

        empleados = empleados_por_evento(id_evento)

        return jsonify({
            "idEvento": int(id_evento),
            "empleados": empleados
        }), 200

    @staticmethod
    def obtener_empleados_disponibles_por_evento(id_evento):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            fecha_evento = obtener_fecha_evento(cursor, id_evento)
            if not fecha_evento:
                return jsonify({"error": "Evento no existe", "codigo": 404}), 404

            disponibles = empleados_disponibles(cursor, fecha_evento, id_evento)
            return jsonify(disponibles), 200

        except Exception as e:
            return jsonify({"error": f"Error al obtener empleados disponibles: {str(e)}", "codigo": 500}), 500
        finally:
            cursor.close()
            conexion.close()