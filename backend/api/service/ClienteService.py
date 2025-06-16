from flask import jsonify
from model.ClienteModel import ClienteModel

class ClienteService:

    @staticmethod
    def registrar_cliente(data):
        """
        Registra un nuevo cliente en el sistema.
        Espera que 'data' contenga 'id_usuario', 'nombre', 'apellido',
        y opcionalmente 'telefono', 'rfc', 'direccion'.
        """
        try:
            if not data:
                return jsonify({"error": "No se proporcionaron datos"}), 400
            
            response, status = ClienteModel.insertar_cliente(data)
            return jsonify(response), status
        except Exception as e:
   
            return jsonify({"error": f"Error en el servicio al registrar cliente: {str(e)}"}), 500