import traceback, sys, os, tempfile
import numpy as np
import soundfile as sf

sys.stdout.reconfigure(encoding='utf-8')

print("=== STT Test ===")

# Step 1: soundfile
print("1. Testing soundfile write/read...")
tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
tmp.close()
audio_out = (np.random.randn(32000) * 0.1).astype('float32')
sf.write(tmp.name, audio_out, 16000)
audio_in, sr = sf.read(tmp.name, dtype='float32')
print(f"   OK: shape={audio_in.shape}, sr={sr}, file={os.path.getsize(tmp.name)} bytes")

# Step 2: whisper load
print("2. Loading Whisper model...")
try:
    import whisper
    m = whisper.load_model('base')
    print("   OK: model loaded")
except Exception as e:
    print(f"   FAIL: {traceback.format_exc()}")
    sys.exit(1)

# Step 3: transcribe numpy array
print("3. Transcribing numpy array...")
try:
    result = m.transcribe(audio_in)
    print(f"   OK: '{result['text']}'")
except Exception as e:
    print(f"   FAIL: {traceback.format_exc()}")

# Step 4: AudioPipeline
print("4. Testing AudioPipeline.speech_to_text...")
try:
    from services.audio_pipeline import AudioPipeline
    p = AudioPipeline()
    text = p.speech_to_text(tmp.name)
    print(f"   OK: '{text}'")
except Exception as e:
    print(f"   FAIL: {traceback.format_exc()}")

os.unlink(tmp.name)
print("=== Done ===")
