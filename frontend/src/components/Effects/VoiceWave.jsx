import { useEffect, useRef } from 'react';

const VoiceWave = ({ isActive, color = '#10b981' }) => {
  const canvasRef = useRef(null);
  const animationRef = useRef(null);
  const phaseRef = useRef(0);

  useEffect(() => {
    if (!isActive) return;

    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;

    const centerY = canvas.height / 2;
    const amplitude = 20;
    const frequency = 0.02;
    const speed = 0.1;

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Draw multiple waves
      for (let wave = 0; wave < 3; wave++) {
        ctx.beginPath();
        ctx.moveTo(0, centerY);

        for (let x = 0; x < canvas.width; x++) {
          const y = centerY + 
            Math.sin(x * frequency + phaseRef.current + wave * 0.5) * amplitude * (1 - wave * 0.3);
          ctx.lineTo(x, y);
        }

        ctx.strokeStyle = `${color}${Math.floor((1 - wave * 0.3) * 255).toString(16).padStart(2, '0')}`;
        ctx.lineWidth = 2 - wave * 0.5;
        ctx.stroke();
      }

      phaseRef.current += speed;
      animationRef.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [isActive, color]);

  if (!isActive) return null;

  return (
    <canvas
      ref={canvasRef}
      style={{
        position: 'absolute',
        bottom: '80px',
        left: '50%',
        transform: 'translateX(-50%)',
        width: '300px',
        height: '60px',
        pointerEvents: 'none',
        zIndex: 10,
      }}
    />
  );
};

export default VoiceWave;
