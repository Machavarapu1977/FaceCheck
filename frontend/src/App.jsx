import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Header from './components/Header';
import UploadSection from './components/UploadSection';
import FaceDetectionSection from './components/FaceDetectionSection';
import ReverseSearchSection from './components/ReverseSearchSection';
import BlockchainSection from './components/BlockchainSection';
import VerificationModal from './components/VerificationModal';
import PipelineProgress from './components/PipelineProgress';
import { AlertCircle } from 'lucide-react';

const STAGES = [
  { key: 'upload', label: 'UPLOAD' },
  { key: 'face_detection', label: 'FACE DETECTION' },
  { key: 'embedding', label: 'EMBEDDING' },
  { key: 'reverse_search', label: 'REVERSE IMAGE SEARCH' },
  { key: 'match_validation', label: 'MATCH VALIDATION' },
  { key: 'blockchain', label: 'BLOCKCHAIN' },
  { key: 'verified', label: 'VERIFIED' },
];

export default function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [resultData, setResultData] = useState(null);
  const [healthStatus, setHealthStatus] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedFaceIndex, setSelectedFaceIndex] = useState(0);
  const [currentStage, setCurrentStage] = useState(null);

  useEffect(() => {
    fetchHealth();
  }, []);

  const fetchHealth = async () => {
    try {
      const resp = await axios.get('/api/health');
      setHealthStatus(resp.data);
    } catch (err) {
      console.error('Failed to fetch system health:', err);
    }
  };

  const handleFileChange = (file) => {
    setSelectedFile(file);
    setError(null);
    setResultData(null);
    setCurrentStage(null);
    setSelectedFaceIndex(0);
    if (file) {
      setPreviewUrl(URL.createObjectURL(file));
      setCurrentStage('upload');
    } else {
      setPreviewUrl(null);
    }
  };

  const handleFaceSelect = (index) => {
    setSelectedFaceIndex(index);
  };

  const handleSubmit = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setError(null);
    setResultData(null);
    setCurrentStage('face_detection');

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('selected_face_index', selectedFaceIndex);

    try {
      setCurrentStage('embedding');
      // Small artificial pause so users can see the stage progress
      await new Promise(r => setTimeout(r, 400));
      setCurrentStage('reverse_search');

      const response = await axios.post('/api/verify', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      setCurrentStage('match_validation');
      await new Promise(r => setTimeout(r, 200));
      setCurrentStage('blockchain');
      await new Promise(r => setTimeout(r, 200));
      setCurrentStage('verified');
      setResultData(response.data);
    } catch (err) {
      setCurrentStage(null);
      const errDetail = err.response?.data?.detail;
      if (typeof errDetail === 'object' && errDetail.message) {
        setError(errDetail.message);
      } else if (typeof errDetail === 'string') {
        setError(errDetail);
      } else {
        setError(err.message || 'An unexpected error occurred during processing.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <Header
        demoMode={healthStatus?.demo_mode}
        provider={healthStatus?.services?.reverse_image_search_provider}
      />

      {currentStage && (
        <PipelineProgress stages={STAGES} currentStage={currentStage} />
      )}

      {error && (
        <div style={{
          background: 'rgba(244, 63, 94, 0.15)',
          border: '1px solid rgba(244, 63, 94, 0.3)',
          color: 'var(--accent-rose)',
          padding: '1rem 1.25rem',
          borderRadius: '12px',
          marginBottom: '1.5rem',
          display: 'flex',
          alignItems: 'center',
          gap: '0.75rem'
        }}>
          <AlertCircle size={20} />
          <div>
            <p style={{ fontWeight: 600 }}>Error</p>
            <p style={{ fontSize: '0.875rem' }}>{error}</p>
          </div>
        </div>
      )}

      <UploadSection
        selectedFile={selectedFile}
        previewUrl={previewUrl}
        onFileChange={handleFileChange}
        onSubmit={handleSubmit}
        loading={loading}
      />

      {resultData && (
        <>
          <FaceDetectionSection
            faceData={resultData.face}
            selectedFaceIndex={selectedFaceIndex}
            onFaceSelect={handleFaceSelect}
          />
          <ReverseSearchSection
            searchInfo={resultData.reverse_search}
            topCandidates={resultData.top_candidates}
            bestMatch={resultData.best_match}
          />
          <BlockchainSection
            hashes={resultData.hashes}
            blockchain={resultData.blockchain}
            onVerifyClick={() => setIsModalOpen(true)}
          />
        </>
      )}

      <VerificationModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        recordData={resultData}
      />
    </div>
  );
}
