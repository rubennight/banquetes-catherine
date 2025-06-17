
from model.CrearPlatilloModel import CrearPlatilloModel

class CrearPlatilloService:

    @staticmethod
    def registrar_platillo(data):
        return CrearPlatilloModel.registrar_platillo(data)
