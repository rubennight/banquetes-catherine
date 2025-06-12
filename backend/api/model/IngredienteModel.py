from util.Database import obtener_conexion

def obtener_ingredientes_por_platillo(id_platillo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT i.descripcion, i.tipo_ingrediente
        FROM platillo_ingrediente pi
        JOIN ingredientes i ON pi.id_ingrediente = i.id_ingrediente
        WHERE pi.id_platillo = :1
        ORDER BY pi.paso
    """, (id_platillo,))
    resultados = [
        {
            "descripcionIngrediente": row[0],
            "tipoIngrediente": row[1]
        } for row in cursor.fetchall()
    ]
    cursor.close()
    conexion.close()
    return resultados