import LoginForm from '../components/LoginForm';

const Login = () => {
  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-form-container">
          <h2>Iniciar Sesión</h2>
          <LoginForm />
        </div>
      </div>
    </div>
  );
};

export default Login;
