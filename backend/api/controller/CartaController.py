from flask import Blueprint, jsonify
from util.Database import obtener_conexion

carta_controller = Blueprint('carta_controller', __name__)

@carta_controller.route('/usuarios/infoCarta', methods=['GET'])
def obtener_info_carta():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # 1. Obtener primeros 8 platillos
    cursor.execute("""
        SELECT id_platillo, descripcion, tipo_platillo, precio_100_personas, url_imagen
        FROM platillos
        WHERE ROWNUM <= 8
    """)
    platillos = cursor.fetchall()

    resultado = []

    for p in platillos:
        id_platillo, descripcion, tipo, precio, imagen = p

        # 2. Obtener ingredientes del platillo
        cursor.execute("""
            SELECT i.descripcion, i.tipo_ingrediente
            FROM platillo_ingrediente pi
            JOIN ingredientes i ON pi.id_ingrediente = i.id_ingrediente
            WHERE pi.id_platillo = :1
            ORDER BY pi.paso
        """, (id_platillo,))
        ingredientes = [
            {
                "descripcionIngrediente": row[0],
                "tipoIngrediente": row[1]
            } for row in cursor.fetchall()
        ]

        # 3. Obtener menús donde aparece el platillo
        cursor.execute("""
            SELECT nombre, descripcion, precio
            FROM menus
            WHERE :1 IN (
                id_platillo_entrada, id_platillo_sopa,
                id_platillo_plato_principal, id_platillo_postre,
                id_platillo_bebidas, id_platillo_infantil
            )
        """, (id_platillo,))
        menus = [
            {
                "nombreMenu": row[0],
                "descripcionMenu": row[1],
                "precioMenu": row[2]
            } for row in cursor.fetchall()
        ]

        resultado.append({
            "idPlatillo": id_platillo,
            "descripcionPlatillo": descripcion,
            "tipoPlatillo": tipo,
            "precio": precio,
            "imagen": imagen,
            "ingredientes": ingredientes,
            "menus": menus
        })

    cursor.close()
    conexion.close()
    return jsonify(resultado), 200
