import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import EventoService from '../../API/classes/EventoService';

const ClienteDashboard = () => {
  const { user } = useAuth();
  const [eventos, setEventos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchEventos = async () => {
      if (user && user.id_usuario) {
        try {
          // Asumiendo que hay un endpoint para obtener eventos por ID de cliente/usuario
          // Podrías necesitar ajustar el servicio o el endpoint del backend
          const data = await EventoService.obtenerEventosPorCliente(user.id_usuario);
          setEventos(data);
        } catch (err) {
          console.error("Error al obtener eventos del cliente:", err);
          setError('No se pudieron cargar tus eventos.');
        } finally {
          setLoading(false);
        }
      } else {
        setLoading(false);
        setError('Usuario no autenticado o ID de usuario no disponible.');
      }
    };

    fetchEventos();
  }, [user]);

  if (loading) {
    return <div className="dashboard-container">Cargando eventos...</div>;
  }

  if (error) {
    return <div className="dashboard-container error-message">Error: {error}</div>;
  }

  return (
    <div className="dashboard-container">
      <h2>Bienvenido, {user?.usuario} ({user?.tipo_usuario})</h2>
      <h3>Mis Eventos/Pedidos</h3>
      {eventos.length === 0 ? (
        <p>No tienes eventos/pedidos registrados.</p>
      ) : (
        <div className="eventos-list">
          {eventos.map(evento => (
            <div key={evento.id_evento} className="evento-card">
              <h4>Evento #{evento.id_evento} - {evento.tipo_evento}</h4>
              <p>Fecha: {new Date(evento.fecha_evento).toLocaleDateString()}</p>
              <p>Descripción: {evento.descripcion}</p>
              <p>Estado: {evento.estado}</p>
              {/* Muestra más detalles del evento si es necesario */}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ClienteDashboard; 