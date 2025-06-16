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

def listar_platillos():
    conexion = obtener_conexion();
    cursor = conexion.cursor()
    cursor = conexion.cursor();
    cursor.execute("""
                   SELECT * FROM platillos
                   """)
    
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultados