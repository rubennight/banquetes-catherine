from flask import jsonify
from model.EventoModel import (
    asignar_empleados_model,
    listar_eventos_model,
    buscar_eventos_por_fecha_model,
    registrar_evento_model
)

class EventoService:

    @staticmethod
    def asignar_empleados_evento(data):
        return asignar_empleados_model(data)

    @staticmethod
    def listar_eventos():
        return listar_eventos_model()

    @staticmethod
    def buscar_eventos_por_fecha(fecha_str):
        return buscar_eventos_por_fecha_model(fecha_str)

    @staticmethod
    def registrar_evento(data):
        # Validar que data sea un diccionario
        if not isinstance(data, dict):
            return jsonify({"error": "Formato de datos inválido", "codigo": 400}), 400
            
        # Validar campos requeridos
        campos_requeridos = ["fechaEvento", "tipoEvento", "descripcion", "idUsuario", "menu"]
        faltantes = [campo for campo in campos_requeridos if campo not in data]
        if faltantes:
            return jsonify({"error": f"Campos faltantes: {faltantes}", "codigo": 400}), 400
            
        try:
            return registrar_evento_model(data)
        except Exception as e:
            print(f"Error en registrar_evento_service: {str(e)}")
            return jsonify({"error": str(e), "codigo": 500}), 500
