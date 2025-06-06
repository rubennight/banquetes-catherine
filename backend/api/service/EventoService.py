from datetime import datetime

class EventoService:
    def __init__(self, database):
        self.db = database
        self.tabla = "eventos"

    def crear_evento(self, evento):
        """
        Recibe un objeto Evento y lo guarda en la base de datos.
        """
        evento_dict = evento.to_dict()
        self.db.insertar(self.tabla, evento_dict)

    def obtener_evento_por_id(self, id_evento):
        """
        Busca y devuelve un evento por su ID.
        """
        return self.db.obtener_por_id(self.tabla, id_evento)

    def obtener_todos_los_eventos(self):
        """
        Devuelve todos los eventos almacenados.
        """
        return self.db.obtener_todos(self.tabla)

    def actualizar_evento(self, id_evento, datos_actualizados):
        """
        Actualiza un evento con nuevos datos.
        """
        return self.db.actualizar(self.tabla, id_evento, datos_actualizados)

    def eliminar_evento(self, id_evento):
        """
        Elimina un evento por ID.
        """
        return self.db.eliminar(self.tabla, id_evento)
