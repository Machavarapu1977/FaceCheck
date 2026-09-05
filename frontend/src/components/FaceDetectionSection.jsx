import React from 'react';
import { UserCheck, Binary, MousePointerClick } from 'lucide-react';

export default function FaceDetectionSection({ faceData, selectedFaceIndex, onFaceSelect }) {
  if (!faceData) return null;

  const { faces_detected_count, primary_face_bbox, all_faces, selected_face_index, embedding_generated, embedding_preview } = faceData;
  const activeFaceIdx = selectedFaceIndex ?? selected_face_index ?? 0;
  const activeBbox = all_faces && all_faces.length > 0 ? all_faces[activeFaceIdx] : primary_face_bbox;

  return (
    <div className="glass-card">
      <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <UserCheck size={20} color="var(--accent-cyan)" /> 2. Face Detection &amp; Embedding Generation
      </h2>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem' }}>
        {/* Faces Detected */}
        <div style={{ background: 'rgba(0,0,0,0.3)', padding: '1rem', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.825rem', marginBottom: '0.25rem' }}>Faces Detected</p>
          <p style={{ fontSize: '1.5rem', fontWeight: 700, color: faces_detected_count === 0 ? 'var(--accent-rose)' : 'var(--accent-cyan)' }}>
            {faces_detected_count}
          </p>
          {faces_detected_count === 0 && (
            <p style={{ fontSize: '0.75rem', color: 'var(--accent-rose)', marginTop: '0.25rem' }}>NO FACE DETECTED</p>
          )}
        </div>

        {/* Bounding Box Coordinates for Selected Face */}
        <div style={{ background: 'rgba(0,0,0,0.3)', padding: '1rem', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.825rem', marginBottom: '0.25rem' }}>
            Bounding Box — Face #{activeFaceIdx + 1}
          </p>
          {activeBbox ? (
            <p className="font-mono" style={{ fontSize: '0.875rem', color: 'var(--text-main)' }}>
              x: {activeBbox.x}, y: {activeBbox.y}, w: {activeBbox.width}, h: {activeBbox.height}
            </p>
          ) : (
            <p style={{ fontSize: '0.875rem' }}>None</p>
          )}
        </div>

        {/* Embedding Status */}
        <div style={{ background: 'rgba(0,0,0,0.3)', padding: '1rem', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.825rem', marginBottom: '0.25rem' }}>512-d Embedding Status</p>
          <span className="badge badge-success" style={{ marginTop: '0.25rem' }}>
            {embedding_generated ? 'Generated & L2 Normalized' : 'Pending'}
          </span>
          {embedding_generated && (
            <p style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: '0.4rem' }}>Dimensions: 512 | Metric: Cosine</p>
          )}
        </div>
      </div>

      {/* Multi-face selection UI */}
      {all_faces && all_faces.length > 1 && (
        <div style={{ marginTop: '1rem', background: 'rgba(96,165,250,0.07)', border: '1px solid rgba(96,165,250,0.25)', borderRadius: '10px', padding: '1rem' }}>
          <p style={{ fontSize: '0.825rem', color: 'var(--accent-blue)', marginBottom: '0.6rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <MousePointerClick size={14} /> {all_faces.length} faces detected — select one to search:
          </p>
          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            {all_faces.map((bbox, i) => (
              <button
                key={i}
                onClick={() => onFaceSelect && onFaceSelect(i)}
                style={{
                  padding: '0.4rem 0.85rem',
                  borderRadius: '8px',
                  fontSize: '0.8rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                  border: activeFaceIdx === i
                    ? '2px solid var(--accent-blue)'
                    : '1px solid var(--border)',
                  background: activeFaceIdx === i
                    ? 'rgba(96,165,250,0.2)'
                    : 'rgba(0,0,0,0.3)',
                  color: activeFaceIdx === i ? 'var(--accent-blue)' : 'var(--text-muted)',
                  transition: 'all 0.2s ease',
                }}
              >
                Face #{i + 1}
              </button>
            ))}
          </div>
          <p style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: '0.5rem' }}>
            Selected: <strong style={{ color: 'var(--accent-blue)' }}>Face #{activeFaceIdx + 1}</strong>
            &nbsp;(x:{all_faces[activeFaceIdx]?.x}, y:{all_faces[activeFaceIdx]?.y},
            w:{all_faces[activeFaceIdx]?.width}, h:{all_faces[activeFaceIdx]?.height})
          </p>
        </div>
      )}

      {/* Embedding preview */}
      {embedding_preview && (
        <div style={{ marginTop: '1rem', background: 'rgba(0,0,0,0.4)', padding: '0.75rem 1rem', borderRadius: '8px' }}>
          <p style={{ fontSize: '0.775rem', color: 'var(--text-subtle)', marginBottom: '0.35rem', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
            <Binary size={14} /> Normalized Vector Sample (First 5 Dimensions):
          </p>
          <p className="hash-text">
            [{embedding_preview.map(n => n.toFixed(4)).join(', ')}, ...]
          </p>
        </div>
      )}
    </div>
  );
}
