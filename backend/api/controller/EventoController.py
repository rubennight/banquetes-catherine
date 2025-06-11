from flask import Blueprint, request, jsonify
from util.Database import obtener_conexion
from datetime import datetime

evento_controller = Blueprint('evento_controller', __name__)

# -----------------------------------------------
# 1. Asignar empleados a un evento
# -----------------------------------------------
@evento_controller.route('/eventos/asignarEmpleados', methods=['POST'])
def asignar_empleados_evento():
    data = request.get_json()
    id_evento = data.get('id_evento')
    empleados = data.get('empleados')

    if not id_evento or not empleados:
        return jsonify({"error": "Faltan datos", "codigo": 400}), 400

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Validar que el evento exista y obtener su fecha
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

# -----------------------------------------------
# 2. Listar todos los eventos
# -----------------------------------------------
@evento_controller.route('/eventos/listar', methods=['GET'])
def listar_eventos():
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

        # Empleados del evento
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

# -----------------------------------------------
# 3. Buscar eventos por fecha (YYYY-MM-DD)
# -----------------------------------------------
@evento_controller.route('/eventos/buscarPorFecha', methods=['GET'])
def buscar_eventos_por_fecha():
    fecha_str = request.args.get('fecha')

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

        # Empleados asignados
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

@evento_controller.route('/eventos/registrar', methods=['POST'])
def registrar_evento():
    data = request.get_json()

    # Validación de campos principales
    campos_requeridos = ["fechaEvento", "tipoEvento", "descripcion", "idUsuario", "menu"]
    faltantes = [campo for campo in campos_requeridos if campo not in data or data[campo] is None]
    if faltantes:
        return jsonify({"error": f"Campos faltantes: {faltantes}", "codigo": 400}), 400

    # Validar tipo de evento
    tipos_validos = ['BODA', 'BAUTIZO', 'XVs', 'EVENTO_CASUAL']
    if data["tipoEvento"] not in tipos_validos:
        return jsonify({"error": "Tipo de evento inválido", "codigo": 400}), 400

    # Parsear fecha
    try:
        fecha_completa = datetime.strptime(data["fechaEvento"], "%d-%m-%Y %H:%M:%S")
    except ValueError:
        return jsonify({"error": "Formato de fechaEvento inválido. Use dd-mm-yyyy HH:MM:SS", "codigo": 400}), 400

    tipo_evento = data["tipoEvento"]
    descripcion_evento = data["descripcion"]
    id_usuario = data["idUsuario"]
    menu_data = data["menu"]

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        # Obtener ID del cliente desde el ID del usuario
        cursor.execute("SELECT id_cliente FROM clientes WHERE id_usuario = :1", (id_usuario,))
        cliente = cursor.fetchone()
        if not cliente:
            return jsonify({"error": "Cliente no encontrado para ese idUsuario", "codigo": 404}), 404
        id_cliente = cliente[0]

        # Insertar evento
        cursor.execute("""
            INSERT INTO eventos (fecha_evento, tipo_evento, descripcion)
            VALUES (:1, :2, :3)
            RETURNING id_evento INTO :4
        """, (fecha_completa, tipo_evento, descripcion_evento, cursor.var(int)))
        
        id_evento = cursor.var.getvalue()

        # Insertar en evento_cliente
        cursor.execute("""
            INSERT INTO evento_cliente (id_evento, id_cliente)
            VALUES (:1, :2)
        """, (id_evento, id_cliente))

        # Procesar menú
        id_menu = menu_data.get("idMenu")
        if id_menu is not None:
            # Verificar que el menú existe
            cursor.execute("SELECT id_menu FROM menus WHERE id_menu = :1", (id_menu,))
            if not cursor.fetchone():
                return jsonify({"error": "Menú no encontrado", "codigo": 404}), 404
        else:
            # Validar campos requeridos para menú personalizado
            campos_menu_requeridos = ["nombre", "descripcion", "idPlatilloEntrada", 
                                    "idPlatilloPlatoPrincipal", "idPlatilloPostre", 
                                    "idPlatilloBebidas"]
            for campo in campos_menu_requeridos:
                if campo not in menu_data:
                    return jsonify({"error": f"Campo '{campo}' requerido para menú personalizado", 
                                  "codigo": 400}), 400

            # Verificar si existe un menú igual
            cursor.execute("""
                SELECT id_menu FROM menus
                WHERE id_platillo_entrada = :1 
                AND NVL(id_platillo_sopa, -1) = NVL(:2, -1)
                AND id_platillo_plato_principal = :3 
                AND id_platillo_postre = :4
                AND id_platillo_bebidas = :5
                AND NVL(id_platillo_infantil, -1) = NVL(:6, -1)
            """, (menu_data["idPlatilloEntrada"], 
                  menu_data.get("idPlatilloSopa"),
                  menu_data["idPlatilloPlatoPrincipal"],
                  menu_data["idPlatilloPostre"],
                  menu_data["idPlatilloBebidas"],
                  menu_data.get("idPlatilloInfantil")))
            
            menu_existente = cursor.fetchone()
            if menu_existente:
                id_menu = menu_existente[0]
            else:
                # Crear nuevo menú
                cursor.execute("""
                    INSERT INTO menus (
                        nombre, descripcion,
                        id_platillo_entrada, id_platillo_sopa,
                        id_platillo_plato_principal, id_platillo_postre,
                        id_platillo_bebidas, id_platillo_infantil
                    ) VALUES (:1, :2, :3, :4, :5, :6, :7, :8)
                    RETURNING id_menu INTO :9
                """, (
                    menu_data["nombre"],
                    menu_data["descripcion"],
                    menu_data["idPlatilloEntrada"],
                    menu_data.get("idPlatilloSopa"),
                    menu_data["idPlatilloPlatoPrincipal"],
                    menu_data["idPlatilloPostre"],
                    menu_data["idPlatilloBebidas"],
                    menu_data.get("idPlatilloInfantil"),
                    cursor.var(int)
                ))
                id_menu = cursor.var.getvalue()

        # Asociar menú con evento
        cursor.execute("""
            INSERT INTO evento_menu (id_evento, id_menu)
            VALUES (:1, :2)
        """, (id_evento, id_menu))

        # Calcular precio total basado en los platillos del menú
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

        # Actualizar precio del evento
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
        return jsonify({"error": str(e), "codigo": 500}), 500
    finally:
        cursor.close()
        conexion.close()