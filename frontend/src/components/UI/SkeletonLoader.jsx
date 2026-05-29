import React from 'react';

const SkeletonLoader = ({ width = '100%', height = '20px', borderRadius = '8px', className = '' }) => {
  return (
    <div
      className={`skeleton ${className}`}
      style={{
        width,
        height,
        borderRadius,
        background: 'linear-gradient(90deg, rgba(255,255,255,0.05) 25%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0.05) 75%)',
        backgroundSize: '200% 100%',
        animation: 'skeleton-loading 1.5s ease-in-out infinite',
      }}
      aria-label="Loading content"
      role="status"
    >
      <style>{`
        @keyframes skeleton-loading {
          0% { background-position: 200% 0; }
          100% { background-position: -200% 0; }
        }
      `}</style>
    </div>
  );
};

export const SkeletonCard = () => (
  <div className="glass p-6 rounded-3xl">
    <SkeletonLoader height="24px" width="60%" className="mb-4" />
    <SkeletonLoader height="16px" width="100%" className="mb-2" />
    <SkeletonLoader height="16px" width="80%" />
  </div>
);

export const SkeletonMessage = ({ isUser = false }) => (
  <div style={{ display: 'flex', flexDirection: 'column', alignItems: isUser ? 'flex-end' : 'flex-start', gap: '8px' }}>
    <SkeletonLoader height="12px" width="60px" />
    <SkeletonLoader 
      height="60px" 
      width={isUser ? '70%' : '80%'} 
      borderRadius={isUser ? '20px 20px 4px 20px' : '20px 20px 20px 4px'}
    />
  </div>
);

export default SkeletonLoader;
