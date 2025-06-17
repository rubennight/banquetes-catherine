
from util.Database import obtener_conexion
from flask import jsonify
import oracledb

class CrearPlatilloModel:

    @staticmethod
    def registrar_platillo(data):
        try:
            descripcion = data.get("descripcion")
            tipo_platillo = data.get("tipo_platillo")
            precio_100_personas = data.get("precio_100_personas")
            url_imagen = data.get("url_imagen")
            ingredientes = data.get("ingredientes", [])

            if not all([descripcion, tipo_platillo, precio_100_personas, url_imagen]) or not ingredientes:
                return jsonify({"codigo": 400, "error": "Faltan datos obligatorios o no se proporcionaron ingredientes"}), 400

            # Validar ingredientes duplicados
            ids_ingredientes = [i["id_ingrediente"] for i in ingredientes]
            if len(ids_ingredientes) != len(set(ids_ingredientes)):
                return jsonify({"codigo": 400, "error": "Hay ingredientes duplicados en la lista"}), 400

            # Validar pasos duplicados
            pasos = [i["paso"] for i in ingredientes if "paso" in i]
            if len(pasos) != len(set(pasos)):
                return jsonify({"codigo": 400, "error": "Hay pasos duplicados en la lista de ingredientes"}), 400

            conexion = obtener_conexion()
            cursor = conexion.cursor()

            # Validar que todos los ingredientes existan
            for ing in ids_ingredientes:
                cursor.execute("SELECT 1 FROM INGREDIENTES WHERE ID_INGREDIENTE = :id", {"id": ing})
                if not cursor.fetchone():
                    return jsonify({"codigo": 400, "error": f"El ingrediente con ID {ing} no existe"}), 400

            # Insertar en PLATILLOS (ID generado por trigger)
            id_platillo_var = cursor.var(oracledb.NUMBER)
            cursor.execute("""
                INSERT INTO PLATILLOS (DESCRIPCION, TIPO_PLATILLO, PRECIO_100_PERSONAS, URL_IMAGEN)
                VALUES (:descripcion, :tipo_platillo, :precio, :imagen)
                RETURNING ID_PLATILLO INTO :id
            """, {
                "descripcion": descripcion,
                "tipo_platillo": tipo_platillo,
                "precio": precio_100_personas,
                "imagen": url_imagen,
                "id": id_platillo_var
            })

            id_platillo = int(id_platillo_var.getvalue()[0])

            # Insertar ingredientes en PLATILLO_INGREDIENTE
            for ing in ingredientes:
                cursor.execute("""
                    INSERT INTO PLATILLO_INGREDIENTE (ID_PLATILLO, ID_INGREDIENTE, PASO, CANTIDAD, MODO_PREPARACION)
                    VALUES (:id_platillo, :id_ingrediente, :paso, :cantidad, :modo)
                """, {
                    "id_platillo": id_platillo,
                    "id_ingrediente": ing["id_ingrediente"],
                    "paso": ing["paso"],
                    "cantidad": ing["cantidad"],
                    "modo": ing["modo_preparacion"]
                })

            conexion.commit()
            cursor.close()
            conexion.close()

            return jsonify({"codigo": 201, "mensaje": "Platillo creado exitosamente", "id_platillo": id_platillo}), 201

        except Exception as e:
            return jsonify({"codigo": 500, "error": f"Error interno del servidor al registrar platillo: {str(e)}"}), 500
