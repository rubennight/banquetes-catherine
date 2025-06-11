from flask import Blueprint, request, jsonify
from util.Database import obtener_conexion

menu_controller = Blueprint('menu_controller', __name__)

@menu_controller.route('/menus/obtenerPorId', methods=['GET'])
def obtener_menu_por_id():
    id_menu = request.args.get('idMenu')

    if not id_menu:
        return jsonify({"error": "Falta el parámetro idMenu", "codigo": 400}), 400

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Obtener menú
    cursor.execute("""
        SELECT id_menu, nombre, descripcion, precio,
               id_platillo_entrada, id_platillo_sopa, id_platillo_plato_principal,
               id_platillo_postre, id_platillo_bebidas, id_platillo_infantil
        FROM menus
        WHERE id_menu = :1
    """, (id_menu,))
    menu = cursor.fetchone()

    if not menu:
        cursor.close()
        conexion.close()
        return jsonify({"error": "Menú no encontrado", "codigo": 404}), 404

    # Mapeo de tipos
    tipos = {
        "ENTRADA": menu[4],
        "SOPA": menu[5],
        "PLATILLO_PRINCIPAL": menu[6],
        "POSTRE": menu[7],
        "BEBIDA": menu[8],
        "INFANTIL": menu[9]
    }

    platillos = []

    for tipo, id_platillo in tipos.items():
        if id_platillo:
            # Obtener descripción de platillo
            cursor.execute("""
                SELECT descripcion FROM platillos WHERE id_platillo = :1
            """, (id_platillo,))
            desc = cursor.fetchone()
            descripcion_platillo = desc[0] if desc else "Sin descripción"

            # Obtener ingredientes
            cursor.execute("""
                SELECT i.descripcion, i.tipo_ingrediente
                FROM platillo_ingrediente pi
                JOIN ingredientes i ON pi.id_ingrediente = i.id_ingrediente
                WHERE pi.id_platillo = :1
                ORDER BY pi.paso
            """, (id_platillo,))
            ingredientes = [
                {"descripcion": ing[0], "tipo": ing[1]}
                for ing in cursor.fetchall()
            ]

            platillos.append({
                "tipo": tipo,
                "descripcion": descripcion_platillo,
                "ingredientes": ingredientes
            })

    cursor.close()
    conexion.close()

    return jsonify({
        "idMenu": menu[0],
        "nombre": menu[1],
        "descripcion": menu[2],
        "precio": menu[3],
        "platillos": platillos
    }), 200
# -----------------------------------------------
# 2. Agregar un nuevo menú
# -----------------------------------------------
@menu_controller.route('/menus/agregar', methods=['POST'])
def agregar_menu():
    data = request.get_json()
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    precio = data.get('precio')
    platillos = data.get('platillos', {})

    if not nombre or not descripcion or not precio or not isinstance(platillos, dict):
        return jsonify({"error": "Faltan campos obligatorios", "codigo": 400}), 400

    entrada = platillos.get("ENTRADA")
    sopa = platillos.get("SOPA")
    principal = platillos.get("PLATILLO_PRINCIPAL")
    postre = platillos.get("POSTRE")
    bebida = platillos.get("BEBIDA")
    infantil = platillos.get("INFANTIL")

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO menus (
            nombre, descripcion, precio,
            id_platillo_entrada, id_platillo_sopa, id_platillo_plato_principal,
            id_platillo_postre, id_platillo_bebidas, id_platillo_infantil
        ) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)
    """, (
        nombre, descripcion, precio,
        entrada, sopa, principal, postre, bebida, infantil
    ))

    cursor.execute("SELECT MAX(id_menu) FROM menus")
    id_generado = cursor.fetchone()[0]

    conexion.commit()
    cursor.close()
    conexion.close()

    return jsonify({
        "mensaje": "Menú agregado correctamente",
        "id_menu": id_generado
    }), 200