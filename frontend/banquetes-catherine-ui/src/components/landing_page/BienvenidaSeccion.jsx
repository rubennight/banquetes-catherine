import banner from '../../assets/images/banquetes-catherine.png';

const BienvenidaSeccion = () => {
    return(
        <div className="bienvenida-section-container">
            <div className="bienvenida-contenido">
                <img 
                    src={banner} 
                    alt="Banquetes Catherine"
                    className="bienvenida-imagen"
                />
                <div className="bienvenida-texto-container">
                    <h3 className="bienvenida-texto">
                        Descubre el arte de celebrar:<br />
                        donde cada evento se convierte<br />
                        en un momento inolvidable
                    </h3>
                </div>
            </div>
        </div>
    )
}

export default BienvenidaSeccion;