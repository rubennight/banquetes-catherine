import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const LoginForm = () => {
  const [formData, setFormData] = useState({
    usuario: '',
    password: ''
  });
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5000/usuarios/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        const data = await response.json();
        login(data);

        switch (data.tipo_usuario) {
          case 'CLIENTE':
            navigate('/cliente-dashboard');
            break;
          case 'GERENTE_CUENTAS':
          case 'GERENTE_EVENTOS':
          case 'GERENTE_RH':
            navigate('/gerente-dashboard');
            break;
          default:
            navigate('/');
        }

      } else {
        const errorData = await response.json();
        alert(errorData.error || 'Error en el inicio de sesión. Por favor, verifica tus credenciales.');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error al conectar con el servidor.');
    }
  };

  return (
    <form className="login-form" onSubmit={handleSubmit}>
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
          type="password"
          name="password"
          placeholder="Contraseña"
          value={formData.password}
          onChange={handleChange}
          required
        />
      </div>
      <button type="submit" className="login-button">
        Iniciar Sesión
      </button>
      <p className="signup-link">
        ¿No tienes una cuenta? <a href="/signup">Regístrate aquí</a>
      </p>
    </form>
  );
};

export default LoginForm;
