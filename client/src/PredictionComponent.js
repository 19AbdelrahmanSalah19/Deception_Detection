import React, { useState } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Modal, Button } from 'react-bootstrap';

function PredictionComponent() {
    const [uploadResult, setUploadResult] = useState(null);
    const [captureResult, setCaptureResult] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [capturing, setCapturing] = useState(false);
    const [error, setError] = useState(null);
    const [videoFile, setVideoFile] = useState(null);
    const [showUploadModal, setShowUploadModal] = useState(false);
    const [showCaptureModal, setShowCaptureModal] = useState(false);

    // Handle file input change
    const handleFileChange = (event) => {
        setVideoFile(event.target.files[0]);
    };

    // Handle prediction using the uploaded video file
    const handleUploadAndPredict = async () => {
        if (!videoFile) {
            setError('Please select a video file.');
            return;
        }
        if (uploading) return; // Prevent multiple submissions
        setUploading(true);
        setError(null);
        const formData = new FormData();
        formData.append('video', videoFile);

        try {
            const response = await axios.post('http://localhost:5000/insertpredict', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            const data = response.data;
            setUploadResult(data);
            setShowUploadModal(true);
        } catch (error) {
            console.error('Error:', error);

            // Debugging information
            if (error.response) {
                console.log('Error response data:', error.response.data);
                console.log('Error response status:', error.response.status);
                console.log('Error response headers:', error.response.headers);
            } else if (error.request) {
                console.log('Error request:', error.request);
            } else {
                console.log('Error message:', error.message);
            }

            setError('An error occurred while making the request.');
        } finally {
            setUploading(false);
        }
    };

    // Handle video capture and prediction
    const handleCaptureAndPredict = async () => {
        if (capturing) return; // Prevent multiple submissions
        setCapturing(true);
        setError(null);
        try {
            const response = await axios.post('http://localhost:5000/capture_and_predict');
            const data = response.data;
            setCaptureResult(data);
            setShowCaptureModal(true);
        } catch (error) {
            console.error('Error:', error);

            // Debugging information
            if (error.response) {
                console.log('Error response data:', error.response.data);
                console.log('Error response status:', error.response.status);
                console.log('Error response headers:', error.response.headers);
            } else if (error.request) {
                console.log('Error request:', error.request);
            } else {
                console.log('Error message:', error.message);
            }

            setError('An error occurred while making the request.');
        } finally {
            setCapturing(false);
        }
    };

    return (
        <div className="container my-4">
            <h3 className="text-center">Capture Video and Predict Action</h3>
            <div className="d-flex justify-content-center my-3">
                <Button
                    variant="primary"
                    onClick={handleCaptureAndPredict}
                    disabled={capturing}
                >
                    {capturing ? 'Loading...' : 'Capture and Predict'}
                </Button>
            </div>
            {error && <p className="text-danger text-center">{error}</p>}
            <hr className="my-4" />
            <h3 className="text-center">Upload Video File and Predict Action</h3>
            <div className="d-flex justify-content-center my-3">
                <input type="file" accept="video/mp4" onChange={handleFileChange} className="form-control-file mr-2" />
                <Button
                    variant="primary"
                    onClick={handleUploadAndPredict}
                    disabled={uploading}
                >
                    {uploading ? 'Loading...' : 'Upload and Predict'}
                </Button>
            </div>
            {error && <p className="text-danger text-center">{error}</p>}

            {/* Capture Prediction Modal */}
            <Modal show={showCaptureModal} onHide={() => setShowCaptureModal(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>Capture Prediction Result</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    {captureResult && (
                        <div>
                            <p>
                                Action: <span style={{ color: captureResult.action === 'lie' ? 'red' : 'green' }}>
                                    {captureResult.action.charAt(0).toUpperCase() + captureResult.action.slice(1)}
                                </span>
                            </p>
                            <p>Confidence: {(captureResult.confidence * 100).toFixed(2)}%</p>
                        </div>
                    )}
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setShowCaptureModal(false)}>
                        Close
                    </Button>
                </Modal.Footer>
            </Modal>

            {/* Upload Prediction Modal */}
            <Modal show={showUploadModal} onHide={() => setShowUploadModal(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>Upload Prediction Result</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    {uploadResult && (
                        <div>
                            <p>
                                Action: <span style={{ color: uploadResult.action === 'lie' ? 'red' : 'green' }}>
                                    {uploadResult.action.toUpperCase()}
                                </span>
                            </p>
                            <p>Confidence: {(uploadResult.confidence * 100).toFixed(2)}%</p>
                        </div>
                    )}
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setShowUploadModal(false)}>
                        Close
                    </Button>
                </Modal.Footer>
            </Modal>
        </div>
    );
}

export default PredictionComponent;