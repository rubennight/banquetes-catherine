# model/UsuarioModel.py
from util.Database import obtener_conexion
from flask import jsonify
import re

class UsuarioModel:
    @staticmethod
    def validar_email(email):
        """Valida el formato del email"""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(patron, email))

    @staticmethod
    def validar_password(password):
        """Valida la fortaleza de la contraseña"""
        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres"
        if not re.search(r'[A-Z]', password):
            return False, "La contraseña debe contener al menos una mayúscula"
        if not re.search(r'[a-z]', password):
            return False, "La contraseña debe contener al menos una minúscula"
        if not re.search(r'\d', password):
            return False, "La contraseña debe contener al menos un número"
        return True, "Contraseña válida"

    @staticmethod
    def verificar_email_existe(email, cursor):
        cursor.execute("""
            SELECT COUNT(*)
            FROM usuarios
            WHERE email = :1
        """, (email,))
        count = cursor.fetchone()[0]
        return count > 0

    @staticmethod
    def verificar_usuario_existe(usuario, cursor):
        cursor.execute("""
            SELECT COUNT(*)
            FROM usuarios
            WHERE usuario = :1
        """, (usuario,))
        count = cursor.fetchone()[0]
        return count > 0

    @staticmethod
    def insertar_usuario(data):
        # Validar campos requeridos
        campos_requeridos = ['usuario', 'email', 'password', 'tipo_usuario']
        for campo in campos_requeridos:
            if campo not in data:
                return {"error": f"El campo {campo} es requerido"}, 400

        usuario = data.get("usuario")
        email = data.get("email")
        password = data.get("password")
        tipo_usuario = data.get("tipo_usuario")
        activo = data.get("activo", 'S')

        # Validar formato de email
        if not UsuarioModel.validar_email(email):
            return {"error": "Formato de email inválido"}, 400

        # Validar fortaleza de contraseña
        password_valida, mensaje = UsuarioModel.validar_password(password)
        if not password_valida:
            return {"error": mensaje}, 400

        # Validar que activo sea 'S' o 'N'
        if activo not in ['S', 'N']:
            return {"error": "El campo activo solo puede ser 'S' o 'N'"}, 400

        # Validar tipo_usuario según los valores permitidos
        tipos_usuario_permitidos = ['CLIENTE', 'GERENTE_CUENTAS', 'GERENTE_EVENTOS', 'GERENTE_RH', 'ADMIN']
        if tipo_usuario not in tipos_usuario_permitidos:
            return {
                "error": f"Tipo de usuario no válido. Valores permitidos: {', '.join(tipos_usuario_permitidos)}"
            }, 400

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            # Verificar si el email ya existe
            if UsuarioModel.verificar_email_existe(email, cursor):
                return {"error": "El email ya está registrado"}, 409

            # Verificar si el usuario ya existe
            if UsuarioModel.verificar_usuario_existe(usuario, cursor):
                return {"error": "El nombre de usuario ya está registrado"}, 409

            # Variable para almacenar el ID del usuario insertado
            new_id_usuario_var = cursor.var(int) # cx_Oracle.NUMBER can also be used if you import cx_Oracle

            cursor.execute("""
                INSERT INTO usuarios (usuario, email, password, tipo_usuario, activo)
                VALUES (:1, :2, :3, :4, :5)
                RETURNING id_usuario INTO :out_id_usuario
            """, (usuario, email, password, tipo_usuario, activo, new_id_usuario_var))
            
            inserted_id = new_id_usuario_var.getvalue()
            id_usuario_creado = inserted_id[0] if isinstance(inserted_id, list) else inserted_id


            conexion.commit()
            return {"mensaje": "Usuario creado correctamente", "id_usuario": id_usuario_creado}, 201
        except Exception as e:
            conexion.rollback()
            # Consider logging the full error e for debugging
            return {"error": "Error al insertar usuario: " + str(e)}, 500
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def obtener_usuarios():
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                SELECT id_usuario, usuario, email, tipo_usuario, activo
                FROM usuarios
            """)

            usuarios = [
                {
                    "id_usuario": row[0],
                    "usuario": row[1],
                    "email": row[2],
                    "tipo_usuario": row[3],
                    "activo": row[4]
                }
                for row in cursor.fetchall()
            ]

            return usuarios, 200
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def autenticar_usuario(usuario, password):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                SELECT id_usuario, usuario, email, tipo_usuario, activo
                FROM usuarios
                WHERE usuario = :1 AND password = :2 AND activo = 'S'
            """, (usuario, password))

            fila = cursor.fetchone()
            
            if fila:
                return {
                    "id_usuario": fila[0],
                    "usuario": fila[1],
                    "email": fila[2],
                    "tipo_usuario": fila[3],
                    "activo": fila[4]
                }, 200
            else:
                return {"error": "Usuario o contraseña incorrectos", "codigo": 401}, 401
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            cursor.close()
            conexion.close()
