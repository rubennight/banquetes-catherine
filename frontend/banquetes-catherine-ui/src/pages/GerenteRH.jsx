import React from 'react';
import { useAuth } from '../context/AuthContext';

const GerenteRH = () => {
  const { user } = useAuth();

  return (
    <div className="sub-dashboard-container">
      <h3>Gestión de Recursos Humanos</h3>
      <p>Bienvenido, {user?.usuario}. Aquí podrás gestionar el personal y recursos humanos.</p>
      {/* Aquí irá la lógica y los componentes para gestionar RH */}
      <div className="feature-section">
        <h4>Funcionalidades clave:</h4>
        <ul>
          <li>Ver y editar información de empleados.</li>
          <li>Gestionar la disponibilidad y horarios de empleados.</li>
          <li>Registrar nuevas contrataciones.</li>
          <li>Generar reportes de desempeño de personal.</li>
        </ul>
      </div>
    </div>
  );
};

export default GerenteRH; 