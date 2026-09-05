import React from 'react';
import { Search, ExternalLink, CheckCircle, AlertCircle, Globe } from 'lucide-react';

const PLATFORM_COLORS = {
  'Instagram': '#E1306C',
  'Facebook': '#1877F2',
  'X (Twitter)': '#1DA1F2',
  'LinkedIn': '#0A66C2',
  'TikTok': '#69C9D0',
  'YouTube': '#FF0000',
  'Reddit': '#FF4500',
  'Pinterest': '#E60023',
  'GitHub': '#6e40c9',
  'Web Result': '#6b7280',
};

function PlatformBadge({ platform }) {
  const color = PLATFORM_COLORS[platform] || '#6b7280';
  return (
    <span style={{
      display: 'inline-block',
      padding: '0.2rem 0.55rem',
      borderRadius: '999px',
      fontSize: '0.7rem',
      fontWeight: 700,
      letterSpacing: '0.03em',
      background: `${color}22`,
      color: color,
      border: `1px solid ${color}55`,
    }}>
      {platform}
    </span>
  );
}

function SimilarityDisplay({ candidate }) {
  const { similarity_calc_status, cosine_similarity } = candidate;

  if (similarity_calc_status === 'CALCULATED' && cosine_similarity !== null && cosine_similarity !== undefined) {
    const pct = Math.round(cosine_similarity * 100);
    const color = pct >= 65 ? '#10b981' : pct >= 45 ? '#f59e0b' : '#94a3b8';
    return (
      <div style={{ marginTop: '0.5rem' }}>
        <p style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Face Biometric Similarity</p>
        <p style={{ fontSize: '1rem', fontWeight: 700, color }}>{pct}%</p>
        <p style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>Threshold: 65% | Metric: Biometric Cosine</p>
      </div>
    );
  }

  return (
    <div style={{ marginTop: '0.5rem', background: 'rgba(100,116,139,0.1)', borderRadius: '6px', padding: '0.4rem 0.6rem' }}>
      <p style={{ fontSize: '0.68rem', color: '#94a3b8', lineHeight: 1.4 }}>
        Visual match from reverse search; facial similarity could not be independently computed from returned thumbnail.
      </p>
    </div>
  );
}

function CandidateCard({ candidate, isTop }) {
  const { url, title, source_domain, platform, image_url, reverse_search_relevance, match } = candidate;

  const matchColor = match ? '#10b981' : '#64748b';
  const matchLabel = match ? 'VERIFIED MATCH' : 'BELOW THRESHOLD';

  return (
    <div style={{
      background: 'rgba(0,0,0,0.3)',
      border: `1px solid ${match ? 'rgba(16,185,129,0.4)' : 'var(--border)'}`,
      borderRadius: '12px',
      padding: '1rem',
      display: 'flex',
      flexDirection: 'column',
      gap: '0.5rem',
      position: 'relative',
      overflow: 'hidden',
    }}>
      {isTop && match && (
        <div style={{ position: 'absolute', top: 0, right: 0, background: '#10b981', padding: '0.2rem 0.6rem', borderRadius: '0 12px 0 8px', fontSize: '0.65rem', fontWeight: 700, color: 'white' }}>
          BEST MATCH
        </div>
      )}

      {/* Header row */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
        <PlatformBadge platform={platform} />
        <span style={{
          padding: '0.2rem 0.55rem',
          borderRadius: '999px',
          fontSize: '0.68rem',
          fontWeight: 700,
          background: `${matchColor}22`,
          color: matchColor,
          border: `1px solid ${matchColor}55`,
        }}>
          {matchLabel}
        </span>
      </div>

      {/* Thumbnail */}
      {image_url && (
        <img
          src={image_url}
          alt="Candidate thumbnail"
          style={{ width: '100%', maxHeight: '120px', objectFit: 'cover', borderRadius: '8px', border: '1px solid var(--border)' }}
          onError={e => { e.target.style.display = 'none'; }}
        />
      )}

      {/* Title */}
      <p style={{ fontWeight: 600, fontSize: '0.875rem', color: 'var(--text-main)', lineHeight: 1.4 }}>{title}</p>

      {/* URL */}
      <a
        href={url}
        target="_blank"
        rel="noopener noreferrer"
        style={{ fontSize: '0.75rem', color: 'var(--accent-blue)', wordBreak: 'break-all', display: 'flex', alignItems: 'center', gap: '0.25rem' }}
      >
        <Globe size={11} /> {url}
      </a>

      <p style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Source: <strong>{source_domain}</strong></p>

      {/* Reverse search relevance */}
      <p style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
        Google Lens Relevance: <strong style={{ color: 'var(--text-main)' }}>{Math.round(reverse_search_relevance * 100)}%</strong>
      </p>

      {/* Honest similarity */}
      <SimilarityDisplay candidate={candidate} />

      {/* Open original post */}
      <a
        href={url}
        target="_blank"
        rel="noopener noreferrer"
        style={{
          marginTop: '0.25rem',
          display: 'inline-flex',
          alignItems: 'center',
          gap: '0.4rem',
          padding: '0.4rem 0.75rem',
          borderRadius: '8px',
          background: 'rgba(96,165,250,0.15)',
          color: 'var(--accent-blue)',
          fontSize: '0.78rem',
          fontWeight: 600,
          border: '1px solid rgba(96,165,250,0.3)',
          textDecoration: 'none',
          width: 'fit-content',
        }}
      >
        <ExternalLink size={13} /> Open Original Post
      </a>
    </div>
  );
}

export default function ReverseSearchSection({ searchInfo, topCandidates, bestMatch }) {
  if (!searchInfo) return null;

  const { provider, candidates_found_count, social_media_matches } = searchInfo;

  const SOCIAL_PLATFORMS = new Set(['Instagram','Facebook','X (Twitter)','LinkedIn','TikTok','YouTube','Reddit','Pinterest']);
  const socialCount = social_media_matches ?? (topCandidates || []).filter(c => SOCIAL_PLATFORMS.has(c.platform)).length;
  const hasVerifiedMatch = (topCandidates || []).some(c => c.match);

  return (
    <div className="glass-card">
      <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <Search size={20} color="var(--accent-cyan)" /> 3. Reverse Image Search &amp; Social Media Match
      </h2>

      {/* Summary row */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: '1rem', marginBottom: '1.25rem' }}>
        <div style={{ background: 'rgba(0,0,0,0.3)', padding: '0.85rem 1rem', borderRadius: '10px', border: '1px solid var(--border)' }}>
          <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '0.25rem' }}>Search Status</p>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <CheckCircle size={15} color="#10b981" />
            <span style={{ fontWeight: 700, color: '#10b981', fontSize: '0.875rem' }}>Completed</span>
          </div>
        </div>

        <div style={{ background: 'rgba(0,0,0,0.3)', padding: '0.85rem 1rem', borderRadius: '10px', border: '1px solid var(--border)' }}>
          <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '0.25rem' }}>Provider</p>
          <p style={{ fontWeight: 700, color: 'var(--accent-blue)', fontSize: '0.875rem', textTransform: 'uppercase' }}>
            {provider || 'SerpAPI'}
          </p>
        </div>

        <div style={{ background: 'rgba(0,0,0,0.3)', padding: '0.85rem 1rem', borderRadius: '10px', border: '1px solid var(--border)' }}>
          <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '0.25rem' }}>Results Found</p>
          <p style={{ fontWeight: 700, color: 'var(--text-main)', fontSize: '1.2rem' }}>{candidates_found_count ?? 0}</p>
        </div>

        <div style={{ background: 'rgba(0,0,0,0.3)', padding: '0.85rem 1rem', borderRadius: '10px', border: '1px solid var(--border)' }}>
          <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '0.25rem' }}>Biometric Match</p>
          <p style={{ fontWeight: 700, color: hasVerifiedMatch ? '#10b981' : 'var(--text-muted)', fontSize: '1.2rem' }}>
            {hasVerifiedMatch ? 'MATCH FOUND' : 'NO MATCH'}
          </p>
        </div>
      </div>

      {/* Informational banner when visual results exist but none meet facial identity threshold */}
      {topCandidates && topCandidates.length > 0 && !hasVerifiedMatch && (
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', color: '#94a3b8', padding: '0.75rem 1rem', background: 'rgba(100,116,139,0.1)', border: '1px solid rgba(100,116,139,0.25)', borderRadius: '8px', marginBottom: '1.25rem' }}>
          <AlertCircle size={18} color="#94a3b8" />
          <span style={{ fontSize: '0.82rem', lineHeight: 1.4 }}>
            Reverse search found visual matches on the web, but none met the biometric face similarity threshold (&ge; 65%). No false-positive identity match is confirmed.
          </span>
        </div>
      )}

      {/* No results */}
      {(!topCandidates || topCandidates.length === 0) && (
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#f59e0b', padding: '0.75rem', background: 'rgba(245,158,11,0.08)', borderRadius: '8px' }}>
          <AlertCircle size={15} />
          <span style={{ fontSize: '0.875rem' }}>No matching public result found from reverse image search.</span>
        </div>
      )}

      {/* Candidate cards */}
      {topCandidates && topCandidates.length > 0 && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem' }}>
          {topCandidates.slice(0, 6).map((candidate, i) => (
            <CandidateCard key={i} candidate={candidate} isTop={i === 0} />
          ))}
        </div>
      )}
    </div>
  );
}
