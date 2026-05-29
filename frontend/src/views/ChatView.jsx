import { useState, useEffect, useRef, useCallback, forwardRef, useImperativeHandle } from 'react';
import { Mic, Send, Wifi, WifiOff, RefreshCw } from 'lucide-react';
import axios from 'axios';
import VoiceWave from '../components/Effects/VoiceWave';

const BACKEND = '';
const POLL_INTERVAL_MS = 5000; // check backend every 5s when offline

const ChatView = forwardRef(({ setVisemeTimeline, customization, speak }, ref) => {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello! I am bobmarley. How can I help you today?' }
  ]);
  const [input, setInput] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [backendOnline, setBackendOnline] = useState(null); // null=checking, true, false
  const [isTyping, setIsTyping] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const scrollContainerRef = useRef(null);
  const pollTimerRef = useRef(null);
  const processMessageRef = useRef(null);

  // ── Backend health check ──────────────────────────────────────────────────
  const checkBackend = useCallback(async () => {
    try {
      await axios.get(`/api/system/health`, { timeout: 2000 });
      setBackendOnline(true);
      return true;
    } catch {
      setBackendOnline(false);
      return false;
    }
  }, []);

  // Start polling when offline, stop when online
  useEffect(() => {
    checkBackend();
  }, []);

  useEffect(() => {
    if (backendOnline === false) {
      pollTimerRef.current = setInterval(() => checkBackend(true), POLL_INTERVAL_MS);
    } else {
      clearInterval(pollTimerRef.current);
    }
    return () => clearInterval(pollTimerRef.current);
  }, [backendOnline, checkBackend]);

// Keep processMessageRef in sync with latest processMessage
  useEffect(() => {
    processMessageRef.current = processMessage;
  });

  const toggleListening = useCallback(async () => {
    if (isRecording) {
      mediaRecorderRef.current?.stop();
      setIsRecording(false);
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioChunksRef.current = [];
      const recorder = new MediaRecorder(stream);

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) audioChunksRef.current.push(e.data);
      };

      recorder.onstop = async () => {
        stream.getTracks().forEach(t => t.stop());
        const blob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        try {
          const arrayBuffer = await blob.arrayBuffer();
          const audioCtx = new AudioContext();
          const decoded = await audioCtx.decodeAudioData(arrayBuffer);
          audioCtx.close();

          // Mix down to mono
          const pcm = decoded.numberOfChannels > 1
            ? (() => { const l = decoded.getChannelData(0); const r = decoded.getChannelData(1); return l.map((v, i) => (v + r[i]) / 2); })()
            : decoded.getChannelData(0);

          // Write valid PCM WAV using actual sample rate
          const sr = decoded.sampleRate;
          const wavBuffer = new ArrayBuffer(44 + pcm.length * 2);
          const view = new DataView(wavBuffer);
          const writeStr = (off, s) => { for (let i = 0; i < s.length; i++) view.setUint8(off + i, s.charCodeAt(i)); };
          writeStr(0, 'RIFF');
          view.setUint32(4, 36 + pcm.length * 2, true);
          writeStr(8, 'WAVE');
          writeStr(12, 'fmt ');
          view.setUint32(16, 16, true);
          view.setUint16(20, 1, true);   // PCM
          view.setUint16(22, 1, true);   // mono
          view.setUint32(24, sr, true);  // sample rate
          view.setUint32(28, sr * 2, true); // byte rate
          view.setUint16(32, 2, true);   // block align
          view.setUint16(34, 16, true);  // bits per sample
          writeStr(36, 'data');
          view.setUint32(40, pcm.length * 2, true);
          for (let i = 0; i < pcm.length; i++) {
            view.setInt16(44 + i * 2, Math.max(-1, Math.min(1, pcm[i])) * 0x7fff, true);
          }

          const wavBlob = new Blob([wavBuffer], { type: 'audio/wav' });
          const formData = new FormData();
          formData.append('audio', wavBlob, 'recording.wav');
          const lang = customization?.language || 'Telugu';
          const res = await axios.post(`${BACKEND}/api/stt?language=${encodeURIComponent(lang)}`, formData);
          const transcript = res.data.transcript;
          if (transcript) {
            setInput(transcript);
            if (processMessageRef.current) processMessageRef.current(transcript);
          }
        } catch (err) {
          console.error('❌ STT error:', err);
          alert('Could not transcribe audio. Make sure the backend is running.');
        }
      };

      mediaRecorderRef.current = recorder;
      recorder.start();
      setIsRecording(true);
    } catch (err) {
      console.error('❌ Mic access error:', err);
      alert('Microphone access denied. Please allow microphone permissions.');
    }
  }, [isRecording, customization]);

  // Expose methods to parent via ref
  useImperativeHandle(ref, () => ({
    activateMic: () => {
      if (!isRecording) {
        toggleListening();
      }
    },
    stopMic: () => {
      if (isRecording) {
        toggleListening();
      }
    }
  }));


  // ── Auto-scroll ───────────────────────────────────────────────────────────
  useEffect(() => {
    if (scrollContainerRef.current) {
      scrollContainerRef.current.scrollTo({
        top: scrollContainerRef.current.scrollHeight,
        behavior: 'smooth',
      });
    }
  }, [messages, isTyping]);

  // ── Message handling ──────────────────────────────────────────────────────
  const handleSend = async () => {
    if (!input.trim()) return;
    const currentInput = input;
    setInput('');
    await processMessage(currentInput);
  };

  const processMessage = async (text) => {
    setMessages(prev => [...prev, { role: 'user', content: text }]);
    // Add empty assistant shell for streaming
    setMessages(prev => [...prev, { role: 'assistant', content: '' }]);

    // Check backend first
    const alive = await checkBackend(true);

    if (!alive) {
      setMessages(prev => {
        const newArr = [...prev];
        newArr[newArr.length - 1] = {
           role: 'assistant',
           content: '⚡ Backend is offline. Launch the app via Leo.bat.',
           isOfflineNote: true
        };
        return newArr;
      });
      return;
    }

    try {
      const response = await fetch(`${BACKEND}/chat_stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          personality: customization?.personality || 'Friendly',
          language: customization?.language || 'Telugu',
          temperature: customization?.temperature || 0.7,
        })
      });

      // Check if response is ok
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let fullReply = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        fullReply += chunk;
        
        setMessages(prev => {
          const newArr = [...prev];
          newArr[newArr.length - 1].content = fullReply;
          return newArr;
        });
      }

      // Call speak function after receiving full response
      if (speak && fullReply) {
        console.log("Calling TTS with text:", fullReply.substring(0, 50) + "...");
        try {
          setIsSpeaking(true);
          speak(fullReply);
          // Reset speaking state after estimated duration
          setTimeout(() => setIsSpeaking(false), fullReply.length * 50);
        } catch (speakError) {
          console.error("TTS error:", speakError);
          setIsSpeaking(false);
        }
      } else {
        console.warn("Speak function not available or no reply text");
      }

    } catch (error) {
      console.error("Chat error:", error);
      setMessages(prev => {
        const newArr = [...prev];
        newArr[newArr.length - 1] = {
          role: 'assistant',
          content: `⚠️ Connection error. Please check if backend is running.`,
          isError: true,
        };
        return newArr;
      });
    }
  };

  // ── Status bar color/icon ─────────────────────────────────────────────────
  const statusColor = backendOnline === null ? '#f59e0b' : backendOnline ? '#6ee7b7' : '#f87171';
  const statusLabel = backendOnline === null ? 'Connecting…' : backendOnline ? 'AI Online' : 'AI Offline';
  const StatusIcon = backendOnline ? Wifi : WifiOff;

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      height: '100%',
      width: '100%',
      padding: '0',
      margin: '0',
      background: 'transparent',
      overflow: 'hidden',
    }}>

      {/* ── Status bar ── */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '16px 24px',
        borderBottom: '1px solid rgba(16,185,129,0.15)',
        background: 'rgba(26, 26, 26, 0.6)',
        backdropFilter: 'blur(20px)',
        flexShrink: 0,
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          {/* Pulsing dot */}
          <span style={{
            width: '8px', height: '8px', borderRadius: '50%',
            background: statusColor,
            boxShadow: backendOnline ? `0 0 8px ${statusColor}` : 'none',
            animation: backendOnline === null ? 'pulse 1.5s infinite' : 'none',
          }} />
          <StatusIcon size={16} color={statusColor} />
          <span style={{ fontSize: '13px', color: statusColor, fontWeight: 600, letterSpacing: '0.04em' }}>
            {statusLabel}
          </span>
          
          {/* Speaking indicator */}
          {isSpeaking && (
            <span style={{ 
              fontSize: '12px', 
              color: '#10b981', 
              marginLeft: '8px',
              display: 'flex',
              alignItems: 'center',
              gap: '4px'
            }}>
              🔊 Speaking...
            </span>
          )}

        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>

          {backendOnline === false && (
            <button
              onClick={() => checkBackend()}
              title="Retry connection"
              aria-label="Retry connection to backend"
              style={{
                background: 'rgba(255,255,255,0.06)',
                border: '1px solid rgba(255,255,255,0.1)',
                borderRadius: '8px', padding: '6px 12px',
                color: '#94a3b8', cursor: 'pointer',
                display: 'flex', alignItems: 'center', gap: '6px',
                fontSize: '12px', transition: 'all 0.2s',
                fontWeight: 500,
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = 'rgba(255,255,255,0.1)';
                e.currentTarget.style.color = '#fff';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = 'rgba(255,255,255,0.06)';
                e.currentTarget.style.color = '#94a3b8';
              }}
            >
              <RefreshCw size={12} /> Retry
            </button>
          )}
        </div>
      </div>

      {/* Offline banner removed per user request */}

      {/* ── Message Feed ── */}
      <div
        ref={scrollContainerRef}
        className="custom-scrollbar"
        style={{
          flex: 1,
          overflowY: 'auto',
          padding: '24px',
          display: 'flex',
          flexDirection: 'column',
          gap: '16px',
          background: 'transparent',
        }}
      >
        {messages.map((m, i) => (
          <div key={i} style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: m.role === 'user' ? 'flex-end' : 'flex-start',
          }}>
            <span style={{
              fontSize: '11px',
              fontWeight: '600',
              letterSpacing: '0.06em',
              textTransform: 'uppercase',
              marginBottom: '4px',
              color: m.role === 'user' ? '#a78bfa' : (m.isError || m.isOfflineNote) ? '#f87171' : '#10b981',
              paddingLeft: m.role === 'user' ? 0 : '4px',
              paddingRight: m.role === 'user' ? '4px' : 0,
            }}>
              {m.role === 'user' ? 'You' : 'bobmarley'}
            </span>

            <div style={{
              maxWidth: '82%',
              padding: '14px 18px',
              borderRadius: m.role === 'user'
                ? '20px 20px 4px 20px'
                : '20px 20px 20px 4px',
              fontSize: '15px',
              lineHeight: '1.6',
              ...(m.role === 'user' ? {
                background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                color: '#fff',
                boxShadow: '0 4px 20px rgba(16,185,129,0.4)',
              } : m.isError || m.isOfflineNote ? {
                background: 'rgba(248,113,113,0.08)',
                color: '#fca5a5',
                border: '1px solid rgba(248,113,113,0.25)',
              } : {
                background: 'rgba(255,255,255,0.06)',
                color: '#e2e8f0',
                border: '1px solid rgba(16,185,129,0.2)',
                boxShadow: '0 2px 12px rgba(0,0,0,0.3)',
              }),
            }}>
              {m.content}
            </div>
          </div>
        ))}

        {/* Typing indicator */}
        {isTyping && (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
            <span style={{ fontSize: '11px', fontWeight: 600, color: '#10b981', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '4px', paddingLeft: '4px' }}>
              bobmarley
            </span>
            <div style={{
              padding: '14px 20px',
              borderRadius: '20px 20px 20px 4px',
              background: 'rgba(255,255,255,0.06)',
              border: '1px solid rgba(16,185,129,0.2)',
              display: 'flex', gap: '5px', alignItems: 'center',
            }}>
              {[0, 1, 2].map(i => (
                <span key={i} style={{
                  width: '7px', height: '7px', borderRadius: '50%',
                  background: '#10b981',
                  display: 'inline-block',
                  animation: `bounce 1.2s ${i * 0.2}s infinite`,
                }} />
              ))}
            </div>
          </div>
        )}
      </div>

      {/* ── Input Bar ── */}
      <div style={{
        padding: '20px 24px',
        borderTop: '1px solid rgba(16,185,129,0.15)',
        background: 'rgba(26, 26, 26, 0.8)',
        backdropFilter: 'blur(20px)',
        display: 'flex',
        gap: '12px',
        alignItems: 'center',
        flexShrink: 0,
        position: 'relative',
      }}>
        {/* Voice Wave Effect */}
        <VoiceWave isActive={isSpeaking} color="#10b981" />


        <button
          onClick={toggleListening}
          title={isRecording ? 'Stop recording' : 'Voice input'}
          aria-label={isRecording ? 'Stop recording' : 'Start voice input'}
          disabled={false}
          style={{
            flexShrink: 0,
            width: '48px', height: '48px',
            borderRadius: '14px',
            border: '1px solid rgba(255,255,255,0.12)',
            background: isRecording ? 'rgba(239,68,68,0.2)' : 'rgba(255,255,255,0.05)',
            color: isRecording ? '#ef4444' : '#94a3b8',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            cursor: 'pointer',
            transition: 'all 0.2s ease',
            opacity: 1,
          }}
          onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'scale(1.05)';
              e.currentTarget.style.borderColor = isRecording ? '#ef4444' : 'rgba(255,255,255,0.2)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'scale(1)';
            e.currentTarget.style.borderColor = 'rgba(255,255,255,0.12)';
          }}
        >
          <Mic size={22} />
        </button>

        <input
          style={{
            flex: 1, height: '48px',
            background: 'rgba(255,255,255,0.07)',
            border: '1px solid rgba(255,255,255,0.12)',
            borderRadius: '14px',
            padding: '0 16px',
            fontSize: '15px', color: '#fff', outline: 'none',
            transition: 'all 0.2s ease',
            opacity: backendOnline === false ? 0.6 : 1,
          }}
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSend()}
          placeholder={backendOnline === false ? 'Backend offline — reconnecting…' : 'Type your message…'}
          disabled={backendOnline === false}
          aria-label="Message input"
          onFocus={e => e.target.style.borderColor = '#10b981'}
          onBlur={e => e.target.style.borderColor = 'rgba(255,255,255,0.12)'}
        />

        <button
          onClick={handleSend}
          disabled={!input.trim() || backendOnline === false}
          aria-label="Send message"
          style={{
            flexShrink: 0,
            width: '48px', height: '48px',
            borderRadius: '14px', border: 'none',
            background: input.trim() && backendOnline !== false 
              ? 'linear-gradient(135deg, #10b981, #059669)' 
              : 'rgba(255,255,255,0.05)',
            color: input.trim() && backendOnline !== false ? '#fff' : '#555',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            cursor: input.trim() && backendOnline !== false ? 'pointer' : 'not-allowed',
            boxShadow: input.trim() && backendOnline !== false 
              ? '0 4px 16px rgba(16,185,129,0.4)' 
              : 'none',
            transition: 'all 0.2s ease',
          }}
          onMouseEnter={(e) => {
            if (input.trim() && backendOnline !== false) {
              e.currentTarget.style.transform = 'scale(1.05)';
              e.currentTarget.style.boxShadow = '0 6px 20px rgba(16,185,129,0.5)';
            }
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'scale(1)';
            if (input.trim() && backendOnline !== false) {
              e.currentTarget.style.boxShadow = '0 4px 16px rgba(16,185,129,0.4)';
            }
          }}
        >
          <Send size={22} />
        </button>
      </div>

      {/* Keyframes injected inline via style tag */}
      <style>{`
        @keyframes bounce {
          0%, 60%, 100% { transform: translateY(0); }
          30% { transform: translateY(-6px); }
        }
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.3; }
        }
      `}</style>
    </div>
  );
});

export default ChatView;
