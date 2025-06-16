import banner from '../assets/images/roasted-chicken-dinner-platter-delicious-feast.png';

const UltimaSeccion = () => {
    return(
        <div className="hero-section-container">
            <div className="hero-section slide-in" style={{ backgroundImage: `url(${banner})` }} />
            
            <div className="hero-description">
                <h2>Bienvenidos a Banquetes Catherine</h2>
                <p>Ofrecemos servicios personalizados para tus eventos más importantes. Descubre nuestra carta y déjate sorprender.</p>
                <button className='text-button-get-started'>Cotiza tu evento</button>
                <button className='text-button-get-started' style={{ background: "#B9C651"}}>Soy colaborador</button>
            </div>
        </div>
    )
}

export default UltimaSeccion;