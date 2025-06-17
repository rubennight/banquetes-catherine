import { useState, useEffect } from "react";
import UsuariosService from "../../API/classes/UsuariosService";
import MenuService from "../../API/classes/MenuService";
import PlatillosService from "../../API/classes/PlatillosService";
import EventoService from "../../API/classes/EventoService";
import "./UltimaSeccionModalLogin.css";

const ModalLogin = ({ cerrarModal }) => {
    const [usuario, setUsuario] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [etapa, setEtapa] = useState("login");
    const [datosUsuario, setDatosUsuario] = useState(null);
    const [platillos, setPlatillos] = useState([]);

    const [fechaEvento, setFechaEvento] = useState("");
    const [tipoEvento, setTipoEvento] = useState("");
    const [descripcion, setDescripcion] = useState("");

    const [menus, setMenus] = useState([]);
    const [menuPersonalizado, setMenuPersonalizado] = useState({});
    const [menuSeleccionado, setMenuSeleccionado] = useState(null);
    const [respuestaEvento, setRespuestaEvento] = useState(null);

    const formatearFecha = (isoString) => {
        const fecha = new Date(isoString);
        const pad = (n) => (n < 10 ? "0" + n : n);
        const dia = pad(fecha.getDate());
        const mes = pad(fecha.getMonth() + 1);
        const anio = fecha.getFullYear();
        const horas = pad(fecha.getHours());
        const minutos = pad(fecha.getMinutes());
        const segundos = pad(fecha.getSeconds());
        return `${dia}-${mes}-${anio} ${horas}:${minutos}:${segundos}`;
    };

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
        try {
            const menus = await new MenuService().obtenerMenus();
            setMenus(menus);
            setEtapa("seleccionarMenu");
        } catch (error) {
            console.error("Error cargando los menús", error);
        }
    };

    const handleSeleccionarMenu = async (menu) => {
        const evento = {
            fechaEvento: formatearFecha(fechaEvento),
            tipoEvento,
            descripcion,
            idUsuario: datosUsuario?.idUsuario || 1,
            menu: {
                idMenu: menu.idMenu,
                descripcion: null,
                nombre: null,
                idPlatilloEntrada: null,
                idPlatilloSopa: null,
                idPlatilloPlatoPrincipal: null,
                idPlatilloPostre: null,
                idPlatilloBebidas: null,
                idPlatilloInfantil: null,
            },
        };

        try {
            const respuesta = await new EventoService().agregarEvento(evento);
            setMenuSeleccionado(menu);
            setRespuestaEvento(respuesta);
            setEtapa("cotizacion");
        } catch (error) {
            console.error("Error al crear evento con menú predefinido:", error);
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
                nombre: "Menú personalizado",
                descripcion: "Menú con selección propia",
                idPlatilloEntrada: parseInt(menuPersonalizado.ENTRADA),
                idPlatilloSopa: parseInt(menuPersonalizado.SOPA),
                idPlatilloPlatoPrincipal: parseInt(menuPersonalizado.PLATILLO_PRINCIPAL),
                idPlatilloPostre: parseInt(menuPersonalizado.POSTRE),
                idPlatilloBebidas: parseInt(menuPersonalizado.BEBIDA),
                idPlatilloInfantil: null,
            },
        };

        try {
            const respuesta = await new EventoService().agregarEvento(evento);
            setMenuSeleccionado(evento.menu);
            setRespuestaEvento(respuesta);
            setEtapa("cotizacion");
        } catch (error) {
            console.error("Error al crear evento personalizado:", error);
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
                                <option value="XV">XV años</option>
                                <option value="CUMPLEAÑOS">Cumpleaños</option>
                                <option value="EVENTO_CASUAL">Evento Casual</option>
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
                                            <li key={p.tipo}>
                                                <strong>{p.tipo}:</strong> {p.descripcion}
                                            </li>
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
                            {["ENTRADA", "SOPA", "PLATILLO_PRINCIPAL", "POSTRE", "BEBIDA"].map((tipo) => (
                                <div key={tipo}>
                                    <label>{tipo}</label>
                                    <select value={menuPersonalizado[tipo] || ""} onChange={(e) => setMenuPersonalizado({ ...menuPersonalizado, [tipo]: e.target.value })}>
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

                {etapa === "cotizacion" && respuestaEvento && (
                    <>
                        <h3>Cotización Generada</h3>
                        <p><strong>Folio del evento:</strong> {respuestaEvento.idEvento}</p>
                        <p><strong>Precio total:</strong> ${respuestaEvento.precio}</p>
                        <h4>Menú seleccionado:</h4>
                        <pre>{JSON.stringify(menuSeleccionado, null, 2)}</pre>
                        <button onClick={() => alert("Aquí iría el proceso de pago.")}>Hacer pago</button>
                    </>
                )}

                <button onClick={cerrarModal} className="cerrar">Cerrar</button>
            </div>
        </div>
    );
};

export default ModalLogin;
