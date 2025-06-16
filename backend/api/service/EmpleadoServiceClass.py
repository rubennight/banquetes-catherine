from model import EmpleadoModel


class EmpleadoService:

    @staticmethod
    def registrar_empleado(data):
        return EmpleadoModel.registrar_empleado(data)

