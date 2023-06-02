import React, { useState } from 'react';
import { FaUpload, FaUserFriends } from 'react-icons/fa';
import { RiSendPlaneFill } from 'react-icons/ri';
import './Header.css';

function Header() {
  const [showUploadForm, setShowUploadForm] = useState(false);

  const handleUploadClick = () => {
    setShowUploadForm(true);
  };

  const handleCloseClick = () => {
    setShowUploadForm(false);
  };

  const handleUploadSubmit = (event) => {
    event.preventDefault();
    // Lógica para enviar el archivo al API
    setShowUploadForm(false);
  };

  return (
    <header className="header">
      <nav className="navbar">
        <ul className="nav-menu">
          <li className="nav-item">
            <a href="#" className="nav-link" onClick={handleUploadClick}>
              <FaUpload className="nav-icon" />
              Subir
            </a>
            {showUploadForm && (
              <div className="upload-form-container">
                <div className="upload-form">
                  <form onSubmit={handleUploadSubmit}>
                    <input type="file" accept=".pdf" />
                    <button type="submit">Subir</button>
                    <button className="close-button" onClick={handleCloseClick}>
                    Cerrar
                  </button>
                  </form>
                </div>
              </div>
            )}
          </li>
          <li className="nav-item">
            <a href="#" className="nav-link">
              <RiSendPlaneFill className="nav-icon" />
              Enviar
            </a>
          </li>
          <li className="nav-item">
            <a href="#" className="nav-link">
              <FaUserFriends className="nav-icon" />
              Peticiones
            </a>
          </li>
        </ul>
      </nav>
    </header>
  );
}

export default Header;




