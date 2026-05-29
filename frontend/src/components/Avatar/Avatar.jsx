import React, { Suspense, useState, useRef } from 'react';
import { Canvas } from '@react-three/fiber';
import { ZoomIn, ZoomOut, Maximize2, RotateCw } from 'lucide-react';
import * as THREE from 'three';
import Scene3D from './Scene3D';

const Avatar = ({ viseme = "Neutral", expression = "Neutral", customization = {} }) => {
  const [zoom, setZoom] = useState(3.2);
  const [autoRotate, setAutoRotate] = useState(false);
  const cameraRef = useRef();

  const handleZoomIn = () => setZoom(prev => Math.max(prev - 0.5, 1.5));
  const handleZoomOut = () => setZoom(prev => Math.min(prev + 0.5, 6));
  const handleReset = () => { setZoom(3.2); setAutoRotate(false); };
  const toggleAutoRotate = () => setAutoRotate(prev => !prev);

  return (
    <div className="avatar-wrapper" style={{ 
      width: '100%', 
      height: '100%', 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center',
      minHeight: '400px',
      position: 'relative'
    }}>
      {/* 3D Canvas */}
      <Canvas 
        camera={{ position: [0, 0.2, zoom], fov: 35 }}
        shadows={{ type: THREE.PCFShadowMap }}
        gl={{ antialias: true, alpha: true }}
        style={{ background: 'transparent' }}
      >
        <Suspense fallback={null}>
          <Scene3D 
            viseme={viseme} 
            expression={expression} 
            customization={customization}
            autoRotate={autoRotate}
            zoom={zoom}
          />
        </Suspense>
      </Canvas>

      {/* Zoom Controls - Modern 3D Design */}
      <div style={{
        position: 'absolute',
        bottom: '6rem',
        right: '2rem',
        display: 'flex',
        flexDirection: 'column',
        gap: '0.75rem',
        zIndex: 10,
      }}>
        {/* Zoom In */}
        <button
          onClick={handleZoomIn}
          title="Zoom In"
          aria-label="Zoom in on avatar"
          className="avatar-control-btn"
          style={{
            width: '48px',
            height: '48px',
            borderRadius: '14px',
            background: 'rgba(26, 26, 26, 0.9)',
            backdropFilter: 'blur(20px)',
            border: '1px solid rgba(16, 185, 129, 0.3)',
            color: '#10b981',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            transition: 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)',
            boxShadow: '0 4px 16px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1)',
            outline: 'none',
          }}
        >
          <ZoomIn size={20} />
        </button>

        {/* Zoom Out */}
        <button
          onClick={handleZoomOut}
          title="Zoom Out"
          aria-label="Zoom out from avatar"
          className="avatar-control-btn"
          style={{
            width: '48px',
            height: '48px',
            borderRadius: '14px',
            background: 'rgba(26, 26, 26, 0.9)',
            backdropFilter: 'blur(20px)',
            border: '1px solid rgba(16, 185, 129, 0.3)',
            color: '#10b981',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            transition: 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)',
            boxShadow: '0 4px 16px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1)',
            outline: 'none',
          }}
        >
          <ZoomOut size={20} />
        </button>

        {/* Auto Rotate */}
        <button
          onClick={toggleAutoRotate}
          title={autoRotate ? "Stop Rotation" : "Auto Rotate"}
          aria-label={autoRotate ? "Stop auto rotation" : "Start auto rotation"}
          className="avatar-control-btn"
          style={{
            width: '48px',
            height: '48px',
            borderRadius: '14px',
            background: autoRotate ? 'rgba(16, 185, 129, 0.25)' : 'rgba(26, 26, 26, 0.9)',
            backdropFilter: 'blur(20px)',
            border: autoRotate ? '1px solid #10b981' : '1px solid rgba(16, 185, 129, 0.3)',
            color: autoRotate ? '#10b981' : '#10b981',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            transition: 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)',
            boxShadow: autoRotate 
              ? '0 8px 24px rgba(16, 185, 129, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.2)' 
              : '0 4px 16px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1)',
            outline: 'none',
          }}
        >
          <RotateCw size={20} style={{ animation: autoRotate ? 'spin 2s linear infinite' : 'none' }} />
        </button>

        {/* Reset View */}
        <button
          onClick={handleReset}
          title="Reset View"
          aria-label="Reset camera view"
          className="avatar-control-btn"
          style={{
            width: '48px',
            height: '48px',
            borderRadius: '14px',
            background: 'rgba(26, 26, 26, 0.9)',
            backdropFilter: 'blur(20px)',
            border: '1px solid rgba(16, 185, 129, 0.3)',
            color: '#10b981',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            transition: 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)',
            boxShadow: '0 4px 16px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1)',
            outline: 'none',
          }}
        >
          <Maximize2 size={20} />
        </button>
      </div>

      {/* Zoom Level Indicator */}
      <div style={{
        position: 'absolute',
        bottom: '2rem',
        right: '2rem',
        padding: '8px 16px',
        borderRadius: '12px',
        background: 'rgba(26, 26, 26, 0.85)',
        backdropFilter: 'blur(20px)',
        border: '1px solid rgba(16, 185, 129, 0.2)',
        color: '#10b981',
        fontSize: '0.75rem',
        fontWeight: 600,
        letterSpacing: '0.05em',
        boxShadow: '0 4px 16px rgba(0, 0, 0, 0.4)',
        zIndex: 10,
      }}>
        ZOOM: {Math.round((6 - zoom) / 4.5 * 100)}%
      </div>

      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        
        .avatar-control-btn:hover {
          transform: scale(1.1) translateY(-2px) !important;
          background: rgba(16, 185, 129, 0.2) !important;
          border-color: #10b981 !important;
          box-shadow: 0 8px 24px rgba(16, 185, 129, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        }
        
        .avatar-control-btn:active {
          transform: scale(0.95) !important;
        }
        
        .avatar-control-btn:focus-visible {
          outline: 2px solid #10b981 !important;
          outline-offset: 2px !important;
        }
      `}</style>
    </div>
  );
};

export default Avatar;
