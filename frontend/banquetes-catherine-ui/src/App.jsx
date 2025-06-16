import { useState, useEffect } from 'react';
import './index.css';
import CartaPlatillo from './components/CartaPlatillo';
import UltimaSeccion from './components/UltimaSeccion';
import MenuSeccion from './components/MenuSeccion';
import BienvenidaSeccion from './components/BienvenidaSeccion';

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