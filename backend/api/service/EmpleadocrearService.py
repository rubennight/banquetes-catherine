from model.EmpleadocrearModel import EmpleadocrearModel

class EmpleadocrearService:

    @staticmethod
    def registrar_empleado(data):
        return EmpleadocrearModel.registrar_empleado(data)
