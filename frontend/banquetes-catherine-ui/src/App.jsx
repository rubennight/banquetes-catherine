import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import './styles/global.css';
import UltimaSeccion from './components/UltimaSeccion';
import MenuCard from './components/MenuCard';
import BienvenidaSeccion from './components/BienvenidaSeccion';
import Login from './pages/Login';
import SignUp from './pages/SignUp';
import ClienteDashboard from './pages/ClienteDashboard';
import GerenteDashboard from './pages/GerenteDashboard';
import GerenteCuentas from './pages/GerenteCuentas';
import GerenteEventos from './pages/GerenteEventos';
import GerenteRH from './pages/GerenteRH';

function PrivateRoute({ children, allowedRoles }) {
  const { user } = useAuth();
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  if (allowedRoles && !allowedRoles.includes(user.tipo_usuario)) {
    return <Navigate to="/unauthorized" replace />;
  }
  return children;
}

function AppContent() {
  const [isScrolled, setIsScrolled] = useState(false);
  const { user, logout } = useAuth();

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const getDashboardPath = (tipo_usuario) => {
    switch (tipo_usuario) {
      case 'CLIENTE':
        return '/cliente-dashboard';
      case 'GERENTE_CUENTAS':
      case 'GERENTE_EVENTOS':
      case 'GERENTE_RH':
        return '/gerente-dashboard';
      default:
        return '/';
    }
  };

  return (
    <>
      <header className={`header ${isScrolled ? 'scrolled' : ''}`}>
        <div className="header-content">
          <button className="text-button">Inicio</button>
          <button className="text-button">Menú</button>
          <button className="text-button">Contacto</button>
          {user ? (
            <button className="text-button" onClick={logout}>Cerrar Sesión</button>
          ) : (
            <button className="text-button" onClick={() => navigate('/login')}>Iniciar Sesión</button>
          )}
          {user && (
            <button className="text-button" onClick={() => navigate(getDashboardPath(user.tipo_usuario))}>
              Mi Panel
            </button>
          )}
        </div>
      </header>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/" element={
          <div>
            <BienvenidaSeccion />
            <MenuCard />
            <UltimaSeccion />
          </div>
        } />

        {/* Rutas Protegidas */}
        <Route path="/cliente-dashboard" element={
          <PrivateRoute allowedRoles={['CLIENTE']}>
            <ClienteDashboard />
          </PrivateRoute>
        } />
        <Route path="/gerente-dashboard" element={
          <PrivateRoute allowedRoles={['GERENTE_CUENTAS', 'GERENTE_EVENTOS', 'GERENTE_RH']}>
            <GerenteDashboard />
          </PrivateRoute>
        } />
        <Route path="/gerente-dashboard/cuentas" element={
          <PrivateRoute allowedRoles={['GERENTE_CUENTAS']}>
            <GerenteCuentas />
          </PrivateRoute>
        } />
        <Route path="/gerente-dashboard/eventos" element={
          <PrivateRoute allowedRoles={['GERENTE_EVENTOS']}>
            <GerenteEventos />
          </PrivateRoute>
        } />
        <Route path="/gerente-dashboard/rh" element={
          <PrivateRoute allowedRoles={['GERENTE_RH']}>
            <GerenteRH />
          </PrivateRoute>
        } />
        <Route path="/unauthorized" element={<div>Acceso no autorizado</div>} />
      </Routes>
    </>
  );
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </Router>
  );
}

export default App;