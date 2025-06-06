class Evento:
    def __init__(self, id_evento, fecha_evento, hora_evento, tipo_evento, descripcion, total_precio):
        self.id_evento = id_evento
        self.fecha_evento = fecha_evento
        self.hora_evento = hora_evento
        self.tipo_evento = tipo_evento
        self.descripcion = descripcion
        self.total_precio = total_precio

    def to_dict(self):
        """Convierte el objeto Evento a un diccionario (útil para JSON o bases de datos)."""
        return {
            "id_evento": self.id_evento,
            "fecha_evento": self.fecha_evento,
            "hora_evento": self.hora_evento,
            "tipo_evento": self.tipo_evento,
            "descripcion": self.descripcion,
            "total_precio": self.total_precio
        }