import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './styles/global.css';
import UltimaSeccion from './components/UltimaSeccion';
import MenuCard from './components/MenuCard';
import BienvenidaSeccion from './components/BienvenidaSeccion';
import Login from './pages/Login';
import SignUp from './pages/SignUp';

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
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/" element={
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
        } />
      </Routes>
    </Router>
  );
}

export default App;