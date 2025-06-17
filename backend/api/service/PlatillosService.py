from flask import jsonify
from model.PlatilloModel import listar_platillos

class PlatillosService:

    @staticmethod
    def listar_platillos():
        """
        Obtiene la lista de todos los platillos
        """
        try:
            platillos = listar_platillos()  
            return platillos 
        except Exception as e:
            raise e 

