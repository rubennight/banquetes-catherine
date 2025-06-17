from util.Database import obtener_conexion

def obtener_primeros_platillos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id_platillo, descripcion, tipo_platillo, precio_100_personas, url_imagen
        FROM platillos
        WHERE ROWNUM <= 8
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultados

# En PlatillosService.py
@staticmethod
def listar_platillos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_platillo, descripcion, tipo_platillo, precio_100_personas, url_imagen FROM platillos")
    filas = cursor.fetchall()
    cursor.close()
    conexion.close()

    return [
        {
            "id_platillo": fila[0],
            "descripcion": fila[1],
            "tipo_platillo": fila[2],
            "precio_100_personas": float(fila[3]),
            "url_imagen": fila[4]
        }
        for fila in filas
    ]

