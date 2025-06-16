import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const SignUpForm = () => {
  const [formData, setFormData] = useState({
    usuario: '',
    email: '',
    password: '',
    confirmPassword: '',
    tipo_usuario: 'CLIENTE' // Valor por defecto
  });
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (formData.password !== formData.confirmPassword) {
      alert('Las contraseñas no coinciden');
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/usuarios', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          usuario: formData.usuario,
          email: formData.email,
          password: formData.password,
          tipo_usuario: formData.tipo_usuario,
          activo: 'S'
        })
      });

      if (response.ok) {
        alert('Registro exitoso');
        navigate('/login');
      } else {
        const data = await response.json();
        alert(data.error || 'Error en el registro');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error al conectar con el servidor');
    }
  };

  return (
    <form className="signup-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <input
          type="text"
          name="usuario"
          placeholder="Usuario"
          value={formData.usuario}
          onChange={handleChange}
          required
        />
      </div>
      <div className="form-group">
        <input
          type="email"
          name="email"
          placeholder="Correo electrónico"
          value={formData.email}
          onChange={handleChange}
          required
        />
      </div>
      <div className="form-group">
        <input
          type="password"
          name="password"
          placeholder="Contraseña"
          value={formData.password}
          onChange={handleChange}
          required
        />
      </div>
      <div className="form-group">
        <input
          type="password"
          name="confirmPassword"
          placeholder="Confirmar contraseña"
          value={formData.confirmPassword}
          onChange={handleChange}
          required
        />
      </div>
      <div className="form-group">
        <select
          name="tipo_usuario"
          value={formData.tipo_usuario}
          onChange={handleChange}
          className="tipo-usuario-select"
          required
        >
          <option value="CLIENTE">Cliente</option>
          <option value="GERENTE_CUENTAS">Gerente de Cuentas</option>
          <option value="GERENTE_EVENTOS">Gerente de Eventos</option>
          <option value="GERENTE_RH">Gerente de RH</option>
        </select>
      </div>
      <button type="submit" className="signup-button">
        Registrarse
      </button>
      <p className="login-link">
        ¿Ya tienes una cuenta? <a href="/login">Inicia sesión aquí</a>
      </p>
    </form>
  );
};

export default SignUpForm; 