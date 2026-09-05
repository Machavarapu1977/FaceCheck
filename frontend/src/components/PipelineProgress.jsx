import React from 'react';
import { Check } from 'lucide-react';

export default function PipelineProgress({ stages, currentStage }) {
  const currentIndex = stages.findIndex(s => s.key === currentStage);

  return (
    <div style={{
      background: 'var(--card-bg)',
      border: '1px solid var(--border)',
      borderRadius: '16px',
      padding: '1.25rem 1.5rem',
      marginBottom: '1.5rem',
      overflowX: 'auto',
    }}>
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '0',
        minWidth: 'max-content',
      }}>
        {stages.map((stage, i) => {
          const isDone = i < currentIndex;
          const isActive = i === currentIndex;
          const isPending = i > currentIndex;

          return (
            <React.Fragment key={stage.key}>
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.4rem' }}>
                {/* Circle */}
                <div style={{
                  width: '32px',
                  height: '32px',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '0.7rem',
                  fontWeight: 700,
                  flexShrink: 0,
                  border: isActive
                    ? '2px solid var(--accent-blue)'
                    : isDone
                    ? '2px solid var(--accent-green, #10b981)'
                    : '2px solid var(--border)',
                  background: isActive
                    ? 'rgba(96, 165, 250, 0.2)'
                    : isDone
                    ? 'rgba(16, 185, 129, 0.2)'
                    : 'transparent',
                  color: isActive
                    ? 'var(--accent-blue)'
                    : isDone
                    ? '#10b981'
                    : 'var(--text-muted)',
                  boxShadow: isActive ? '0 0 12px rgba(96,165,250,0.4)' : 'none',
                  transition: 'all 0.3s ease',
                }}>
                  {isDone ? <Check size={14} /> : i + 1}
                </div>
                {/* Label */}
                <span style={{
                  fontSize: '0.6rem',
                  fontWeight: isActive ? 700 : 500,
                  letterSpacing: '0.04em',
                  color: isActive
                    ? 'var(--accent-blue)'
                    : isDone
                    ? '#10b981'
                    : 'var(--text-muted)',
                  textAlign: 'center',
                  maxWidth: '72px',
                  lineHeight: 1.2,
                  transition: 'color 0.3s ease',
                }}>
                  {stage.label}
                </span>
              </div>

              {/* Connector line */}
              {i < stages.length - 1 && (
                <div style={{
                  height: '2px',
                  width: '40px',
                  flexShrink: 0,
                  marginBottom: '18px',
                  background: i < currentIndex
                    ? '#10b981'
                    : 'var(--border)',
                  transition: 'background 0.3s ease',
                }} />
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
}
