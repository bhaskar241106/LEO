import React from 'react';

const LoadingSpinner = ({ size = 'md', color = '#00d2ff' }) => {
  const sizes = {
    sm: '16px',
    md: '24px',
    lg: '32px',
    xl: '48px'
  };

  return (
    <div
      style={{
        width: sizes[size],
        height: sizes[size],
        border: `3px solid rgba(255, 255, 255, 0.1)`,
        borderTop: `3px solid ${color}`,
        borderRadius: '50%',
        animation: 'spin 0.8s linear infinite',
      }}
      role="status"
      aria-label="Loading"
    >
      <style>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default LoadingSpinner;
