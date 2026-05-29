import React, { useEffect, useState } from 'react';
import { CheckCircle, AlertCircle, Info, X } from 'lucide-react';

const Toast = ({ message, type = 'info', duration = 3000, onClose }) => {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsVisible(false);
      setTimeout(onClose, 300);
    }, duration);

    return () => clearTimeout(timer);
  }, [duration, onClose]);

  const icons = {
    success: <CheckCircle size={20} />,
    error: <AlertCircle size={20} />,
    info: <Info size={20} />,
  };

  const colors = {
    success: { bg: 'rgba(16, 185, 129, 0.15)', border: '#10b981', text: '#6ee7b7' },
    error: { bg: 'rgba(239, 68, 68, 0.15)', border: '#ef4444', text: '#fca5a5' },
    info: { bg: 'rgba(0, 210, 255, 0.15)', border: '#00d2ff', text: '#67e8f9' },
  };

  const style = colors[type];

  return (
    <div
      style={{
        position: 'fixed',
        top: '2rem',
        right: '2rem',
        zIndex: 9999,
        display: 'flex',
        alignItems: 'center',
        gap: '12px',
        padding: '14px 18px',
        background: style.bg,
        border: `1px solid ${style.border}`,
        borderRadius: '12px',
        color: style.text,
        backdropFilter: 'blur(20px)',
        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.4)',
        transform: isVisible ? 'translateX(0)' : 'translateX(400px)',
        opacity: isVisible ? 1 : 0,
        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        maxWidth: '400px',
      }}
      role="alert"
      aria-live="polite"
    >
      {icons[type]}
      <span style={{ flex: 1, fontSize: '14px', fontWeight: 500 }}>{message}</span>
      <button
        onClick={() => {
          setIsVisible(false);
          setTimeout(onClose, 300);
        }}
        style={{
          background: 'transparent',
          border: 'none',
          color: style.text,
          cursor: 'pointer',
          padding: '4px',
          display: 'flex',
          alignItems: 'center',
          opacity: 0.7,
          transition: 'opacity 0.2s',
        }}
        onMouseEnter={(e) => e.currentTarget.style.opacity = '1'}
        onMouseLeave={(e) => e.currentTarget.style.opacity = '0.7'}
        aria-label="Close notification"
      >
        <X size={16} />
      </button>
    </div>
  );
};

export default Toast;
