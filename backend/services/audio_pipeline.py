import whisper
import numpy as np
import soundfile as sf
import os
import logging

logger = logging.getLogger("DEAR.Audio")

class AudioPipeline:
    def __init__(self, model_size: str = "base"):
        self.model_size = model_size
        self._stt_model = None

    def speech_to_text(self, audio_path: str, language: str = None) -> str:
        """
        Converts WAV file to text using Whisper, loading audio via soundfile
        to avoid the ffmpeg dependency on Windows.
        """
        import traceback
        try:
            if self._stt_model is None:
                self._stt_model = whisper.load_model(self.model_size)

            # Load audio with soundfile (no ffmpeg needed for WAV)
            audio, sr = sf.read(audio_path, dtype='float32', always_2d=False)
            # Mix down to mono if stereo
            if audio.ndim == 2:
                audio = audio.mean(axis=1)
            # Resample to 16kHz if needed (Whisper expects 16kHz)
            if sr != 16000:
                import librosa
                audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)

            # Pass language hint to Whisper for better accuracy
            transcribe_kwargs = {}
            if language:
                transcribe_kwargs["language"] = language

            # Pass numpy array directly — bypasses ffmpeg entirely
            result = self._stt_model.transcribe(audio, **transcribe_kwargs)
            return result.get("text", "").strip()
        except Exception as e:
            logger.error(f"STT Error full traceback:\n{traceback.format_exc()}")
            return ""

    def text_to_speech(self, text: str, output_path: str, voice: str = "en_US-lessac-medium.onnx"):
        """
        Converts text to speech using Piper TTS.
        Note: This assumes piper-tts is installed or available in PATH.
        """
        try:
            # Command: piper --model <model> --output_file <out>
            # For this demo, we'll use a subprocess call to piper
            import subprocess
            cmd = [
                "piper", 
                "--model", voice, 
                "--output_file", output_path
            ]
            process = subprocess.Popen(cmd, stdin=subprocess.PIPE)
            process.communicate(input=text.encode('utf-8'))
            return output_path
        except Exception as e:
            logger.error(f"TTS Error: {str(e)}")
            return None
