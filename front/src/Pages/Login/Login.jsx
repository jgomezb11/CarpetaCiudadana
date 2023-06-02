import React, { useState } from 'react';
import './Login.css';

function Login() {
  const [name, setName] = useState('');
  const [documentId, setDocumentId] = useState(null);
  const [address, setAddress] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showRegister, setShowRegister] = useState(true);

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
    const data = {
      email,
      password,
      name,
      address,
      id: documentId
    };
    fetch('http://127.0.0.1:5002/user/registerUser', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
      .then(response => {
        return response.json();
      })
      .then(data => {
        if (data.hasOwnProperty("msg")) {
          alert('msg');
        } else {
          alert('Registro exitoso');
          toggleShowRegister();
        }
      })
      .catch(error => {
        console.error(error);
      });

    console.log(JSON.stringify(data));
  };

  const handleLoginSubmit = async (event) => {
    event.preventDefault();
    const data = {
      email,
      password
    };
    fetch('http://127.0.0.1:5002/user/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
      .then(response => {
        const statusCode = response.status;
        if (statusCode === 400) {
          alert("No dejes campos en blanco");
        } else if (statusCode === 401) {
          alert("Email o contraseña incorrecta");
        } else if (statusCode === 200) {
          //Redijire al HomePage
        }
        return response.json();
      })
      .then(data => {
        localStorage.setItem('token', data.access_token);
      })
      .catch(error => {
        console.error(error);
      });

    console.log(JSON.stringify(data));
  };

  const toggleShowRegister = () => {
    setShowRegister(!showRegister);
    setName(null);
    setDocumentId(null);
    setAddress(null);
    setEmail(null);
    setPassword(null);
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
          <p>
            ¿Ya tienes una cuenta? <button onClick={toggleShowRegister}>Inicia sesión</button>
          </p>
        </div>
      )}
    </div>
  );
}

export default Login;

