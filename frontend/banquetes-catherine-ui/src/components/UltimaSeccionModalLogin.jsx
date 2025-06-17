import { useState, useEffect } from "react";
import UsuariosService from "../../API/classes/UsuariosService";
import MenuService from "../../API/classes/MenuService";
import PlatillosService from "../../API/classes/PlatillosService";
import EventoService from "../../API/classes/EventoService";
import Spinner from "../assets/react.svg"; // Asegúrate de tener este archivo SVG
import "./UltimaSeccionModalLogin.css";

const ModalLogin = ({ cerrarModal }) => {
    const [usuario, setUsuario] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [etapa, setEtapa] = useState("login");
    const [datosUsuario, setDatosUsuario] = useState(null);
    const [platillos, setPlatillos] = useState([]);
    const [menus, setMenus] = useState([]);
    const [menuSeleccionado, setMenuSeleccionado] = useState(null);
    const [menuPersonalizado, setMenuPersonalizado] = useState({});
    const [nombreMenuPersonalizado, setNombreMenuPersonalizado] = useState("");
    const [descripcionMenuPersonalizado, setDescripcionMenuPersonalizado] = useState("");
    const [fechaEvento, setFechaEvento] = useState("");
    const [tipoEvento, setTipoEvento] = useState("");
    const [descripcion, setDescripcion] = useState("");
    const [cotizacion, setCotizacion] = useState(null);
    const [loading, setLoading] = useState(false);

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

    const handlePago = () => {
        setEtapa("pagoExitoso");
    };

    const obtenerPlatillosPorTipo = (tipo) => {
        return platillos.filter((p) => (p.tipo_platillo || "").toUpperCase() === tipo);
    };

    const getPlatilloPorId = (id) => platillos.find(p => p.id_platillo === parseInt(id));

    const formatearFecha = (fechaLocal) => {
        const fecha = new Date(fechaLocal);
        return `${String(fecha.getDate()).padStart(2, "0")}-${String(fecha.getMonth() + 1).padStart(2, "0")}-${fecha.getFullYear()} ${String(fecha.getHours()).padStart(2, "0")}:${String(fecha.getMinutes()).padStart(2, "0")}:00`;
    };

    const handleLogin = async (e) => {
        e.preventDefault();
        setError("");
        try {
            const respuesta = await UsuariosService.login(usuario, password);
            setDatosUsuario(respuesta);
            setEtapa("evento");
            // eslint-disable-next-line no-unused-vars
        } catch (err) {
            setError("Credenciales incorrectas.");
        }
    };

    const handleCrearEvento = async (e) => {
        e.preventDefault();
        // eslint-disable-next-line no-unused-vars
        const evento = {
            fechaEvento,
            tipoEvento,
            descripcion,
            idUsuario: datosUsuario?.idUsuario || 1,
        };

        try {
            const menus = await new MenuService().obtenerMenus();
            setMenus(menus);
            setEtapa('seleccionarMenu');
        } catch (error) {
            console.error('Error cargando los menús', error);
        }
    };

    const handleSeleccionarMenu = async (menu) => {
        const evento = {
            fechaEvento: formatearFecha(fechaEvento),
            tipoEvento,
            descripcion,
            idUsuario: datosUsuario?.idUsuario || 1,
            menu: {
                ...menu
            }
        };

        try {
            setLoading(true);
            const respuesta = await new EventoService().agregarEvento(evento);
            setCotizacion(respuesta);
            setMenuSeleccionado(menu);
            setEtapa("cotizacion");
        } catch (error) {
            console.error("Error al agregar evento:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleCrearMenuPersonalizado = async (e) => {
        e.preventDefault();

        const evento = {
            fechaEvento: formatearFecha(fechaEvento),
            tipoEvento,
            descripcion,
            idUsuario: datosUsuario?.idUsuario || 1,
            menu: {
                idMenu: null,
                nombre: nombreMenuPersonalizado,
                descripcion: descripcionMenuPersonalizado,
                idPlatilloEntrada: parseInt(menuPersonalizado.ENTRADA),
                idPlatilloSopa: parseInt(menuPersonalizado.SOPA),
                idPlatilloPlatoPrincipal: parseInt(menuPersonalizado.PLATILLO_PRINCIPAL),
                idPlatilloPostre: parseInt(menuPersonalizado.POSTRE),
                idPlatilloBebidas: parseInt(menuPersonalizado.BEBIDA),
                idPlatilloInfantil: null,
            }
        };

        try {
            setLoading(true);
            const respuesta = await new EventoService().agregarEvento(evento);
            setCotizacion(respuesta);
            setMenuSeleccionado(evento.menu);
            setEtapa("cotizacion");
        } catch (error) {
            console.error("Error al agregar evento:", error);
        } finally {
            setLoading(false);
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
                            <input type="text" placeholder="Usuario" value={usuario} onChange={(e) => setUsuario(e.target.value)} required />
                            <input type="password" placeholder="Contraseña" value={password} onChange={(e) => setPassword(e.target.value)} required />
                            <button type="submit">Iniciar sesión</button>
                        </form>
                    </>
                )}

                {etapa === "evento" && (
                    <>
                        <h3>Datos de tu evento</h3>
                        <form onSubmit={handleCrearEvento}>
                            <input type="datetime-local" value={fechaEvento} onChange={(e) => setFechaEvento(e.target.value)} required />
                            <select value={tipoEvento} onChange={(e) => setTipoEvento(e.target.value)} required>
                                <option value="">Tipo de evento</option>
                                <option value="BODA">Boda</option>
                                <option value="XVs">XV años</option>
                                <option value="CUMPLEAÑOS">Cumpleaños</option>
                                <option value="EVENTO_CASUAL">Empresarial</option>
                            </select>
                            <input type="text" placeholder="Descripción del evento" value={descripcion} onChange={(e) => setDescripcion(e.target.value)} required />
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
                                            <li key={p.tipo}><strong>{p.tipo}:</strong><br />{p.descripcion}</li>
                                        ))}
                                    </ul>
                                    <button onClick={() => handleSeleccionarMenu(menu)}>Seleccionar este menú</button>
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
                            <input type="text" placeholder="Nombre del menú" value={nombreMenuPersonalizado} onChange={(e) => setNombreMenuPersonalizado(e.target.value)} required />
                            <textarea placeholder="Descripción del menú" value={descripcionMenuPersonalizado} onChange={(e) => setDescripcionMenuPersonalizado(e.target.value)} required />
                            {["ENTRADA", "SOPA", "PLATILLO_PRINCIPAL", "POSTRE", "BEBIDA"].map((tipo) => (
                                <div key={tipo}>
                                    <label>{tipo}</label>
                                    <select value={menuPersonalizado[tipo] || ""} onChange={(e) => setMenuPersonalizado({ ...menuPersonalizado, [tipo]: e.target.value })}>
                                        <option value="">Selecciona un platillo</option>
                                        {obtenerPlatillosPorTipo(tipo).map((platillo) => (
                                            <option key={platillo.id_platillo} value={platillo.id_platillo}>{platillo.descripcion}</option>
                                        ))}
                                    </select>
                                </div>
                            ))}
                            <button type="submit">Guardar menú personalizado</button>
                        </form>
                    </>
                )}

                {etapa === "cotizacion" && cotizacion && (
                    <>
                        <h3>Resumen del evento</h3>
                        <p><strong>ID del evento:</strong> {cotizacion.idEvento}</p>
                        <p><strong>Precio:</strong> ${cotizacion.precio}</p>
                        <h4>Menú seleccionado:</h4>
                        <p><strong>Nombre:</strong> {menuSeleccionado.nombre}</p>
                        <p><strong>Descripción:</strong> {menuSeleccionado.descripcion}</p>
                        <ul>
                            {["idPlatilloEntrada", "idPlatilloSopa", "idPlatilloPlatoPrincipal", "idPlatilloPostre", "idPlatilloBebidas"].map((campo, i) => {
                                const platillo = getPlatilloPorId(menuSeleccionado[campo]);
                                return platillo ? <li key={i}><strong>{platillo.tipo}:</strong> {platillo.descripcion}</li> : null;
                            })}
                        </ul>
                        <button onClick={handlePago}>Hacer pago</button>
                    </>
                )}

                {loading && (
                    <div className="loading-overlay">
                        <img src={Spinner} alt="Cargando..." />
                    </div>
                )}

                {etapa === "pagoExitoso" && (
                    <>
                        <h3>¡Pago realizado con éxito!</h3>
                        <p>Tu evento ha sido registrado correctamente.</p>
                        <p>Gracias por confiar en nosotros. 🎉</p>
                    </>
                )}

                <button onClick={cerrarModal} className="cerrar">Cerrar</button>
            </div>
        </div>
    );
};

export default ModalLogin;
