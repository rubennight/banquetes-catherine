import React from 'react';
import { useAuth } from '../context/AuthContext';

const GerenteCuentas = () => {
  const { user } = useAuth();

  return (
    <div className="sub-dashboard-container">
      <h3>Gestión de Cuentas</h3>
      <p>Bienvenido, {user?.usuario}. Aquí podrás gestionar las cuentas de clientes.</p>
      {/* Aquí irá la lógica y los componentes para gestionar clientes/cuentas */}
      <div className="feature-section">
        <h4>Funcionalidades clave:</h4>
        <ul>
          <li>Ver listado de clientes y sus detalles.</li>
          <li>Actualizar información de clientes.</li>
          <li>Gestionar el estado de los clientes.</li>
          <li>Ver reportes de clientes.</li>
        </ul>
      </div>
    </div>
  );
};

export default GerenteCuentas; 