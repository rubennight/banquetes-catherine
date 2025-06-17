import React, { useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link, Outlet } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';

const GerenteDashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (user && user.tipo_usuario) {
      switch (user.tipo_usuario) {
        case 'GERENTE_CUENTAS':
          navigate('/gerente-dashboard/cuentas');
          break;
        case 'GERENTE_EVENTOS':
          navigate('/gerente-dashboard/eventos');
          break;
        case 'GERENTE_RH':
          navigate('/gerente-dashboard/rh');
          break;
        default:
          navigate('/unauthorized');
          break;
      }
    }
  }, [user, navigate]);

  return (
    <div className="dashboard-container">
      <h2>Bienvenido, {user?.usuario} ({user?.tipo_usuario})</h2>
      <h3>Panel de Gerencia</h3>
      <nav className="dashboard-nav">
        {user?.tipo_usuario === 'GERENTE_CUENTAS' && (
          <Link to="/gerente-dashboard/cuentas" className="dashboard-nav-link">Gestión de Cuentas</Link>
        )}
        {user?.tipo_usuario === 'GERENTE_EVENTOS' && (
          <Link to="/gerente-dashboard/eventos" className="dashboard-nav-link">Gestión de Eventos</Link>
        )}
        {user?.tipo_usuario === 'GERENTE_RH' && (
          <Link to="/gerente-dashboard/rh" className="dashboard-nav-link">Gestión de RH</Link>
        )}
      </nav>
      <div className="dashboard-content">
        {/* Outlet renderizará los componentes anidados (GerenteCuentas, GerenteEventos, GerenteRH) */}
        <Outlet />
        <p>Selecciona una opción del menú para comenzar.</p>
      </div>
    </div>
  );
};

export default GerenteDashboard; 