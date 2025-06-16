import { useState, useEffect } from "react";
import UsuariosService from "../../API/classes/UsuariosService";
import MenuService from "../../API/classes/MenuService";
import PlatillosService from "../../API/classes/PlatillosService"
import "./UltimaSeccionModalLogin.css";

const ModalLogin = ({ cerrarModal }) => {
    const [usuario, setUsuario] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [etapa, setEtapa] = useState("login");
    const [datosUsuario, setDatosUsuario] = useState(null);
    const [platillos, setPlatillos] = useState([]);

    // Para el formulario de evento
    const [fechaEvento, setFechaEvento] = useState("");
    const [tipoEvento, setTipoEvento] = useState("");
    const [descripcion, setDescripcion] = useState("");

    //Para la parte del menú
    const [menus, setMenus] = useState([]);
    const [menuPersonalizado, setMenuPersonalizado] = useState({});

    useEffect(() => {
        const cargarPlatillos = async () => {
            try {
                const data = await PlatillosService.obtenerPlatillos();
                setPlatillos(data);
            } catch (error) {
                console.error("Error al cargar platillos:", error);
            }
        };

        cargarPlatillos();
    }, []);

    const obtenerPlatillosPorTipo = (tipo) => {
        return platillos.filter((p) => (p.tipo_platillo || "").toUpperCase() === tipo);
    };

    const handleCrearMenuPersonalizado = (e) => {
        e.preventDefault();
        console.log("Menú personalizado:", menuPersonalizado);
        // Aquí puedes armar el objeto `menu` y enviarlo al backend si quieres
    };

    const handleLogin = async (e) => {
        e.preventDefault();
        setError("");
        try {
            const respuesta = await UsuariosService.login(usuario, password);
            setDatosUsuario(respuesta); // guarda info del usuario si la hay
            setEtapa("evento");
            // eslint-disable-next-line no-unused-vars
        } catch (err) {
            setError("Credenciales incorrectas.");
        }
    };

    const handleCrearEvento = async (e) => {
        e.preventDefault();
        const evento = {
            fechaEvento,
            tipoEvento,
            descripcion,
            idUsuario: datosUsuario?.idUsuario || 1, // reemplaza con el campo correcto del backend
        };
        console.log("Evento a enviar:", evento);

        try {
            const menus = await new MenuService().obtenerMenus();
            setMenus(menus);
            setEtapa('seleccionarMenu');
        } catch (error) {
            console.error('Error cargando los menús', error);
        }
    };

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                {etapa === "login" && (
                    <>
                        <h3>Inicia sesión para cotizar tu evento</h3>
                        {error && <p className="error">{error}</p>}
                        <form onSubmit={handleLogin}>
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
                    </>
                )}

                {etapa === "evento" && (
                    <>
                        <h3>Datos de tu evento</h3>
                        <form onSubmit={handleCrearEvento}>
                            <input
                                type="datetime-local"
                                value={fechaEvento}
                                onChange={(e) => setFechaEvento(e.target.value)}
                                required
                            />
                            <select
                                value={tipoEvento}
                                onChange={(e) => setTipoEvento(e.target.value)}
                                required
                            >
                                <option value="">Tipo de evento</option>
                                <option value="BODA">Boda</option>
                                <option value="XV">XV años</option>
                                <option value="CUMPLEAÑOS">Cumpleaños</option>
                                <option value="EMPRESARIAL">Empresarial</option>
                            </select>
                            <input
                                type="text"
                                placeholder="Descripción del evento"
                                value={descripcion}
                                onChange={(e) => setDescripcion(e.target.value)}
                                required
                            />
                            <button type="submit">Escoger Menú</button>
                        </form>
                    </>
                )}

                {etapa === "seleccionarMenu" && (
                    <>
                        <h3>Selecciona tu menú</h3>
                        <div className="contenedor-menus">
                            {menus.map((menu) => (
                                <div key={menu.idMenu} className="tarjeta-menu">
                                    <h4>{menu.nombre}</h4>
                                    <p>{menu.descripcion}</p>
                                    <p><strong>Precio:</strong> ${menu.precio} x 100 personas</p>
                                    <ul>
                                        {menu.platillos.map((p) => (
                                            <li key={p.tipo}>
                                                <strong>{p.tipo}:</strong>
                                                <br />
                                                {p.descripcion}
                                            </li>
                                        ))}
                                    </ul>
                                    <button>Seleccionar este menú</button>
                                </div>
                            ))}
                        </div>
                        <button onClick={() => setEtapa("personalizarMenu")} className="cerrar">Personaliza tu menú</button>
                    </>
                )}

                {etapa === "personalizarMenu" && (
                    <>
                        <h3>Personaliza tu menú</h3>
                        <form onSubmit={handleCrearMenuPersonalizado}>
                            {["ENTRADA", "SOPA", "PLATILLO_PRINCIPAL", "POSTRE", "BEBIDA", "INFANTIL"].map((tipo) => (
                                <div key={tipo}>
                                    <label>{tipo}</label>
                                    <select
                                        value={menuPersonalizado[tipo] || ""}
                                        onChange={(e) =>
                                            setMenuPersonalizado({
                                                ...menuPersonalizado,
                                                [tipo]: e.target.value,
                                            })
                                        }
                                    >
                                        <option value="">Selecciona un platillo</option>
                                        {obtenerPlatillosPorTipo(tipo).map((platillo) => (
                                            <option key={platillo.id_platillo} value={platillo.id_platillo}>
                                                {platillo.descripcion}
                                            </option>
                                        ))}
                                    </select>
                                </div>
                            ))}
                            <button type="submit">Guardar menú personalizado</button>
                        </form>
                    </>
                )}
                <button onClick={cerrarModal} className="cerrar">Cerrar</button>
            </div>
        </div>
    );
};

export default ModalLogin;
