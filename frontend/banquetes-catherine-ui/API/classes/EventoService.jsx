class EventoService {
  async agregarEvento(evento) {
    try {
      const response = await fetch("http://localhost:5000/eventos/registrar", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(evento),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data?.error || "Error en el servidor");
      }

      return data;
    } catch (error) {
      console.error("Error en EventoService.agregarEvento:", error);
      throw error;
    }
  }
}

export default EventoService;
