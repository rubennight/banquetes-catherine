import oracledb
from util.Database import obtener_conexion

class ClienteModel:
    @staticmethod
    def insertar_cliente(data):
        campos_requeridos = ['usuario', 'password', 'email','nombre', 'apellido']
        for campo in campos_requeridos:
            if campo not in data or data[campo] is None: 
                return {"error": f"El campo '{campo}' es requerido"}, 400

        usuario = data.get("usuario")
        password = data.get("password")
        email = data.get("email")
        nombre = data.get("nombre")
        apellido = data.get("apellido")
        telefono = data.get("telefono") 
        rfc = data.get("rfc")           
        direccion = data.get("direccion") 

        conexion = None
        cursor = None
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            
            cursor.execute("""
                SELECT 1 FROM USUARIOS WHERE USUARIO = :usuario OR EMAIL = :email
            """, {
                "usuario": usuario,
                "email": email
            })

            
            
            if rfc:
                cursor.execute("SELECT COUNT(*) FROM clientes WHERE rfc = :1", (rfc,))
                if cursor.fetchone()[0] > 0:
                    return {"error": f"El RFC '{rfc}' ya está registrado."}, 409
                
            id_usuario_var = cursor.var(oracledb.NUMBER)

            cursor.execute("""
                INSERT INTO USUARIOS (USUARIO, PASSWORD, EMAIL, TIPO_USUARIO)
                VALUES (:usuario, :password, :email, :tipo_usuario)
                RETURNING ID_USUARIO INTO :id_usuario
            """, {
                "usuario": usuario,
                "password": password,
                "email": email,
                "tipo_usuario": "CLIENTE",  
                "id_usuario": id_usuario_var
            })

            id_usuario = int(id_usuario_var.getvalue()[0])

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