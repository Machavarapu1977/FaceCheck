import React, { useRef } from 'react';
import { Upload, Image as ImageIcon, CheckCircle2 } from 'lucide-react';

export default function UploadSection({ selectedFile, previewUrl, onFileChange, onSubmit, loading }) {
  const fileInputRef = useRef(null);

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onFileChange(e.dataTransfer.files[0]);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  return (
    <div className="glass-card">
      <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <ImageIcon size={20} color="var(--accent-blue)" /> 1. Upload Input Photograph
      </h2>

      <div className="grid-2">
        <div
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onClick={() => fileInputRef.current?.click()}
          style={{
            border: '2px dashed var(--border-accent)',
            borderRadius: '12px',
            padding: '2.5rem 1.5rem',
            textAlign: 'center',
            cursor: 'pointer',
            background: 'rgba(0, 0, 0, 0.2)',
            transition: 'background 0.2s ease'
          }}
        >
          <input
            type="file"
            ref={fileInputRef}
            onChange={(e) => e.target.files?.[0] && onFileChange(e.target.files[0])}
            accept=".jpg,.jpeg,.png"
            style={{ display: 'none' }}
          />
          <Upload size={40} color="var(--accent-blue)" style={{ marginBottom: '1rem' }} />
          <p style={{ fontWeight: 600, marginBottom: '0.25rem' }}>Click or drag photo here to upload</p>
          <p style={{ color: 'var(--text-subtle)', fontSize: '0.825rem' }}>Supports JPG, JPEG, and PNG (Max 10MB)</p>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', border: '1px solid var(--border-color)', borderRadius: '12px', padding: '1rem', background: 'rgba(0,0,0,0.1)' }}>
          {previewUrl ? (
            <div style={{ textAlign: 'center', width: '100%' }}>
              <img
                src={previewUrl}
                alt="Upload preview"
                style={{ maxHeight: '180px', maxWidth: '100%', borderRadius: '8px', objectFit: 'contain', marginBottom: '0.75rem', boxShadow: '0 4px 12px rgba(0,0,0,0.5)' }}
              />
              <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '0.75rem' }}>{selectedFile?.name}</p>
              <button
                className="btn-primary"
                onClick={onSubmit}
                disabled={loading}
                style={{ width: '100%', justifyContent: 'center' }}
              >
                {loading ? 'Processing Pipeline...' : 'Run Face Verification Pipeline'}
              </button>
            </div>
          ) : (
            <div style={{ textAlign: 'center', color: 'var(--text-subtle)' }}>
              <p>No image selected for preview</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
