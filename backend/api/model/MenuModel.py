from util.Database import obtener_conexion
from flask import jsonify

def obtener_menus_por_platillo(id_platillo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT nombre, descripcion, precio
        FROM menus
        WHERE :1 IN (
            id_platillo_entrada, id_platillo_sopa,
            id_platillo_plato_principal, id_platillo_postre,
            id_platillo_bebidas, id_platillo_infantil
        )
    """, (id_platillo,))
    resultados = [
        {
            "nombreMenu": row[0],
            "descripcionMenu": row[1],
            "precioMenu": row[2]
        } for row in cursor.fetchall()
    ]
    cursor.close()
    conexion.close()
    return resultados

def obtener_menu_con_detalle(id_menu):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

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
            cursor.execute("SELECT descripcion FROM platillos WHERE id_platillo = :1", (id_platillo,))
            desc = cursor.fetchone()
            descripcion_platillo = desc[0] if desc else "Sin descripción"

            cursor.execute("""
                SELECT i.descripcion, i.tipo_ingrediente
                FROM platillo_ingrediente pi
                JOIN ingredientes i ON pi.id_ingrediente = i.id_ingrediente
                WHERE pi.id_platillo = :1
                ORDER BY pi.paso
            """, (id_platillo,))
            ingredientes = [{"descripcion": ing[0], "tipo": ing[1]} for ing in cursor.fetchall()]

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


def insertar_menu(data):
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


def obtener_menus():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_menu, nombre, descripcion, precio,
               id_platillo_entrada, id_platillo_sopa, id_platillo_plato_principal,
               id_platillo_postre, id_platillo_bebidas, id_platillo_infantil
        FROM menus
    """)
    menus_raw = cursor.fetchall()

    if not menus_raw:
        cursor.close()
        conexion.close()
        return jsonify({"error": "No se encontraron menús", "codigo": 404}), 404

    lista_menus = []

    for menu in menus_raw:
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
                cursor.execute("SELECT descripcion FROM platillos WHERE id_platillo = :1", (id_platillo,))
                desc = cursor.fetchone()
                descripcion_platillo = desc[0] if desc else "Sin descripción"

                cursor.execute("""
                    SELECT i.descripcion, i.tipo_ingrediente
                    FROM platillo_ingrediente pi
                    JOIN ingredientes i ON pi.id_ingrediente = i.id_ingrediente
                    WHERE pi.id_platillo = :1
                    ORDER BY pi.paso
                """, (id_platillo,))
                ingredientes = [{"descripcion": ing[0], "tipo": ing[1]} for ing in cursor.fetchall()]

                platillos.append({
                    "tipo": tipo,
                    "descripcion": descripcion_platillo,
                    "ingredientes": ingredientes
                })

        lista_menus.append({
            "idMenu": menu[0],
            "nombre": menu[1],
            "descripcion": menu[2],
            "precio": menu[3],
            "platillos": platillos
        })

    cursor.close()
    conexion.close()

    return jsonify(lista_menus), 200
