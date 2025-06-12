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
        return registrar_evento_model(data)
