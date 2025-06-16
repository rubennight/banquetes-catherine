from util.Database import obtener_conexion

class ClienteModel:
    @staticmethod
    def insertar_cliente(data):
        campos_requeridos = ['id_usuario', 'nombre', 'apellido']
        for campo in campos_requeridos:
            if campo not in data or data[campo] is None: # Check for presence and not None
                return {"error": f"El campo '{campo}' es requerido"}, 400

        id_usuario = data.get("id_usuario")
        nombre = data.get("nombre")
        apellido = data.get("apellido")
        telefono = data.get("telefono") # Optional
        rfc = data.get("rfc")           # Optional, but unique if provided
        direccion = data.get("direccion") # Optional

        conexion = None
        cursor = None
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            cursor.execute("SELECT COUNT(*) FROM usuarios WHERE id_usuario = :1", (id_usuario,))
            if cursor.fetchone()[0] == 0:
                return {"error": f"El id_usuario '{id_usuario}' no existe."}, 404

            cursor.execute("SELECT COUNT(*) FROM clientes WHERE id_usuario = :1", (id_usuario,))
            if cursor.fetchone()[0] > 0:
                return {"error": f"El id_usuario '{id_usuario}' ya está asociado a un cliente."}, 409
            
            if rfc:
                cursor.execute("SELECT COUNT(*) FROM clientes WHERE rfc = :1", (rfc,))
                if cursor.fetchone()[0] > 0:
                    return {"error": f"El RFC '{rfc}' ya está registrado."}, 409

            new_id_cliente_var = cursor.var(int)

            cursor.execute("""
                INSERT INTO clientes (id_usuario, nombre, apellido, telefono, rfc, direccion)
                VALUES (:id_usuario, :nombre, :apellido, :telefono, :rfc, :direccion)
                RETURNING id_cliente INTO :out_id_cliente
            """, {
                "id_usuario": id_usuario,
                "nombre": nombre,
                "apellido": apellido,
                "telefono": telefono,
                "rfc": rfc,
                "direccion": direccion,
                "out_id_cliente": new_id_cliente_var
            })
            
            inserted_id = new_id_cliente_var.getvalue()
            id_cliente_creado = inserted_id[0] if isinstance(inserted_id, list) else inserted_id

            conexion.commit()
            return {"mensaje": "Cliente creado correctamente", "id_cliente": id_cliente_creado}, 201

        except Exception as e: 
            if conexion:
                conexion.rollback()
            error_message = f"Error al insertar cliente: {str(e)}"
        
            if hasattr(e, 'args') and e.args and hasattr(e.args[0], 'code') and e.args[0].code == 1:
                if rfc and rfc in str(e).upper(): 
                     error_message = f"El RFC '{rfc}' ya está registrado (ORA-00001)."
                elif id_usuario and str(id_usuario) in str(e): 
                     error_message = f"El id_usuario '{id_usuario}' ya está asociado a un cliente (ORA-00001)."


            return {"error": error_message}, 500
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()