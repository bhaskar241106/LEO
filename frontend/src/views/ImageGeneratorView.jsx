import { useState, useEffect } from 'react';
import { Image as ImageIcon, Sparkles, Download, RefreshCw, Loader } from 'lucide-react';
import axios from 'axios';

const BACKEND = 'http://localhost:8000';

const ImageGeneratorView = () => {
  const [prompt, setPrompt] = useState('');
  const [negativePrompt, setNegativePrompt] = useState('blurry, bad quality, distorted');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedImage, setGeneratedImage] = useState(null);
  const [error, setError] = useState(null);
  const [isAvailable, setIsAvailable] = useState(null);
  const [settings, setSettings] = useState({
    width: 512,
    height: 512,
    steps: 20,
    cfgScale: 7.0,
    enhancePrompt: true
  });

  // Check if image generation is available
  useEffect(() => {
    checkAvailability();
  }, []);

  const checkAvailability = async () => {
    try {
      const response = await axios.get(`${BACKEND}/api/image/status`);
      setIsAvailable(response.data);
    } catch (err) {
      setIsAvailable({ available: false, message: 'Backend offline' });
    }
  };

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError('Please enter a prompt');
      return;
    }

    setIsGenerating(true);
    setError(null);
    setGeneratedImage(null);

    try {
      const response = await axios.post(`${BACKEND}/api/image/generate`, {
        prompt: prompt,
        negative_prompt: negativePrompt,
        width: settings.width,
        height: settings.height,
        steps: settings.steps,
        cfg_scale: settings.cfgScale,
        enhance_prompt: settings.enhancePrompt
      }, {
        timeout: 600000 // 10 minutes (first generation on CPU can take 5-8 minutes)
      });

      if (response.data.success) {
        setGeneratedImage(response.data);
      } else {
        setError(response.data.error || response.data.note);
      }
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Generation failed');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleDownload = () => {
    if (!generatedImage?.image) return;

    const link = document.createElement('a');
    link.href = `data:image/png;base64,${generatedImage.image}`;
    link.download = `generated-${Date.now()}.png`;
    link.click();
  };

  const presetPrompts = [
    "A serene mountain landscape at sunset with vibrant colors",
    "A futuristic city with flying cars and neon lights",
    "A cute robot assistant helping people",
    "An astronaut floating in space with Earth in background",
    "A magical forest with glowing mushrooms and fireflies"
  ];

  return (
    <div className="view-container custom-scrollbar" style={{ padding: '2rem' }}>
      {/* Header */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '15px',
        marginBottom: '30px'
      }}>
        <ImageIcon size={32} color="#10b981" />
        <div>
          <h1 style={{
            fontSize: '2rem',
            fontWeight: 700,
            background: 'linear-gradient(90deg, #fff, #10b981)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            margin: 0
          }}>
            AI Image Generator
          </h1>
          <p style={{ color: '#94a3b8', fontSize: '0.9rem', margin: '5px 0 0 0' }}>
            {isAvailable?.available 
              ? `✅ ${isAvailable.message}` 
              : '⚠️ Stable Diffusion not available'}
          </p>
        </div>
      </div>

      {/* Main Content */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: '30px',
        maxWidth: '1400px'
      }}>
        {/* Left Panel - Input */}
        <div>
          {/* Prompt Input */}
          <div style={{ marginBottom: '20px' }}>
            <label style={{
              display: 'block',
              color: '#10b981',
              fontWeight: 600,
              marginBottom: '8px',
              fontSize: '0.9rem'
            }}>
              Prompt
            </label>
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe the image you want to generate..."
              style={{
                width: '100%',
                minHeight: '120px',
                padding: '15px',
                background: 'rgba(255,255,255,0.05)',
                border: '1px solid rgba(16,185,129,0.2)',
                borderRadius: '12px',
                color: '#fff',
                fontSize: '0.95rem',
                resize: 'vertical',
                outline: 'none',
                transition: 'all 0.2s'
              }}
              onFocus={(e) => e.target.style.borderColor = '#10b981'}
              onBlur={(e) => e.target.style.borderColor = 'rgba(16,185,129,0.2)'}
            />
          </div>

          {/* Preset Prompts */}
          <div style={{ marginBottom: '20px' }}>
            <label style={{
              display: 'block',
              color: '#94a3b8',
              fontWeight: 600,
              marginBottom: '8px',
              fontSize: '0.85rem'
            }}>
              Quick Presets
            </label>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
              {presetPrompts.map((preset, i) => (
                <button
                  key={i}
                  onClick={() => setPrompt(preset)}
                  style={{
                    padding: '6px 12px',
                    background: 'rgba(16,185,129,0.1)',
                    border: '1px solid rgba(16,185,129,0.3)',
                    borderRadius: '8px',
                    color: '#10b981',
                    fontSize: '0.8rem',
                    cursor: 'pointer',
                    transition: 'all 0.2s'
                  }}
                  onMouseEnter={(e) => {
                    e.target.style.background = 'rgba(16,185,129,0.2)';
                    e.target.style.transform = 'translateY(-2px)';
                  }}
                  onMouseLeave={(e) => {
                    e.target.style.background = 'rgba(16,185,129,0.1)';
                    e.target.style.transform = 'translateY(0)';
                  }}
                >
                  {preset.substring(0, 30)}...
                </button>
              ))}
            </div>
          </div>

          {/* Negative Prompt */}
          <div style={{ marginBottom: '20px' }}>
            <label style={{
              display: 'block',
              color: '#94a3b8',
              fontWeight: 600,
              marginBottom: '8px',
              fontSize: '0.9rem'
            }}>
              Negative Prompt (Optional)
            </label>
            <input
              type="text"
              value={negativePrompt}
              onChange={(e) => setNegativePrompt(e.target.value)}
              placeholder="What to avoid..."
              style={{
                width: '100%',
                padding: '12px 15px',
                background: 'rgba(255,255,255,0.05)',
                border: '1px solid rgba(255,255,255,0.1)',
                borderRadius: '10px',
                color: '#fff',
                fontSize: '0.9rem',
                outline: 'none'
              }}
            />
          </div>

          {/* Settings */}
          <div style={{
            background: 'rgba(16,185,129,0.05)',
            border: '1px solid rgba(16,185,129,0.2)',
            borderRadius: '12px',
            padding: '20px',
            marginBottom: '20px'
          }}>
            <h3 style={{ color: '#10b981', fontSize: '1rem', marginBottom: '15px' }}>
              Settings
            </h3>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
              <div>
                <label style={{ color: '#94a3b8', fontSize: '0.85rem', display: 'block', marginBottom: '5px' }}>
                  Width: {settings.width}px
                </label>
                <input
                  type="range"
                  min="256"
                  max="1024"
                  step="64"
                  value={settings.width}
                  onChange={(e) => setSettings({...settings, width: parseInt(e.target.value)})}
                  style={{ width: '100%' }}
                />
              </div>

              <div>
                <label style={{ color: '#94a3b8', fontSize: '0.85rem', display: 'block', marginBottom: '5px' }}>
                  Height: {settings.height}px
                </label>
                <input
                  type="range"
                  min="256"
                  max="1024"
                  step="64"
                  value={settings.height}
                  onChange={(e) => setSettings({...settings, height: parseInt(e.target.value)})}
                  style={{ width: '100%' }}
                />
              </div>

              <div>
                <label style={{ color: '#94a3b8', fontSize: '0.85rem', display: 'block', marginBottom: '5px' }}>
                  Steps: {settings.steps}
                </label>
                <input
                  type="range"
                  min="10"
                  max="50"
                  step="5"
                  value={settings.steps}
                  onChange={(e) => setSettings({...settings, steps: parseInt(e.target.value)})}
                  style={{ width: '100%' }}
                />
              </div>

              <div>
                <label style={{ color: '#94a3b8', fontSize: '0.85rem', display: 'block', marginBottom: '5px' }}>
                  CFG Scale: {settings.cfgScale}
                </label>
                <input
                  type="range"
                  min="1"
                  max="20"
                  step="0.5"
                  value={settings.cfgScale}
                  onChange={(e) => setSettings({...settings, cfgScale: parseFloat(e.target.value)})}
                  style={{ width: '100%' }}
                />
              </div>
            </div>

            <div style={{ marginTop: '15px' }}>
              <label style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                color: '#94a3b8',
                fontSize: '0.9rem',
                cursor: 'pointer'
              }}>
                <input
                  type="checkbox"
                  checked={settings.enhancePrompt}
                  onChange={(e) => setSettings({...settings, enhancePrompt: e.target.checked})}
                  style={{ cursor: 'pointer' }}
                />
                <Sparkles size={16} />
                Enhance prompt with AI
              </label>
            </div>
          </div>

          {/* Generate Button */}
          <button
            onClick={handleGenerate}
            disabled={isGenerating || !isAvailable?.available}
            style={{
              width: '100%',
              padding: '15px',
              background: isGenerating || !isAvailable?.available 
                ? 'rgba(255,255,255,0.1)' 
                : 'linear-gradient(135deg, #10b981, #059669)',
              border: 'none',
              borderRadius: '12px',
              color: '#fff',
              fontSize: '1rem',
              fontWeight: 600,
              cursor: isGenerating || !isAvailable?.available ? 'not-allowed' : 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '10px',
              transition: 'all 0.3s',
              boxShadow: isGenerating || !isAvailable?.available 
                ? 'none' 
                : '0 4px 20px rgba(16,185,129,0.4)'
            }}
            onMouseEnter={(e) => {
              if (!isGenerating && isAvailable?.available) {
                e.target.style.transform = 'translateY(-2px)';
                e.target.style.boxShadow = '0 6px 25px rgba(16,185,129,0.5)';
              }
            }}
            onMouseLeave={(e) => {
              e.target.style.transform = 'translateY(0)';
              if (!isGenerating && isAvailable?.available) {
                e.target.style.boxShadow = '0 4px 20px rgba(16,185,129,0.4)';
              }
            }}
          >
            {isGenerating ? (
              <>
                <Loader size={20} className="spin" />
                Generating... ({settings.steps} steps)
              </>
            ) : (
              <>
                <Sparkles size={20} />
                Generate Image
              </>
            )}
          </button>
        </div>

        {/* Right Panel - Output */}
        <div>
          <div style={{
            background: 'rgba(255,255,255,0.03)',
            border: '2px dashed rgba(16,185,129,0.3)',
            borderRadius: '16px',
            padding: '20px',
            minHeight: '500px',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            {isGenerating && (
              <div style={{ textAlign: 'center' }}>
                <Loader size={48} color="#10b981" className="spin" style={{ marginBottom: '20px' }} />
                <p style={{ color: '#10b981', fontSize: '1.1rem', fontWeight: 600 }}>
                  Creating your image...
                </p>
                <p style={{ color: '#94a3b8', fontSize: '0.9rem' }}>
                  This may take 30-60 seconds
                </p>
              </div>
            )}

            {error && !isGenerating && (
              <div style={{ textAlign: 'center', color: '#ef4444' }}>
                <p style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '10px' }}>
                  ⚠️ Error
                </p>
                <p style={{ fontSize: '0.9rem' }}>{error}</p>
                {!isAvailable?.available && (
                  <div style={{
                    marginTop: '20px',
                    padding: '15px',
                    background: 'rgba(239,68,68,0.1)',
                    borderRadius: '10px',
                    fontSize: '0.85rem',
                    color: '#fca5a5'
                  }}>
                    <p style={{ fontWeight: 600, marginBottom: '10px' }}>
                      Setup Required:
                    </p>
                    <ol style={{ textAlign: 'left', paddingLeft: '20px' }}>
                      <li>Install Stable Diffusion WebUI</li>
                      <li>Start with --api flag</li>
                      <li>Ensure it's running on port 7860</li>
                    </ol>
                  </div>
                )}
              </div>
            )}

            {generatedImage && !isGenerating && (
              <div style={{ width: '100%' }}>
                <img
                  src={`data:image/png;base64,${generatedImage.image}`}
                  alt="Generated"
                  style={{
                    width: '100%',
                    borderRadius: '12px',
                    marginBottom: '15px',
                    boxShadow: '0 8px 32px rgba(0,0,0,0.5)'
                  }}
                />
                <div style={{
                  background: 'rgba(16,185,129,0.1)',
                  padding: '12px',
                  borderRadius: '10px',
                  marginBottom: '15px'
                }}>
                  <p style={{ color: '#94a3b8', fontSize: '0.85rem', margin: 0 }}>
                    <strong style={{ color: '#10b981' }}>Prompt:</strong> {generatedImage.prompt}
                  </p>
                </div>
                <button
                  onClick={handleDownload}
                  style={{
                    width: '100%',
                    padding: '12px',
                    background: 'rgba(16,185,129,0.2)',
                    border: '1px solid #10b981',
                    borderRadius: '10px',
                    color: '#10b981',
                    fontSize: '0.95rem',
                    fontWeight: 600,
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '8px',
                    transition: 'all 0.2s'
                  }}
                  onMouseEnter={(e) => {
                    e.target.style.background = 'rgba(16,185,129,0.3)';
                  }}
                  onMouseLeave={(e) => {
                    e.target.style.background = 'rgba(16,185,129,0.2)';
                  }}
                >
                  <Download size={18} />
                  Download Image
                </button>
              </div>
            )}

            {!isGenerating && !error && !generatedImage && (
              <div style={{ textAlign: 'center', color: '#94a3b8' }}>
                <ImageIcon size={64} style={{ marginBottom: '20px', opacity: 0.3 }} />
                <p style={{ fontSize: '1.1rem' }}>
                  Your generated image will appear here
                </p>
              </div>
            )}
          </div>
        </div>
      </div>

      <style>{`
        .spin {
          animation: spin 1s linear infinite;
        }
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default ImageGeneratorView;
