import React, { useState } from 'react';
import { ShieldCheck, ExternalLink, CheckCircle, XCircle, Loader } from 'lucide-react';
import axios from 'axios';

export default function BlockchainSection({ hashes, blockchain, onVerifyClick }) {
  if (!hashes) return null;

  const [verifyStatus, setVerifyStatus] = useState(null); // null | 'loading' | 'verified' | 'failed' | 'error'
  const [verifyMessage, setVerifyMessage] = useState('');

  const handleVerify = async () => {
    if (!blockchain?.record_id || !hashes) {
      setVerifyStatus('error');
      setVerifyMessage('Missing record data for on-chain verification.');
      return;
    }

    setVerifyStatus('loading');
    setVerifyMessage('');

    try {
      const response = await axios.post('/api/blockchain/verify', {
        record_id: blockchain.record_id,
        image_hash: hashes.image_hash,
        match_data_hash: hashes.match_data_hash,
        record_hash: hashes.record_hash,
      });

      if (response.data.is_valid) {
        setVerifyStatus('verified');
        setVerifyMessage(response.data.message || 'ON-CHAIN RECORD VERIFIED');
      } else {
        setVerifyStatus('failed');
        setVerifyMessage(response.data.message || 'VERIFICATION FAILED');
      }
    } catch (err) {
      setVerifyStatus('error');
      const detail = err.response?.data?.detail;
      setVerifyMessage(typeof detail === 'string' ? detail : 'Blockchain transaction could not be verified.');
    }
  };

  const HashRow = ({ label, value }) => (
    <div style={{ marginBottom: '0.85rem' }}>
      <p style={{ fontSize: '0.775rem', color: 'var(--text-muted)', marginBottom: '0.25rem' }}>{label}</p>
      <p className="hash-text" style={{ wordBreak: 'break-all', fontSize: '0.78rem' }}>{value}</p>
    </div>
  );

  return (
    <div className="glass-card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '0.75rem', marginBottom: '1.25rem' }}>
        <h2 style={{ fontSize: '1.25rem', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <ShieldCheck size={20} color="var(--accent-green, #10b981)" /> 4. Blockchain Record &amp; Cryptographic Hashes
        </h2>
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
          {/* Verify on-chain button */}
          <button
            onClick={handleVerify}
            disabled={verifyStatus === 'loading'}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
              padding: '0.5rem 1rem',
              borderRadius: '8px',
              background: 'rgba(16,185,129,0.15)',
              border: '1px solid rgba(16,185,129,0.4)',
              color: '#10b981',
              fontWeight: 600,
              fontSize: '0.82rem',
              cursor: verifyStatus === 'loading' ? 'not-allowed' : 'pointer',
              opacity: verifyStatus === 'loading' ? 0.7 : 1,
            }}
          >
            {verifyStatus === 'loading' ? <Loader size={14} className="spin" /> : <ShieldCheck size={14} />}
            Verify On-Chain Record
          </button>
        </div>
      </div>

      {/* Verification result banner */}
      {verifyStatus && verifyStatus !== 'loading' && (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.6rem',
          padding: '0.75rem 1rem',
          borderRadius: '10px',
          marginBottom: '1rem',
          background: verifyStatus === 'verified' ? 'rgba(16,185,129,0.12)' : 'rgba(244,63,94,0.12)',
          border: `1px solid ${verifyStatus === 'verified' ? 'rgba(16,185,129,0.35)' : 'rgba(244,63,94,0.35)'}`,
          color: verifyStatus === 'verified' ? '#10b981' : 'var(--accent-rose)',
          fontSize: '0.875rem',
          fontWeight: 700,
        }}>
          {verifyStatus === 'verified' ? <CheckCircle size={18} /> : <XCircle size={18} />}
          {verifyStatus === 'verified' ? '✓ ' : '✗ '}{verifyMessage}
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
        {/* Hashes column */}
        <div>
          <HashRow label="Input Image SHA-256 Hash" value={hashes.image_hash} />
          <HashRow label="Canonical Match Data Hash" value={hashes.match_data_hash} />
          <HashRow label="Combined Verification Record Hash" value={hashes.record_hash} />
        </div>

        {/* Blockchain receipt column */}
        {blockchain && (
          <div style={{ background: 'rgba(0,0,0,0.3)', borderRadius: '10px', padding: '1rem', border: '1px solid var(--border)' }}>
            <p style={{ fontWeight: 700, color: 'var(--accent-blue)', marginBottom: '0.85rem', display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.875rem' }}>
              <ShieldCheck size={14} /> EVM Testnet Receipt Details
            </p>

            <div style={{ display: 'grid', gap: '0.5rem', fontSize: '0.8rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-muted)' }}>Network:</span>
                <span style={{ fontWeight: 600, color: 'var(--accent-blue)' }}>{blockchain.network_name || `Chain ${blockchain.chain_id}`}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-muted)' }}>Chain ID:</span>
                <span style={{ fontWeight: 600 }}>{blockchain.chain_id}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-muted)' }}>Block Number:</span>
                <span style={{ fontWeight: 600 }}>#{blockchain.block_number}</span>
              </div>
            </div>

            <div style={{ marginTop: '0.75rem' }}>
              <p style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginBottom: '0.2rem' }}>Tx Hash:</p>
              <p className="hash-text" style={{ fontSize: '0.72rem', wordBreak: 'break-all' }}>{blockchain.transaction_hash}</p>
            </div>

            <div style={{ marginTop: '0.75rem' }}>
              <p style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginBottom: '0.2rem' }}>On-Chain Record ID:</p>
              <p className="hash-text" style={{ fontSize: '0.72rem', wordBreak: 'break-all' }}>{blockchain.record_id}</p>
            </div>

            {blockchain.contract_address && (
              <div style={{ marginTop: '0.75rem' }}>
                <p style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginBottom: '0.2rem' }}>Contract:</p>
                <p className="hash-text" style={{ fontSize: '0.72rem', wordBreak: 'break-all' }}>{blockchain.contract_address}</p>
              </div>
            )}

            {/* Blockchain explorer link */}
            {blockchain.explorer_url && (
              <a
                href={blockchain.explorer_url}
                target="_blank"
                rel="noopener noreferrer"
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '0.4rem',
                  marginTop: '1rem',
                  padding: '0.45rem 0.85rem',
                  borderRadius: '8px',
                  background: 'rgba(96,165,250,0.15)',
                  color: 'var(--accent-blue)',
                  fontSize: '0.78rem',
                  fontWeight: 600,
                  border: '1px solid rgba(96,165,250,0.3)',
                  textDecoration: 'none',
                  width: '100%',
                  justifyContent: 'center',
                }}
              >
                <ExternalLink size={13} /> View Transaction on Blockchain Explorer
              </a>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
