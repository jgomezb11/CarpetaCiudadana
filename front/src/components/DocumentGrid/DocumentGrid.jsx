import React, { useState, useEffect, useReducer } from 'react';
import Modal from 'react-modal';
import pdfLogo from './pdf-logo.png';
import './DocumentGrid.css';
import { AiFillDelete, AiOutlineDownload } from 'react-icons/ai';



const DocumentGrid = () => {
    const [documents, setDocuments] = useState([]);
    const [selectedDocument, setSelectedDocument] = useState(null);
    const [modalOpen, setModalOpen] = useState(false);
    const [ignored, forceUpdate] = useReducer(x => x + 1, 0);

    const fetchDocuments = async () => {
        const data = {
            email: localStorage.getItem('email')
        };
        fetch('http://3.220.28.150:5000/doc/getAll', {
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

    const handleDocumentClick = (document) => {
        setSelectedDocument(document);
        setModalOpen(true);
    };

    const closeModal = () => {
        setModalOpen(false);
    };

    const deleteDocument = (id) => {
        const data = {
            id
        };
        fetch('http://3.220.28.150:5000/doc/delDocument', {
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
        const timerId = setTimeout(() => {
            window.location.reload();
        }, 2000);


    };

    return (
        <div className="document-grid-container">
            <div className="document-grid">
                {documents.map((document) => (
                    <div
                        key={document.id}
                        className="document-item"
                        onClick={() => handleDocumentClick(document)}
                    >
                        <img src={pdfLogo} alt="PDF" />
                        <h4>{document.name}</h4>
                    </div>
                ))}
            </div>
            {selectedDocument && (
                <Modal
                    className="modal"
                    isOpen={modalOpen}
                    onRequestClose={closeModal}
                    shouldCloseOnOverlayClick={true}
                >
                    <div className="modal-content">
                        <h3>{selectedDocument.id}. {selectedDocument.name}</h3>
                        <p>El archivo se encuentra en la carpeta {selectedDocument.carpeta}</p>
                        <p>Fue subido el {selectedDocument.date_of_upload}</p>
                        <p>El correo de su dueño es {selectedDocument.owner}</p>
                        <p>El encargado de su validacion es {selectedDocument.sender}</p>
                        {selectedDocument.is_signed ? (<p>El documento ya fue firmado</p>) : (<p>El documento no ha sido firmado</p>)}
                        <button className="modal-close-button" onClick={closeModal}>
                            <span className="close-icon">&times;</span>
                        </button>
                        <button className="erase-button" onClick={() => deleteDocument(selectedDocument.id)}> <AiFillDelete /> Eliminar</button>
                        <a target="_blank" className="download-button" href={selectedDocument.s3_link}> <AiOutlineDownload /> Descargar</a>
                    </div>

                </Modal>
            )}
        </div>
    );
};

export default DocumentGrid;
