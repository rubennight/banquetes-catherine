class EmpleadoService {
  async obtenerEmpleadosDisponibles() {
    try {
      const token = localStorage.getItem('token');
      // Asume que hay un endpoint en el backend como /empleados/disponibles
      const response = await fetch("http://localhost:5000/empleados/disponibles", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data?.error || "Error al obtener empleados disponibles");
      }
      return data;
    } catch (error) {
      console.error("Error en EmpleadoService.obtenerEmpleadosDisponibles:", error);
      throw error;
    }
  }
}

export default EmpleadoService; 