import { useState, useEffect } from 'react';
import './index.css';
import CartaPlatillo from './components/cartas/CartaPlatillo';
import UltimaSeccion from './components/landing_page/UltimaSeccion';
import MenuSeccion from './components/landing_page/MenuSeccion';
import BienvenidaSeccion from './components/landing_page/BienvenidaSeccion';

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
      <BienvenidaSeccion />

      <MenuSeccion />

      <UltimaSeccion />
    </div>
  );
}

export default App;