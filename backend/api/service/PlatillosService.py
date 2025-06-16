from flask import jsonify
from model.PlatilloModel import listar_platillos

class PlatillosService:

    @staticmethod
    def listar_platillos():
        """
        Obtiene la lista de todos los platillos
        """
        try:
            platillos, status = listar_platillos()
            return jsonify(platillos), status
        except Exception as e:
            return jsonify({"error": str(e)}), 500

