import React, { useState, useEffect } from 'react';
import { FaUpload, FaUserFriends } from 'react-icons/fa';
import { RiSendPlaneFill } from 'react-icons/ri';
import './Header.css';
import Modal from 'react-modal';
import { useNavigate } from 'react-router-dom';

function Header() {
  const [showUploadForm, setShowUploadForm] = useState(false);
  const [showPeticiones, setShowPeticiones] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [documents, setDocuments] = useState([]);
  const [selectedDocuments, setSelectedDocuments] = useState([]);
  const [email, setEmail] = useState("");
  const navigate = useNavigate();

  const fetchDocuments = async () => {
    const data = {
      email: localStorage.getItem('email')
    };
    fetch('http://127.0.0.1:5002/doc/getAll', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + localStorage.getItem('token')
      },
      body: JSON.stringify(data)
    })
      .then(response => {
        return response.json();
      })
      .then(data => {
        setDocuments(data);
      })
      .catch(error => {
        console.error(error);
      });

    console.log(JSON.stringify(data));
  };
  useEffect(() => {
    fetchDocuments();
  }, []);


  const handleUploadClick = () => {
    setShowUploadForm(!showUploadForm);
  };

  const handleCloseUpload = () => {
    setShowUploadForm(false);
  };

  const handleUploadSubmit = (event) => {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    formData.append('email', email);
    formData.append('sender', email);

    fetch('http://127.0.0.1:5002/doc/delete', {
      method: 'POST',
      headers: {
        'Content-Type': 'multipart/form-data',
        authorization: localStorage.getItem('token')
      },
      body: formData
    })
      .then(response => {
      })
      .then(data => {
        if (data.hasOwnProperty("msg")) {
          alert(data.msg);
        } else {
          alert("Archivo subido correctamente");
          fetchDocuments();
        }
      })
      .catch(error => {
        console.error(error);
      });
    setShowUploadForm(false);
  };

  const handleMailModal = () => {
    setShowModal(!showModal);
  }

  const handleDocumentSelect = (event) => {
    const selectedDocumentIds = Array.from(event.target.selectedOptions, (option) => option.value);
    const selectedDocs = documents.filter((doc) => selectedDocumentIds.includes(doc.id.toString()));
    setSelectedDocuments(selectedDocs);
  };

  const handleEmailchange = (event) => {

    setEmail(event.target.value);
  };

  const handleModalClose = () => {
    setShowModal(false);
    setSelectedDocuments([]);
    setEmail("");
  };

  const handleSendEmail = () => {
    const links = selectedDocuments.map(objeto => objeto.s3_list);
    const data = {
      sender: localStorage.getItem('email'),
      links,
      owner: email
    };
    fetch('http://127.0.0.1:5002/doc/getAll', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    })
      .then(response => {
        if (response.status == 201){
          alert("Envio exitoso");
        } else {
          alert("Envio fallido");
        }
        return response.json();
      })
      .then(data => {
      })
      .catch(error => {
        console.error(error);
      });

    handleModalClose();
  };

  const handlePeticiones = () => {
    setShowPeticiones(!showPeticiones);
  };

  const handleLogOut = () => {
    localStorage.removeItem('token');
    navigate('/');
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
                    <button className="close-button" onClick={handleCloseUpload}>
                      Cerrar
                    </button>
                  </form>
                </div>
              </div>
            )}
          </li>
          <li className="nav-item">
            <a href="#" className="nav-link" onClick={handleMailModal}>
              <RiSendPlaneFill className="nav-icon" />
              Enviar
            </a>
          </li>
          <li className="nav-item">
            <a href="#" className="nav-link" onClick={handlePeticiones}>
              <FaUserFriends className="nav-icon" />
              Peticiones
            </a>
            {showPeticiones && (
              <div className="peticiones-container">
                <div className="peticion-form">
                  <form onSubmit={handleUploadSubmit}>
                    <input type="file" accept=".pdf" />
                    <button type="submit">Subir</button>
                    <button className="close-button" onClick={handleCloseUpload}>
                      Cerrar
                    </button>
                  </form>
                </div>
              </div>
            )}
          </li>
        </ul>
        <button className='handleLogOut' onClick={handleLogOut}>Cerrar sesion</button>
      </nav>
      <Modal
        isOpen={showModal}
        onRequestClose={handleModalClose}
        contentLabel="Seleccionar documentos"
        className="modal"
        shouldCloseOnOverlayClick={true}
      >
        <div className="modal-mail-content">
          <h3>Seleccionar documentos</h3>
          <select className="document-select" multiple onChange={handleDocumentSelect}>
            {documents.map((doc) => (
              <option key={doc.id} value={doc.id}>
                {doc.title}
              </option>
            ))}
          </select>
          <input type="email" value={email} onChange={handleEmailchange} className="email-input" placeholder="Correo electrónico" />
          <button className="send-button" onClick={handleSendEmail}>
            Enviar por correo
          </button>
          <button className="close-mail-button" onClick={handleModalClose}>
            Cerrar
          </button>
        </div>


      </Modal>
    </header>
  );
}

export default Header;




