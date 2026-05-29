import { useEffect, useRef, useState } from 'react';
import { Hand } from 'lucide-react';

const GestureControl = ({ onGesture, isEnabled, onToggle }) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const handsRef = useRef(null);
  const [isActive, setIsActive] = useState(false);
  const [detectedGesture, setDetectedGesture] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const lastGestureRef = useRef(null);
  const gestureTimeoutRef = useRef(null);
  const streamRef = useRef(null);
  const animationFrameRef = useRef(null);

  // Gesture detection logic
  const detectGesture = (landmarks) => {
    if (!landmarks || landmarks.length === 0) return null;

    const hand = landmarks[0];
    
    // Get key points
    const thumb = hand[4];
    const indexTip = hand[8];
    const middleTip = hand[12];
    const ringTip = hand[16];
    const pinkyTip = hand[20];
    const wrist = hand[0];
    const indexBase = hand[5];
    const middleBase = hand[9];
    const thumbBase = hand[2];

    // Calculate distances
    const thumbIndexDist = Math.hypot(thumb.x - indexTip.x, thumb.y - indexTip.y);
    const palmHeight = Math.abs(wrist.y - indexBase.y);
    
    // Helper: Check if finger is extended (tip is above base)
    const isFingerExtended = (tip, base) => tip.y < base.y - 0.05;
    const isFingerClosed = (tip, base) => tip.y > base.y;

    // Count extended fingers
    const indexExtended = isFingerExtended(indexTip, indexBase);
    const middleExtended = isFingerExtended(middleTip, middleBase);
    const ringExtended = isFingerExtended(ringTip, hand[13]);
    const pinkyExtended = isFingerExtended(pinkyTip, hand[17]);
    
    const extendedFingers = [indexExtended, middleExtended, ringExtended, pinkyExtended].filter(Boolean).length;

    // � THUMBS UP: Thumb pointing up, all fingers closed
    const thumbUp = thumb.y < thumbBase.y - 0.15; // Thumb significantly above its base
    const allFingersClosed = !indexExtended && !middleExtended && !ringExtended && !pinkyExtended;
    if (thumbUp && allFingersClosed && thumb.y < wrist.y) {
      return 'thumbs_up';
    }

    // 👎 THUMBS DOWN: Thumb pointing down, all fingers closed
    const thumbDown = thumb.y > thumbBase.y + 0.15; // Thumb significantly below its base
    if (thumbDown && allFingersClosed && thumb.y > wrist.y) {
      return 'thumbs_down';
    }

    // ✋ HAND RAISE: Open palm raised high (all fingers extended, hand high in frame)
    const allFingersExtended = extendedFingers >= 3;
    const handRaised = wrist.y < 0.4; // Hand in upper part of frame
    if (allFingersExtended && handRaised && thumbIndexDist > 0.12) {
      return 'hand_raise';
    }

    // ✊ FIST: All fingers closed tightly
    const isFist = thumbIndexDist < 0.1 && 
                   extendedFingers === 0 &&
                   Math.hypot(indexTip.x - middleTip.x, indexTip.y - middleTip.y) < 0.08;
    if (isFist) {
      return 'fist';
    }

    // ☝️ POINT: Only index finger extended
    if (indexExtended && !middleExtended && !ringExtended && !pinkyExtended) {
      return 'point';
    }

    // 👋 WAVE: Open palm (must be last to avoid false positives)
    const isOpenPalm = thumbIndexDist > 0.15 && extendedFingers >= 3;
    if (isOpenPalm && palmHeight > 0.15) {
      return 'wave';
    }

    return null;
  };

  // Handle gesture detection
  const handleGesture = (gesture) => {
    if (!gesture || gesture === lastGestureRef.current) return;

    console.log('👋 Gesture detected:', gesture);
    setDetectedGesture(gesture);
    lastGestureRef.current = gesture;

    // Trigger callback
    if (onGesture) {
      onGesture(gesture);
    }

    // Clear gesture after 2 seconds
    if (gestureTimeoutRef.current) {
      clearTimeout(gestureTimeoutRef.current);
    }
    gestureTimeoutRef.current = setTimeout(() => {
      setDetectedGesture(null);
      lastGestureRef.current = null;
    }, 2000);
  };

  // Debug: Log hand position for calibration
  const debugHandPosition = (landmarks) => {
    if (!landmarks || landmarks.length === 0) return;
    const hand = landmarks[0];
    const thumb = hand[4];
    const indexTip = hand[8];
    const wrist = hand[0];
    const thumbBase = hand[2];
    
    // Log key metrics every 2 seconds
    if (!window.lastDebugLog || Date.now() - window.lastDebugLog > 2000) {
      console.log('📊 Hand Debug:', {
        thumbY: thumb.y.toFixed(2),
        thumbBaseY: thumbBase.y.toFixed(2),
        wristY: wrist.y.toFixed(2),
        indexY: indexTip.y.toFixed(2),
        thumbUp: thumb.y < thumbBase.y - 0.15,
        thumbDown: thumb.y > thumbBase.y + 0.15,
      });
      window.lastDebugLog = Date.now();
    }
  };

  // Initialize MediaPipe Hands
  useEffect(() => {
    if (!isEnabled) return;

    console.log('🤚 Initializing gesture control...');
    setIsLoading(true);

    // Load MediaPipe Hands from CDN
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js';
    script.crossOrigin = 'anonymous';
    
    script.onload = async () => {
      console.log('✅ MediaPipe Hands loaded');
      
      try {
        // Initialize Hands
        const hands = new window.Hands({
          locateFile: (file) => {
            return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
          }
        });

        hands.setOptions({
          maxNumHands: 1,
          modelComplexity: 1,
          minDetectionConfidence: 0.7,
          minTrackingConfidence: 0.7
        });

        hands.onResults((results) => {
          const canvas = canvasRef.current;
          if (!canvas) return;

          const ctx = canvas.getContext('2d');
          ctx.save();
          ctx.clearRect(0, 0, canvas.width, canvas.height);

          // Draw video frame
          if (results.image) {
            ctx.drawImage(results.image, 0, 0, canvas.width, canvas.height);
          }

          // Draw hand landmarks
          if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
            for (const landmarks of results.multiHandLandmarks) {
              // Draw connections
              ctx.strokeStyle = '#10b981';
              ctx.lineWidth = 2;
              
              const connections = [
                [0, 1], [1, 2], [2, 3], [3, 4], // Thumb
                [0, 5], [5, 6], [6, 7], [7, 8], // Index
                [0, 9], [9, 10], [10, 11], [11, 12], // Middle
                [0, 13], [13, 14], [14, 15], [15, 16], // Ring
                [0, 17], [17, 18], [18, 19], [19, 20], // Pinky
                [5, 9], [9, 13], [13, 17] // Palm
              ];

              connections.forEach(([start, end]) => {
                const startPoint = landmarks[start];
                const endPoint = landmarks[end];
                ctx.beginPath();
                ctx.moveTo(startPoint.x * canvas.width, startPoint.y * canvas.height);
                ctx.lineTo(endPoint.x * canvas.width, endPoint.y * canvas.height);
                ctx.stroke();
              });

              // Draw points
              landmarks.forEach((landmark) => {
                ctx.fillStyle = '#34d399';
                ctx.beginPath();
                ctx.arc(
                  landmark.x * canvas.width,
                  landmark.y * canvas.height,
                  5,
                  0,
                  2 * Math.PI
                );
                ctx.fill();
              });
            }

            // Detect gesture
            const gesture = detectGesture(results.multiHandLandmarks);
            if (gesture) {
              handleGesture(gesture);
            }
            
            // Debug logging
            debugHandPosition(results.multiHandLandmarks);
          }

          ctx.restore();
        });

        handsRef.current = hands;

        // Start camera
        const video = videoRef.current;
        if (video) {
          const stream = await navigator.mediaDevices.getUserMedia({
            video: { width: 640, height: 480 }
          });
          
          video.srcObject = stream;
          streamRef.current = stream;
          
          await video.play();
          
          // Process frames
          const processFrame = async () => {
            if (handsRef.current && video.readyState === 4) {
              await handsRef.current.send({ image: video });
            }
            animationFrameRef.current = requestAnimationFrame(processFrame);
          };
          
          processFrame();
          setIsActive(true);
          setIsLoading(false);
          console.log('✅ Gesture control active');
        }
      } catch (error) {
        console.error('❌ Failed to initialize gesture control:', error);
        setIsLoading(false);
        alert('Failed to access camera. Please check permissions.');
      }
    };

    script.onerror = () => {
      console.error('❌ Failed to load MediaPipe Hands');
      setIsLoading(false);
      alert('Failed to load gesture recognition library. Please check your internet connection.');
    };

    document.head.appendChild(script);

    return () => {
      console.log('🧹 Cleaning up gesture control');
      
      // Stop animation frame
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
      
      // Stop camera stream
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
      
      // Remove script
      if (script.parentNode) {
        script.parentNode.removeChild(script);
      }
      
      if (gestureTimeoutRef.current) {
        clearTimeout(gestureTimeoutRef.current);
      }
      
      setIsActive(false);
      setIsLoading(false);
    };
  }, [isEnabled]);

  const gestureLabels = {
    wave: '👋 Wave',
    thumbs_up: '👍 Thumbs Up',
    thumbs_down: '👎 Thumbs Down',
    hand_raise: '✋ Hand Raised',
    fist: '✊ Fist',
    point: '☝️ Pointing'
  };

  return (
    <div style={{
      position: 'fixed',
      bottom: '20px',
      right: '20px',
      zIndex: 1000,
    }}>
      {/* Toggle Button */}
      <button
        onClick={onToggle}
        title={isEnabled ? 'Disable gesture control' : 'Enable gesture control'}
        style={{
          width: '60px',
          height: '60px',
          borderRadius: '50%',
          border: '2px solid rgba(16,185,129,0.3)',
          background: isEnabled ? 'rgba(16,185,129,0.2)' : 'rgba(255,255,255,0.05)',
          color: isEnabled ? '#10b981' : '#94a3b8',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          cursor: 'pointer',
          transition: 'all 0.3s ease',
          boxShadow: isEnabled ? '0 0 20px rgba(16,185,129,0.4)' : 'none',
          animation: isEnabled ? 'pulse 2s infinite' : 'none',
        }}
      >
        {isEnabled ? <Hand size={28} /> : <Hand size={28} />}
      </button>

      {/* Camera Preview */}
      {isEnabled && (
        <div style={{
          position: 'absolute',
          bottom: '80px',
          right: '0',
          width: '320px',
          background: 'rgba(26,26,26,0.95)',
          borderRadius: '16px',
          padding: '12px',
          border: '2px solid rgba(16,185,129,0.3)',
          boxShadow: '0 8px 32px rgba(0,0,0,0.6)',
        }}>
          {/* Header */}
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '8px',
          }}>
            <span style={{
              fontSize: '14px',
              fontWeight: 600,
              color: '#10b981',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
            }}>
              <Hand size={16} /> {isLoading ? 'Loading...' : 'Gesture Control'}
            </span>
            {detectedGesture && (
              <span style={{
                fontSize: '20px',
                animation: 'bounce 0.5s ease',
              }}>
                {gestureLabels[detectedGesture]}
              </span>
            )}
          </div>

          {/* Video Canvas */}
          <div style={{ position: 'relative', borderRadius: '12px', overflow: 'hidden' }}>
            <video
              ref={videoRef}
              style={{
                display: 'none',
              }}
            />
            <canvas
              ref={canvasRef}
              width={640}
              height={480}
              style={{
                width: '100%',
                height: 'auto',
                display: 'block',
                transform: 'scaleX(-1)', // Mirror effect
              }}
            />
          </div>

          {/* Gesture Guide */}
          <div style={{
            marginTop: '8px',
            padding: '8px',
            background: 'rgba(16,185,129,0.1)',
            borderRadius: '8px',
            fontSize: '11px',
            color: '#94a3b8',
          }}>
            <div style={{ fontWeight: 600, color: '#10b981', marginBottom: '4px' }}>
              Gestures:
            </div>
            <div>👋 Wave = Activate Mic</div>
            <div>👍 Thumbs Up = Positive</div>
            <div>👎 Thumbs Down = Negative</div>
            <div>✋ Hand Raise = Interrupt</div>
          </div>
        </div>
      )}

      <style>{`
        @keyframes bounce {
          0%, 100% { transform: scale(1); }
          50% { transform: scale(1.2); }
        }
      `}</style>
    </div>
  );
};

export default GestureControl;
