import React from 'react';
import { ShieldCheck, Cpu, Database, Link as LinkIcon } from 'lucide-react';

export default function Header({ demoMode, provider }) {
  return (
    <header className="glass-card" style={{ marginBottom: '2rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.5rem' }}>
            <div style={{ padding: '0.5rem', background: 'rgba(59, 130, 246, 0.2)', borderRadius: '12px' }}>
              <ShieldCheck size={28} color="#3b82f6" />
            </div>
            <h1 style={{ fontSize: '1.75rem', fontWeight: 700, letterSpacing: '-0.02em' }}>
              Face ID <span style={{ color: 'var(--accent-blue)' }}>+</span> Blockchain Verification
            </h1>
          </div>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.925rem' }}>
            Cryptographically verifiable reverse image search and facial embedding provenance on EVM testnet.
          </p>
        </div>

        <div style={{ display: 'flex', gap: '0.75rem' }}>
          <span className="badge badge-info">
            <Cpu size={14} /> Provider: {provider || 'SerpAPI'}
          </span>
          <span className={`badge ${demoMode ? 'badge-info' : 'badge-success'}`}>
            <Database size={14} /> {demoMode ? 'DEMO MODE' : 'PRODUCTION PIPELINE'}
          </span>
        </div>
      </div>
    </header>
  );
}
