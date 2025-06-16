import { useState } from 'react';
import banner from '../assets/images/roasted-chicken-dinner-platter-delicious-feast.png';
import './UltimaSeccion.css';
import ModalLogin from './UltimaSeccionModalLogin';

const UltimaSeccion = () => {
    const [mostrarModal, setMostrarModal] = useState(false);

    return (
        <div className="ultima-section-container">
            <div
                className="ultima-banner slide-in"
                style={{ backgroundImage: `url(${banner})` }}
            />

            <div className="ultima-description">
                <h2>Bienvenidos a Banquetes Catherine</h2>
                <p>
                    Ofrecemos servicios personalizados para tus eventos más importantes.
                    Descubre nuestra carta y déjate sorprender.
                </p>
                <div className="ultima-buttons">
                    <button
                        className="text-button-get-started"
                        onClick={() => setMostrarModal(true)}
                    >
                        Cotiza tu evento
                    </button>
                    <button
                        className="text-button-get-started"
                        style={{ background: "#B9C651" }}
                    >
                        Soy colaborador
                    </button>
                </div>
            </div>

            {mostrarModal && <ModalLogin cerrarModal={() => setMostrarModal(false)} />}
        </div>
    );
};

export default UltimaSeccion;
