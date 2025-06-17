import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import EventoService from '../../API/classes/EventoService';
import EmpleadoService from '../../API/classes/EmpleadoService';

const GerenteEventos = () => {
  const { user } = useAuth();
  const [eventos, setEventos] = useState([]);
  const [empleados, setEmpleados] = useState([]);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [selectedEmployee, setSelectedEmployee] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Obtener eventos pendientes o próximos
        const eventosData = await EventoService.obtenerEventosPendientes(); // Necesitas implementar este método en EventoService
        setEventos(eventosData);

        // Obtener empleados disponibles (por ejemplo, aquellos que pueden ser asignados a eventos)
        const empleadosData = await EmpleadoService.obtenerEmpleadosDisponibles(); // Necesitas implementar este método en EmpleadoService
        setEmpleados(empleadosData);
      } catch (err) {
        console.error("Error al cargar datos para gerente de eventos:", err);
        setError('No se pudieron cargar los datos necesarios.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleAssignEmployee = async () => {
    if (selectedEvent && selectedEmployee) {
      try {
        // Lógica para asignar empleado al evento
        // Asume que hay un endpoint como /eventos/{id}/asignar-empleado
        await EventoService.asignarEmpleadoAEvento(selectedEvent.id_evento, selectedEmployee); // Necesitas implementar este método
        alert(`Empleado ${selectedEmployee} asignado al evento ${selectedEvent.id_evento} exitosamente.`);
        // Refrescar la lista de eventos o actualizar el estado
        setSelectedEvent(null);
        setSelectedEmployee('');
        // Recargar datos para ver el cambio
        const eventosData = await EventoService.obtenerEventosPendientes();
        setEventos(eventosData);
      } catch (err) {
        console.error("Error al asignar empleado:", err);
        alert('Error al asignar empleado.');
      }
    } else {
      alert('Por favor, selecciona un evento y un empleado.');
    }
  };

  if (loading) {
    return <div className="sub-dashboard-container">Cargando datos de eventos...</div>;
  }

  if (error) {
    return <div className="sub-dashboard-container error-message">Error: {error}</div>;
  }

  return (
    <div className="sub-dashboard-container">
      <h3>Gestión de Eventos</h3>
      <p>Bienvenido, {user?.usuario}. Aquí podrás asignar empleados a eventos.</p>

      <div className="feature-section">
        <h4>Eventos Pendientes:</h4>
        {eventos.length === 0 ? (
          <p>No hay eventos pendientes de asignación.</p>
        ) : (
          <div className="events-list">
            {eventos.map(evento => (
              <div
                key={evento.id_evento}
                className={`event-card ${selectedEvent?.id_evento === evento.id_evento ? 'selected' : ''}`}
                onClick={() => setSelectedEvent(evento)}
              >
                <h5>Evento #{evento.id_evento} - {evento.tipo_evento}</h5>
                <p>Fecha: {new Date(evento.fecha_evento).toLocaleDateString()}</p>
                <p>Descripción: {evento.descripcion}</p>
              </div>
            ))}
          </div>
        )}
      </div>

      {selectedEvent && (
        <div className="assignment-section">
          <h4>Asignar empleado a Evento #{selectedEvent.id_evento}:</h4>
          <select
            value={selectedEmployee}
            onChange={(e) => setSelectedEmployee(e.target.value)}
            className="select-employee"
          >
            <option value="">Selecciona un empleado</option>
            {empleados.map(empleado => (
              <option key={empleado.id_empleado} value={empleado.id_empleado}>
                {empleado.nombre} {empleado.apellido} ({empleado.puesto})
              </option>
            ))}
          </select>
          <button onClick={handleAssignEmployee} className="assign-button">Asignar Empleado</button>
        </div>
      )}

      {/* Aquí puedes añadir otras funcionalidades de gestión de eventos */}
    </div>
  );
};

export default GerenteEventos; 