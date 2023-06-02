import React, { useState, useEffect } from 'react';
import Modal from 'react-modal';
import pdfLogo from './pdf-logo.png';
import './DocumentGrid.css';

const DocumentGrid = ({ userId }) => {
    const [documents, setDocuments] = useState([
        { id: 1, title: 'Documento 1', description: 'Descripción del documento 1' },
        { id: 2, title: 'Documento 2', description: 'Descripción del documento 2' },
        { id: 3, title: 'Documento 3', description: 'Descripción del documento 3' },
        { id: 4, title: 'Documento 4', description: 'Descripción del documento 4' },
        { id: 5, title: 'Documento 5', description: 'Descripción del documento 5' }
    ]);
    const [selectedDocument, setSelectedDocument] = useState(null);
    const [modalOpen, setModalOpen] = useState(false);

    const fetchDocuments = async () => {
        try {
            const response = await fetch('URL_DEL_API', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    // Datos del usuario para la petición POST
                    // ...
                }),
            });

            if (response.ok) {
                const data = await response.json();
                setDocuments(data);
            } else {
                console.error('Error al obtener los documentos:', response.statusText);
            }
        } catch (error) {
            console.error('Error al realizar la petición:', error);
        }
    };

    useEffect(() => {
        fetchDocuments();
    }, []);

    const handleDocumentClick = (document) => {
        setSelectedDocument(document);
        setModalOpen(true);
    };

    const closeModal = () => {
        setModalOpen(false);
    };

    const downloadDocument = (document) => {

    };

    const eraseDocument = (document) => {

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
                        <h4>{document.title}</h4>
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
                        <h3>{selectedDocument.title}</h3>
                        <p>{selectedDocument.description}</p>
                        <button className="close-button" onClick={closeModal}>
                            <span className="close-icon">&times;</span>
                        </button>
                        <button className="erase-button" onClick={eraseDocument}>Eliminar</button>
                        <button className="download-button" onClick={downloadDocument}>Descargar</button>
                    </div>

                </Modal>
            )}
        </div>
    );
};

export default DocumentGrid;
