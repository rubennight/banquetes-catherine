from util.Database import obtener_conexion
from flask import jsonify
import oracledb

class EmpleadocrearModel:

    @staticmethod
    def registrar_empleado(data):
        try:
            usuario = data.get("usuario")
            password = data.get("password")
            email = data.get("email")
            tipo_usuario = data.get("tipo_usuario")  # 'GERENTE_EVENTOS', etc.
            nombre = data.get("nombre")
            apellido = data.get("apellido")
            puesto = data.get("puesto")
            tipo_contrato = data.get("tipo_contrato")  # 'TIEMPO_COMPLETO' o 'MEDIO_TIEMPO'

            if not all([usuario, password, email, tipo_usuario, nombre, apellido, puesto, tipo_contrato]):
                return jsonify({"codigo": 400, "error": "Faltan datos obligatorios"}), 400

            conexion = obtener_conexion()
            cursor = conexion.cursor()

            # Validar duplicado por USUARIO o EMAIL
            cursor.execute("""
                SELECT 1 FROM USUARIOS WHERE USUARIO = :usuario OR EMAIL = :email
            """, {
                "usuario": usuario,
                "email": email
            })

            if cursor.fetchone():
                return jsonify({"codigo": 409, "error": "Ya existe un usuario registrado con ese nombre de usuario o email"}), 409

            # Insertar en USUARIOS y obtener ID generado
            id_usuario_var = cursor.var(oracledb.NUMBER)

            cursor.execute("""
                INSERT INTO USUARIOS (USUARIO, PASSWORD, EMAIL, TIPO_USUARIO)
                VALUES (:usuario, :password, :email, :tipo_usuario)
                RETURNING ID_USUARIO INTO :id_usuario
            """, {
                "usuario": usuario,
                "password": password,
                "email": email,
                "tipo_usuario": tipo_usuario,
                "id_usuario": id_usuario_var
            })

            id_usuario = int(id_usuario_var.getvalue()[0])

            # Insertar en EMPLEADOS
            cursor.execute("""
                INSERT INTO EMPLEADOS (ID_USUARIO, NOMBRE, APELLIDO, PUESTO, TIPO_CONTRATO)
                VALUES (:id_usuario, :nombre, :apellido, :puesto, :tipo_contrato)
            """, {
                "id_usuario": id_usuario,
                "nombre": nombre,
                "apellido": apellido,
                "puesto": puesto,
                "tipo_contrato": tipo_contrato
            })

            conexion.commit()
            cursor.close()
            conexion.close()

            return jsonify({"codigo": 201, "mensaje": "Empleado registrado exitosamente", "id_usuario": id_usuario}), 201

        except Exception as e:
            return jsonify({"codigo": 500, "error": f"Error interno del servidor al registrar empleado: {str(e)}"}), 500
