import { useState, useEffect } from 'react';
import './index.css';
import banner from './assets/images/roasted-chicken-dinner-platter-delicious-feast.png';
import CartaPlatillo from './components/cartas/CartaPlatillo';

function App() {
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div>
      <header className={`header ${isScrolled ? 'scrolled' : ''}`}>
        <div className="header-content">
          <button className="text-button">Inicio</button>
          <button className="text-button">Menú</button>
          <button className="text-button">Contacto</button>
        </div>
      </header>
      
      <div className="hero-section-container">
        <div className="hero-section slide-in" style={{ backgroundImage: `url(${banner})` }} />
        
        <div className="hero-description">
          <h2>Bienvenidos a Banquetes Catherine</h2>
          <p>Ofrecemos servicios personalizados para tus eventos más importantes. Descubre nuestra carta y déjate sorprender.</p>
          <button className='text-button-get-started'>Cotiza tu evento</button>
          <button className='text-button-get-started' style={{ background: "#B9C651"}}>Soy colaborador</button>
        </div>
      </div>
      <div className="content-section">
        {/* Contenido de ejemplo para hacer scroll */}
        <CartaPlatillo />
      </div>
    </div>
  );
}

export default App;