from util.Database import obtener_conexion
from flask import jsonify
from datetime import datetime
import oracledb

def evento_existe(id_evento):
    """
    Verifica si existe un evento con el ID especificado
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT 1 FROM eventos WHERE id_evento = :1", (id_evento,))
        return cursor.fetchone() is not None
    finally:
        cursor.close()
        conexion.close()

def obtener_fecha_evento(id_evento):
    """
    Obtiene la fecha de un evento específico
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT fecha_evento FROM eventos WHERE id_evento = :1", (id_evento,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    finally:
        cursor.close()
        conexion.close()

def asignar_empleados_model(data):
    id_evento = data.get('id_evento')
    empleados = data.get('empleados')

    if not id_evento or not empleados:
        return jsonify({"error": "Faltan datos", "codigo": 400}), 400

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT fecha_evento FROM eventos WHERE id_evento = :1", (id_evento,))
    evento_row = cursor.fetchone()
    if not evento_row:
        cursor.close()
        conexion.close()
        return jsonify({"error": "Evento no encontrado", "codigo": 404}), 404

    fecha_evento = evento_row[0]
    empleados_asignados = 0

    for id_empleado in empleados:
        cursor.execute("""
            SELECT COUNT(*)
            FROM evento_empleados ee
            JOIN eventos e ON ee.id_evento = e.id_evento
            WHERE ee.id_empleado = :1 AND TRUNC(e.fecha_evento) = TRUNC(:2)
        """, (id_empleado, fecha_evento))
        ya_ocupado = cursor.fetchone()[0]

        if ya_ocupado == 0:
            cursor.execute("""
                INSERT INTO evento_empleados (id_evento, id_empleado)
                VALUES (:1, :2)
            """, (id_evento, id_empleado))
            empleados_asignados += 1

    conexion.commit()
    cursor.close()
    conexion.close()

    return jsonify({"mensaje": f"{empleados_asignados} empleados asignados correctamente"}), 200


def listar_eventos_model():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT e.id_evento, e.fecha_evento, e.tipo_evento, e.descripcion, e.total_precio,
               m.nombre, m.descripcion, m.precio
        FROM eventos e
        LEFT JOIN evento_menu em ON e.id_evento = em.id_evento
        LEFT JOIN menus m ON em.id_menu = m.id_menu
    """)
    eventos_raw = cursor.fetchall()

    eventos = []

    for row in eventos_raw:
        id_evento = row[0]

        cursor.execute("""
            SELECT emp.id_empleado, emp.nombre, emp.apellido, emp.puesto
            FROM evento_empleados ee
            JOIN empleados emp ON ee.id_empleado = emp.id_empleado
            WHERE ee.id_evento = :1
        """, (id_evento,))
        empleados = [
            {
                "idEmpleado": emp[0],
                "nombre": emp[1],
                "apellido": emp[2],
                "puesto": emp[3]
            }
            for emp in cursor.fetchall()
        ]

        eventos.append({
            "idEvento": row[0],
            "fechaEvento": row[1].strftime("%d-%m-%Y %H:%M:%S"),
            "tipoEvento": row[2],
            "descripcion": row[3],
            "totalPrecio": row[4],
            "menu": {
                "nombreMenu": row[5],
                "descripcionMenu": row[6],
                "precioMenu": row[7]
            } if row[5] else None,
            "empleados": empleados
        })

    cursor.close()
    conexion.close()

    return jsonify({"eventos": eventos}), 200


def buscar_eventos_por_fecha_model(fecha_str):
    if not fecha_str:
        return jsonify({"error": "Parámetro 'fecha' es obligatorio", "codigo": 400}), 400

    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD", "codigo": 400}), 400

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT e.id_evento, e.fecha_evento, e.tipo_evento, e.descripcion, e.total_precio,
               m.nombre, m.descripcion, m.precio
        FROM eventos e
        LEFT JOIN evento_menu em ON e.id_evento = em.id_evento
        LEFT JOIN menus m ON em.id_menu = m.id_menu
        WHERE TRUNC(e.fecha_evento) = TRUNC(:1)
    """, (fecha,))
    eventos_raw = cursor.fetchall()

    eventos = []

    for row in eventos_raw:
        id_evento = row[0]

        cursor.execute("""
            SELECT emp.id_empleado, emp.nombre, emp.apellido, emp.puesto
            FROM evento_empleados ee
            JOIN empleados emp ON ee.id_empleado = emp.id_empleado
            WHERE ee.id_evento = :1
        """, (id_evento,))
        empleados = [
            {
                "idEmpleado": emp[0],
                "nombre": emp[1],
                "apellido": emp[2],
                "puesto": emp[3]
            }
            for emp in cursor.fetchall()
        ]

        eventos.append({
            "idEvento": row[0],
            "fechaEvento": row[1].strftime("%d-%m-%Y %H:%M:%S"),
            "tipoEvento": row[2],
            "descripcion": row[3],
            "totalPrecio": row[4],
            "menu": {
                "nombreMenu": row[5],
                "descripcionMenu": row[6],
                "precioMenu": row[7]
            } if row[5] else None,
            "empleados": empleados
        })

    cursor.close()
    conexion.close()

    return jsonify({"eventos": eventos}), 200


def registrar_evento_model(data):
    try:
        fecha_evento = datetime.strptime(data["fechaEvento"], "%d-%m-%Y %H:%M:%S")
        tipo_evento = data["tipoEvento"]
        descripcion_evento = data["descripcion"]
        id_usuario = data["idUsuario"]
        menu_data = data["menu"]

        print(f"Recibido idUsuario: {id_usuario}")  # Log del ID recibido

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            # Verificar si existe el cliente y obtener información completa
            cursor.execute("""
                SELECT c.id_cliente, u.usuario, u.email, u.tipo_usuario
                FROM usuarios u
                LEFT JOIN clientes c ON c.id_usuario = u.id_usuario
                WHERE u.id_usuario = :1
            """, (id_usuario,))
            resultado = cursor.fetchone()
            
            if not resultado or not resultado[0]:
                print(f"No se encontró cliente para el idUsuario: {id_usuario}")
                return jsonify({"error": "Cliente no encontrado para ese idUsuario o el usuario no es un cliente", "codigo": 404}), 404
            
            id_cliente = resultado[0]
            print(f"Cliente encontrado - ID: {id_cliente}, Usuario: {resultado[1]}, Email: {resultado[2]}, Tipo: {resultado[3]}")

            # Verificar que el usuario sea de tipo CLIENTE
            if resultado[3] != 'CLIENTE':
                return jsonify({"error": "El usuario no es de tipo CLIENTE", "codigo": 400}), 400

            # Verificar si ya existe un evento para este cliente en la misma fecha
            cursor.execute("""
                SELECT e.id_evento 
                FROM eventos e
                JOIN evento_cliente ec ON e.id_evento = ec.id_evento
                WHERE ec.id_cliente = :1 
                AND TRUNC(e.fecha_evento) = TRUNC(:2)
            """, (id_cliente, fecha_evento))
            
            evento_existente = cursor.fetchone()
            if evento_existente:
                return jsonify({
                    "error": "Ya existe un evento registrado para este cliente en la misma fecha",
                    "codigo": 400
                }), 400

            try:
                # Insertar evento dejando que la secuencia maneje el ID
                cursor.execute("""
                    INSERT INTO eventos (fecha_evento, tipo_evento, descripcion)
                    VALUES (:1, :2, :3)
                    RETURNING id_evento INTO :4
                """, [fecha_evento, tipo_evento, descripcion_evento, cursor.var(oracledb.NUMBER)])
                
                id_evento = cursor.var.getvalue()[0]
                print(f"ID de evento generado automáticamente: {id_evento}")  # Debug log
            except Exception as e:
                print(f"Error al insertar evento: {str(e)}")
                print(f"Datos: fecha={fecha_evento}, tipo={tipo_evento}")
                raise e

            try:
                # Insertar en evento_cliente (la fecha_registro se maneja por DEFAULT SYSDATE)
                cursor.execute("""
                    INSERT INTO evento_cliente (id_evento, id_cliente)
                    VALUES (:1, :2)
                """, (id_evento, id_cliente))
            except Exception as e:
                print(f"Error al insertar evento_cliente: {str(e)}")
                print(f"Datos: id_evento={id_evento}, id_cliente={id_cliente}")
                conexion.rollback()
                raise e

            # Procesar menú
            id_menu = menu_data.get("idMenu")
            if id_menu is not None:
                cursor.execute("SELECT id_menu FROM menus WHERE id_menu = :1", (id_menu,))
                if not cursor.fetchone():
                    conexion.rollback()
                    return jsonify({"error": "Menú no encontrado", "codigo": 404}), 404
            else:
                # Validar campos requeridos del menú personalizado
                campos_menu_requeridos = ["nombre", "descripcion", "idPlatilloEntrada", 
                                        "idPlatilloPlatoPrincipal", "idPlatilloPostre", 
                                        "idPlatilloBebidas"]
                for campo in campos_menu_requeridos:
                    if campo not in menu_data:
                        conexion.rollback()
                        return jsonify({
                            "error": f"Campo '{campo}' requerido para menú personalizado",
                            "codigo": 400
                        }), 400

                # Verificar si existe un menú igual
                cursor.execute("""
                    SELECT id_menu FROM menus
                    WHERE id_platillo_entrada = :1 
                    AND NVL(id_platillo_sopa, -1) = NVL(:2, -1)
                    AND id_platillo_plato_principal = :3 
                    AND id_platillo_postre = :4
                    AND id_platillo_bebidas = :5
                    AND NVL(id_platillo_infantil, -1) = NVL(:6, -1)
                """, (
                    menu_data["idPlatilloEntrada"], 
                    menu_data.get("idPlatilloSopa"),
                    menu_data["idPlatilloPlatoPrincipal"],
                    menu_data["idPlatilloPostre"],
                    menu_data["idPlatilloBebidas"],
                    menu_data.get("idPlatilloInfantil")
                ))

                menu_existente = cursor.fetchone()
                if menu_existente:
                    id_menu = menu_existente[0]
                else:
                    # Crear nuevo menú usando RETURNING
                    cursor.execute("""
                        INSERT INTO menus (
                            nombre, descripcion,
                            id_platillo_entrada, id_platillo_sopa,
                            id_platillo_plato_principal, id_platillo_postre,
                            id_platillo_bebidas, id_platillo_infantil
                        ) VALUES (:1, :2, :3, :4, :5, :6, :7, :8)
                        RETURNING id_menu INTO :9
                    """, [
                        menu_data["nombre"],
                        menu_data["descripcion"],
                        menu_data["idPlatilloEntrada"],
                        menu_data.get("idPlatilloSopa"),
                        menu_data["idPlatilloPlatoPrincipal"],
                        menu_data["idPlatilloPostre"],
                        menu_data["idPlatilloBebidas"],
                        menu_data.get("idPlatilloInfantil"),
                        cursor.var(oracledb.NUMBER)
                    ])
                    id_menu = cursor.var.getvalue()[0]

            # Insertar relación evento-menú
            cursor.execute("""
                INSERT INTO evento_menu (id_evento, id_menu)
                VALUES (:1, :2)
            """, (id_evento, id_menu))

            # Calcular precio total
            cursor.execute("""
                SELECT COALESCE(SUM(p.precio_100_personas), 0)
                FROM menus m
                LEFT JOIN platillos p ON 
                    p.id_platillo IN (
                        m.id_platillo_entrada, m.id_platillo_sopa,
                        m.id_platillo_plato_principal, m.id_platillo_postre,
                        m.id_platillo_bebidas, m.id_platillo_infantil
                    )
                WHERE m.id_menu = :1
            """, (id_menu,))
            precio_total = cursor.fetchone()[0]

            # Actualizar precio en evento
            cursor.execute("""
                UPDATE eventos 
                SET total_precio = :1 
                WHERE id_evento = :2
            """, (precio_total, id_evento))

            conexion.commit()

            return jsonify({
                "idEvento": id_evento,
                "precio": precio_total
            }), 200

        except Exception as e:
            conexion.rollback()
            raise e
        finally:
            cursor.close()
            conexion.close()

    except Exception as e:
        print(f"Error en registrar_evento_model: {str(e)}")  # Para debug
        return jsonify({"error": str(e), "codigo": 500}), 500