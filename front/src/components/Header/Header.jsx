import React, { useState, useEffect, useReducer } from 'react';
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
  const [ignored, forceUpdate] = useReducer(x => x + 1, 0);

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
  }, [ignored]);


  const handleUploadClick = () => {
    setShowUploadForm(!showUploadForm);
  };

  const handleCloseUpload = () => {
    setShowUploadForm(false);
  };

  const [file, setFile] = useState(null);

  const handleUploadSubmit = (event) => {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const fileField = document.querySelector('input[type="file"]');
    formData.append('file', fileField.files[0]);
    formData.append('email', localStorage.getItem('email'));
    formData.append('sender', localStorage.getItem('email'));

    for (let [key, value] of formData.entries()) { 
      console.log(key, value);
    }
    fetch('http://127.0.0.1:5002/doc/createDoc', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + localStorage.getItem('token')
      },
      body: formData
    })
    .then(response => {
      console.log(response);
      return response.json();
    })
    .then(data => {
      if (data.hasOwnProperty("msg")) {
        alert(data.msg);
      } else {
        alert("Archivo subido correctamente");
        forceUpdate();
      }
    })
    .catch(error => {
      console.error(error);
    });
    setShowUploadForm(false);
  };

  const handleFileChange = (event) => {
    setFile(event.target.files[0]); 
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
    const links = selectedDocuments.map(objeto => objeto.s3_link);
    const data = {
      sender: localStorage.getItem('email'),
      links,
      owner: email
    };
    fetch('http://127.0.0.1:5002/doc/sendDocs', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + localStorage.getItem('token')

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
    localStorage.removeItem('token')
    localStorage.removeItem('email');
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
                    <input type="file" name="file" accept=".pdf" onChange={handleFileChange} />
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
                {doc.name}
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




