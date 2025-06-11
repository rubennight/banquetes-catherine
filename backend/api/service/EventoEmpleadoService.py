from util.Database import obtener_conexion

class EventoEmpleadoService:
    @staticmethod
    def obtener_empleados_disponibles(fecha, id_evento=None):
        """
        Obtiene los empleados disponibles para una fecha específica.
        
        Args:
            fecha (datetime): Fecha para verificar disponibilidad
            id_evento (int, optional): ID del evento actual (para excluirlo de la verificación)
            
        Returns:
            list: Lista de diccionarios con información de empleados disponibles
        """
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        try:
            # Consulta base para obtener empleados disponibles
            query = """
                SELECT e.id_empleado, e.nombre, e.apellido, e.puesto
                FROM empleados e
                WHERE e.activo = 'S'
            """
            
            params = []
            
            # Si hay una fecha, filtrar por empleados que no tengan eventos ese día
            if fecha:
                query += """
                    AND e.id_empleado NOT IN (
                        SELECT ee.id_empleado
                        FROM evento_empleados ee
                        JOIN eventos ev ON ee.id_evento = ev.id_evento
                        WHERE TRUNC(ev.fecha_evento) = TRUNC(:1)
                """
                params.append(fecha)
                
                # Si se proporciona un ID de evento, excluirlo de la verificación
                if id_evento:
                    query += " AND ev.id_evento <> :2"
                    params.append(id_evento)
                
                query += ")"
            
            # Ordenar resultados
            query += " ORDER BY e.apellido, e.nombre"
            
            # Ejecutar consulta
            cursor.execute(query, tuple(params))
            
            # Formatear resultados
            empleados = [
                {
                    "idEmpleado": row[0],
                    "nombre": row[1],
                    "apellido": row[2],
                    "puesto": row[3]
                } for row in cursor.fetchall()
            ]
            
            return empleados
            
        except Exception as e:
            # Loggear el error (implementa tu propio sistema de logging)
            print(f"Error al obtener empleados disponibles: {str(e)}")
            raise e
        finally:
            cursor.close()
            conexion.close()
    
    @staticmethod
    def asignar_empleado_evento(id_evento, id_empleado):
        """
        Asigna un empleado a un evento específico.
        
        Args:
            id_evento (int): ID del evento
            id_empleado (int): ID del empleado a asignar
            
        Returns:
            bool: True si la asignación fue exitosa, False en caso contrario
        """
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        try:
            # Verificar si ya está asignado
            cursor.execute(
                "SELECT COUNT(*) FROM evento_empleados WHERE id_evento = :1 AND id_empleado = :2",
                (id_evento, id_empleado)
            )
            if cursor.fetchone()[0] > 0:
                return False  # Ya está asignado
                
            # Insertar la asignación
            cursor.execute(
                "INSERT INTO evento_empleados (id_evento, id_empleado) VALUES (:1, :2)",
                (id_evento, id_empleado)
            )
            
            conexion.commit()
            return True
            
        except Exception as e:
            conexion.rollback()
            print(f"Error al asignar empleado: {str(e)}")
            return False
        finally:
            cursor.close()
            conexion.close()