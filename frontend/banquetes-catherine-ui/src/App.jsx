import { useState, useEffect } from 'react';
import './styles/global.css';
import UltimaSeccion from './components/UltimaSeccion';
import MenuCard from './components/MenuCard';
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
      <MenuCard />
      <UltimaSeccion />
    </div>
  );
}

export default App;
