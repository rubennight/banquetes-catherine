class PlatillosService {
    async obtenerPlatillos() {
        try {
            const response = await fetch("http://127.0.0.1:5000/platillos");
            if (!response.ok) throw new Error("Error al obtener platillos");
            return await response.json();
        } catch (error) {
            console.error("Error en PlatillosService:", error);
            throw error;
        }
    }
}

export default new PlatillosService();
