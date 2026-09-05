import React, { useState } from 'react';
import { X, ShieldCheck, AlertTriangle, CheckCircle2 } from 'lucide-react';
import axios from 'axios';

export default function VerificationModal({ isOpen, onClose, recordData }) {
  if (!isOpen || !recordData) return null;

  const [verifying, setVerifying] = useState(false);
  const [verificationResult, setVerificationResult] = useState(null);

  const handleVerify = async () => {
    setVerifying(true);
    try {
      const resp = await axios.post('/api/verification/verify', {
        record_id: recordData.blockchain.record_id,
        image_hash: recordData.hashes.image_hash,
        match_data_hash: recordData.hashes.match_data_hash,
        record_hash: recordData.hashes.record_hash
      });
      setVerificationResult(resp.data);
    } catch (err) {
      setVerificationResult({
        is_valid: false,
        message: err.response?.data?.detail?.message || 'Verification endpoint call failed.'
      });
    } finally {
      setVerifying(false);
    }
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(0, 0, 0, 0.8)',
      backdropFilter: 'blur(8px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000,
      padding: '1rem'
    }}>
      <div className="glass-card" style={{ maxWidth: '560px', width: '100%', margin: 0, position: 'relative' }}>
        <button
          onClick={onClose}
          style={{ position: 'absolute', top: '1.25rem', right: '1.25rem', background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}
        >
          <X size={20} />
        </button>

        <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <ShieldCheck size={22} color="var(--accent-emerald)" /> On-Chain Tamper Verification
        </h2>

        <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem', marginBottom: '1.25rem' }}>
          Recalculates cryptographic SHA-256 hashes of the current local image and metadata, and compares them directly against the immutable smart contract record on EVM testnet.
        </p>

        <div style={{ background: 'rgba(0,0,0,0.3)', padding: '1rem', borderRadius: '10px', marginBottom: '1.25rem', fontSize: '0.825rem' }}>
          <p style={{ color: 'var(--text-muted)', marginBottom: '0.25rem' }}>Record ID:</p>
          <p className="hash-text" style={{ marginBottom: '0.75rem' }}>{recordData.blockchain.record_id}</p>

          <p style={{ color: 'var(--text-muted)', marginBottom: '0.25rem' }}>Verification Hash:</p>
          <p className="hash-text" style={{ color: 'var(--accent-emerald)' }}>{recordData.hashes.record_hash}</p>
        </div>

        {verificationResult ? (
          <div style={{
            padding: '1rem',
            borderRadius: '10px',
            background: verificationResult.is_valid ? 'rgba(16, 185, 129, 0.15)' : 'rgba(244, 63, 94, 0.15)',
            border: verificationResult.is_valid ? '1px solid rgba(16, 185, 129, 0.4)' : '1px solid rgba(244, 63, 94, 0.4)',
            marginBottom: '1.25rem'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.35rem' }}>
              {verificationResult.is_valid ? (
                <CheckCircle2 size={20} color="var(--accent-emerald)" />
              ) : (
                <AlertTriangle size={20} color="var(--accent-rose)" />
              )}
              <h4 style={{ fontWeight: 700, color: verificationResult.is_valid ? 'var(--accent-emerald)' : 'var(--accent-rose)' }}>
                {verificationResult.is_valid ? 'VALID RECORD' : 'TAMPER DETECTED / INVALID'}
              </h4>
            </div>
            <p style={{ fontSize: '0.825rem', color: 'var(--text-main)' }}>{verificationResult.message}</p>
          </div>
        ) : null}

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem' }}>
          <button className="btn-secondary" onClick={onClose}>Close</button>
          <button className="btn-primary" onClick={handleVerify} disabled={verifying}>
            {verifying ? 'Checking Blockchain...' : 'Execute Tamper Verification'}
          </button>
        </div>
      </div>
    </div>
  );
}
