// src/services/UsuariosService.js
class UsuariosService {
    async obtenerUsuarios() {
        try {
            const response = await fetch('http://127.0.0.1:5000/usuarios/infoCarta');
            if (!response.ok) {
                throw new Error(`Error en la respuesta: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error("Error al obtener usuarios:", error);
            throw error;
        }
    }

    async login(usuario, password) {
        try {
            const response = await fetch('http://127.0.0.1:5000/usuarios/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ usuario, password }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Error en el inicio de sesión');
            }

            return data;
        } catch (error) {
            console.error("Error durante el login:", error);
            throw error;
        }
    }
}

export default new UsuariosService();
