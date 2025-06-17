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

  async obtenerEventosPorCliente(idUsuario) {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:5000/eventos/cliente/${idUsuario}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data?.error || "Error al obtener eventos del cliente");
      }
      return data;
    } catch (error) {
      console.error("Error en EventoService.obtenerEventosPorCliente:", error);
      throw error;
    }
  }

  async obtenerEventosPendientes() {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch("http://localhost:5000/eventos/pendientes", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data?.error || "Error al obtener eventos pendientes");
      }
      return data;
    } catch (error) {
      console.error("Error en EventoService.obtenerEventosPendientes:", error);
      throw error;
    }
  }

  async asignarEmpleadoAEvento(idEvento, idEmpleado) {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:5000/eventos/${idEvento}/asignar-empleado`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({ id_empleado: idEmpleado }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data?.error || "Error al asignar empleado a evento");
      }
      return data;
    } catch (error) {
      console.error("Error en EventoService.asignarEmpleadoAEvento:", error);
      throw error;
    }
  }
}

export default EventoService;
