import React, { useState } from 'react';
import './Login.css';

function Login() {
  const [name, setName] = useState('');
  const [documentId, setDocumentId] = useState(null);
  const [address, setAddress] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showRegister, setShowRegister] = useState(true);
  const [isRegistered, setIsRegistered] = useState(false);

  const handleNameChange = (event) => {
    setName(event.target.value);
  };

  const handledocumentIdChange = (event) => {
    setDocumentId(event.target.value);
  };

  const handleAddressChange = (event) => {
    setAddress(event.target.value);
  };

  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleRegisterSubmit = (event) => {
    event.preventDefault();
    // Aquí puedes enviar la información de registro a tu API
    console.log('Register:', name, address, email, password);
    setIsRegistered(true);
  };

  const handleLoginSubmit = async (event) => {
    event.preventDefault();
    try { 
      const response = await fetch('API_URL', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: email,
          password: password
        }),
      });
    
      if (!response.ok) {
        throw new Error('Error al realizar la petición');
      }
    
      const resultData = await response.json();
      console.log(resultData.Result);
    } catch (error) {
      console.error('Error:', error);
      alert('Error:', error);
    }
    console.log('Login:', email, password);
  };

  const toggleShowRegister = () => {
    setShowRegister(!showRegister);
  };

  return (
    <div className="login-form">
      {!showRegister ? (
        <div className="login-container">
          <h2>Iniciar Sesión</h2>
          <form onSubmit={handleLoginSubmit}>
            <div className="form-group">
              <label>Correo electronico:</label>
              <input type="email" value={email} onChange={handleEmailChange} placeholder='Email@ejemplo.com' required />
            </div>
            <div className="form-group">
              <label>Contraseña:</label>
              <input type="password" value={password} onChange={handlePasswordChange} required />
            </div>
            <button type="submit">Iniciar sesión</button>
          </form>
          <p>
            ¿No tienes una cuenta? <button onClick={toggleShowRegister}>Registrate</button>
          </p>
        </div>
      ) : (
        <div className="register-container">
          <h2>Registro</h2>
          <form onSubmit={handleRegisterSubmit}>
            <div className="form-group">
              <label>Nombre:</label>
              <input type="text" value={name} onChange={handleNameChange} required />
            </div>
            <div className="form-group">
              <label>Cédula:</label>
              <input type="number" value={documentId} onChange={handledocumentIdChange} required />
            </div>
            <div className="form-group">
              <label>Dirección:</label>
              <input type="text" value={address} onChange={handleAddressChange} required />
            </div>
            <div className="form-group">
              <label>Coreo electronico:</label>
              <input type="email" value={email} onChange={handleEmailChange} placeholder='Email@ejemplo.com' required />
            </div>
            <div className="form-group">
              <label>Contraseña:</label>
              <input type="password" value={password} onChange={handlePasswordChange} required />
            </div>
            <button type="submit">Registrate</button>
          </form>
          {!isRegistered && (
            <p>
              ¿Ya tienes una cuenta? <button onClick={toggleShowRegister}>Inicia sesión</button>
            </p>
          )}

          {isRegistered && (
            <p>
              ¡Te registraste con exito! por favor <button onClick={toggleShowRegister}>Iniciar sesión</button> para continuar.
            </p>
          )}
        </div>
      )}
    </div>
  );
}

export default Login;

