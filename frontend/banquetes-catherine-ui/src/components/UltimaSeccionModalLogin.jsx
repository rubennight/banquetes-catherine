import { useState } from "react";
import UsuariosService from "../../API/classes/UsuariosService";
import "./UltimaSeccionModalLogin.css";

const ModalLogin = ({ cerrarModal }) => {
    const [usuario, setUsuario] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [mensaje, setMensaje] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        try {
            const respuesta = await UsuariosService.login(usuario, password);
            setMensaje(`¡Bienvenido, ${respuesta.usuario || "usuario"}!`);
            // Aquí podrías guardar token o info si te la regresan
            cerrarModal();
        } catch (err) {
            setError("Credenciales incorrectas.");
        }
    };

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <h3>Inicia sesión para cotizar tu evento</h3>
                {error && <p className="error">{error}</p>}
                <form onSubmit={handleSubmit}>
                    <input
                        type="text"
                        placeholder="Usuario"
                        value={usuario}
                        onChange={(e) => setUsuario(e.target.value)}
                        required
                    />
                    <input
                        type="password"
                        placeholder="Contraseña"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                    <button type="submit">Iniciar sesión</button>
                </form>
                <button onClick={cerrarModal} className="cerrar">Cerrar</button>
            </div>
        </div>
    );
};

export default ModalLogin;
