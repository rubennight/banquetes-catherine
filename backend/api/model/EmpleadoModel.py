from util.Database import obtener_conexion
from flask import jsonify
import oracledb

def empleados_por_evento(id_evento):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT e.id_empleado, e.nombre, e.apellido, e.puesto
        FROM evento_empleados ee
        JOIN empleados e ON ee.id_empleado = e.id_empleado
        WHERE ee.id_evento = :1
    """, (id_evento,))
    empleados = [
        {
            "idEmpleado": row[0],
            "nombre": row[1],
            "apellido": row[2],
            "puesto": row[3]
        } for row in cursor.fetchall()
    ]
    cursor.close()
    conexion.close()
    return empleados

def empleados_disponibles(fecha_evento, id_evento):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            SELECT id_empleado, nombre, apellido, puesto 
            FROM empleados 
            WHERE id_empleado NOT IN (
                SELECT id_empleado FROM evento_empleados ee
                JOIN eventos ev ON ee.id_evento = ev.id_evento
                WHERE ev.fecha_evento = :1
            )
        """, (fecha_evento,))
        return [
            {
                "idEmpleado": row[0],
                "nombre": row[1],
                "apellido": row[2],
                "puesto": row[3]
            } for row in cursor.fetchall()
        ]
    finally:
        cursor.close()
        conexion.close()

def registrar_empleado(data):
    print(' << A >>')
    try:
        usuario = data.get("usuario")
        print(' << B >>')
        password = data.get("password")
        print(' << C >>')
        email = data.get("email")
        print(' << D >>')
        tipo_usuario = data.get("tipo_usuario")  # 'GERENTE_EVENTOS', etc.
        print(' << E >>')
        nombre = data.get("nombre")
        print(' << F >>')
        apellido = data.get("apellido")
        print(' << G >>')
        puesto = data.get("puesto")
        print(' << H >>')
        tipo_contrato = data.get("tipo_contrato")  # 'TIEMPO_COMPLETO' o 'MEDIO_TIEMPO'
        print(' << I >>')
        print('ayuda')
        if not all([usuario, password, email, tipo_usuario, nombre, apellido, puesto, tipo_contrato]):
            return jsonify({"codigo": 400, "error": "Faltan datos obligatorios"}), 400

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Validar duplicado por USUARIO o EMAIL
        cursor.execute("""
            SELECT 1 FROM usuarios WHERE UPPER(usuario) = UPPER(:usuario) OR UPPER(email) = UPPER(:email)
        """, {
            "usuario": usuario,
            "email": email
        })

        print('ayuda2')
        if cursor.fetchone():
            return jsonify({"codigo": 409, "error": "Ya existe un usuario registrado con ese nombre de usuario o email"}), 409
        print(' << J >>')
        # Insertar en USUARIOS y obtener ID generado
        id_usuario_var = cursor.var(oracledb.NUMBER)
        print(' << K >>')
        cursor.execute("""
            INSERT INTO USUARIOS (USUARIO, PASSWORD, EMAIL, TIPO_USUARIO)
            VALUES (:usuario, :password, :email, :tipo_usuario)
            RETURNING id_usuario INTO :id_usuario
        """, {
            "usuario": usuario,
            "password": password,
            "email": email,
            "tipo_usuario": tipo_usuario,
            "id_usuario": id_usuario_var
        })
        print(' << L >>')
        id_usuario = int(id_usuario_var.getvalue()[0])
        print('\n\n >>>>>>>>>>>>>>>>>>>> id_usuario:', id_usuario)
        print(' << M >>')
        # Insertar en EMPLEADOS
        id_empleado_var = cursor.var(oracledb.NUMBER)
        print(' << N  >>')
        cursor.execute("""
            INSERT INTO EMPLEADOS (id_usuario, NOMBRE, APELLIDO, PUESTO, TIPO_CONTRATO)
            VALUES (:id_usuario, :nombre, :apellido, :puesto, :tipo_contrato)
            RETURNING ID_EMPLEADO INTO :id_empleado
        """, {
            "id_usuario": id_usuario,
            "nombre": nombre,
            "apellido": apellido,
            "puesto": puesto,
            "tipo_contrato": tipo_contrato,
            "id_empleado": id_empleado_var
        })
        
        print(' << O >>')
        
        id_empleado = int(id_empleado_var.getvalue()[0])
        print('ayuda3')
        if tipo_usuario == 'GERENTE_EVENTOS':
            # Insertar en GERENTES_EVENTOS
            cursor.execute("""
                INSERT INTO GERENTES (id_empleado,tipo_gerente, especialidad)
                VALUES (:id_empleado, :tipo_gerente, :especialidad)
            """, {
                "id_empleado": id_empleado,
                "tipo_gerente": "EVENTOS",
                "especialidad": "EVENTOS DE NIÑOS"                 
            })
        elif tipo_usuario == 'GERENTE_CUENTAS':
            print('ayudaNose que numero')
            # Insertar en GERENTES_CATERING
            cursor.execute("""
                INSERT INTO GERENTES (id_empleado,tipo_gerente, especialidad)
                VALUES (:id_empleado, :tipo_gerente, :especialidad)
            """, {
                "id_empleado": id_empleado,
                "tipo_gerente": "CUENTAS",
                "especialidad": "CUENTAS DE EVENTOS"
            })
        elif tipo_usuario == 'GERENTE_RH':
            print('ayuda4')
            # Insertar en GERENTES_RH
            cursor.execute("""
                INSERT INTO GERENTES (id_empleado,tipo_gerente, especialidad)
                VALUES (:id_empleado, :tipo_gerente, :especialidad)
            """, {
                "id_empleado": id_empleado,
                "tipo_gerente": "RH",
                "especialidad": "recursos humanos head hunting"
            })
            
        print('BEFORE COMMIT')
        conexion.commit()
        print('AFTER COMMIT')
        cursor.close()
        conexion.close()

        return jsonify({"codigo": 201, "mensaje": "Empleado registrado exitosamente", "id_usuario": id_usuario}), 201

    except Exception as e:
        print(f"Error al registrar empleado: {str(e)}")
        if conexion:
            conexion.rollback()
        return jsonify({"codigo": 500, "error": f"Error interno del servidor al registrar empleado: {str(e)}"}), 500

