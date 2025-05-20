# util/Database.py
import oracledb

def obtener_conexion():
    return oracledb.connect(
        user="banquetes_admin",
        password="banquetes2025",
        dsn="localhost/XEPDB1"
    )
