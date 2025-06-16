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
    setMensaje("");
    try {
      const respuesta = await UsuariosService.login(usuario, password);
      setMensaje(`¡Bienvenido, ${respuesta.usuario || "usuario"}!`);
      // No cerrar modal para que el usuario vea el mensaje
      // cerrarModal(); // Quitar esta línea para que no cierre inmediatamente
    // eslint-disable-next-line no-unused-vars
    } catch (err) {
      setError("Credenciales incorrectas.");
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h3>Inicia sesión para cotizar tu evento</h3>
        {error && <p className="error">{error}</p>}
        {mensaje && <p className="mensaje-exito">{mensaje}</p>}
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
