import { useState, useEffect } from "react";
import UsuariosService from "../../API/classes/UsuariosService";
import "./CartaPlatillo.css"; // <- Asegúrate de tener este archivo

const CartaPlatillo = () => {
    const [platillos, setPlatillos] = useState([]);
    const [cargando, setCargando] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const cargarPlatillos = async () => {
            try {
                const data = await UsuariosService.obtenerUsuarios();
                setPlatillos(data);
            } catch (err) {
                setError("No se pudieron cargar los platillos" + err.message);
            } finally {
                setCargando(false);
            }
        };

        cargarPlatillos();
    }, []);

    if (cargando) return <div>Cargando...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div className="menu-section-container">
            {platillos.slice(0, 5).map((platillo) => (
                <div key={platillo.idPlatillo} className="platillo-card">
                    <img
                        src={platillo.imagen}
                        alt={platillo.descripcionPlatillo}
                        className="platillo-img"
                    />
                    <div className="platillo-info">
                        <h3>{platillo.descripcionPlatillo}</h3>
                        <p><strong>Tipo:</strong> {platillo.tipoPlatillo}</p>
                        <p><strong>Precio base:</strong> ${platillo.precio / 100}</p>

                        <h4>Menús donde se encuentra:</h4>
                        <ul className="menus-lista">
                            {platillo.menus.map((menu, i) => (
                                <li key={i}>
                                    <strong>{menu.nombreMenu}:</strong> {menu.descripcionMenu} — ${menu.precioMenu / 100}
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default CartaPlatillo;
