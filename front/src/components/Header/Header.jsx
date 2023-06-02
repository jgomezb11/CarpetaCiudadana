import React from 'react';
import { FaDownload, FaUpload, FaBell, FaUserFriends } from 'react-icons/fa';
import './Header.css';

function Header() {
  return (
    <header className="header">
      <nav className="navbar">
        <ul className="nav-menu">
          <li className="nav-item">
            <a href="#" className="nav-link">
              <FaUpload className="nav-icon" />
              Subir
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
