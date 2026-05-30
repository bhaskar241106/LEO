import subprocess
import re
import os
import shutil
import logging

logger = logging.getLogger("DEAR.Phonemes")

class PhonemeExtractor:
    # Friendly language name to standard eSpeak-NG voice code mapping
    ESPEAK_VOICE_MAP = {
        'English': 'en-us',
        'Telugu': 'te',
        'Hindi': 'hi',
        'Tamil': 'ta',
        'Kannada': 'kn',
        'Malayalam': 'ml',
        'Bengali': 'bn',
        'Marathi': 'mr',
        'Gujarati': 'gu',
        'Punjabi': 'pa',
        'Urdu': 'ur'
    }

    def __init__(self, espeak_path: str = None):
        if espeak_path is None:
            # 1. First look in system environment PATH
            resolved_path = shutil.which("espeak-ng")
            if not resolved_path:
                resolved_path = shutil.which("espeak")
            
            # 2. Check standard Windows default directories if not found in PATH
            if not resolved_path:
                common_paths = [
                    r"C:\Program Files\eSpeak NG\espeak-ng.exe",
                    r"C:\Program Files (x86)\eSpeak NG\espeak-ng.exe",
                    r"C:\Program Files\eSpeak\espeak.exe",
                    r"C:\Program Files (x86)\eSpeak\espeak.exe"
                ]
                for path in common_paths:
                    if os.path.exists(path):
                        resolved_path = path
                        break
            
            self.espeak_path = resolved_path or r"C:\Program Files\eSpeak NG\espeak-ng.exe"
        else:
            self.espeak_path = espeak_path
            
        logger.info(f"PhonemeExtractor initialized with eSpeak path: {self.espeak_path}")

        # Viseme mapping table based on simplified phoneme groups
        self.viseme_map = {
            'a': 'A', 'e': 'A', 'i': 'A', 'o': 'O', 'u': 'O',
            '@': 'A', 'E': 'A', 'I': 'A', 'O': 'O', 'U': 'O',
            'p': 'M', 'b': 'M', 'm': 'M', 'f': 'F', 'v': 'F',
            't': 'T', 'd': 'T', 'n': 'T', 's': 'T', 'z': 'T',
            'S': 'T', 'Z': 'T', 'r': 'T', 'l': 'T', 'k': 'T', 'g': 'T',
            'w': 'O'
        }

    def get_visemes(self, text: str, language: str = "English"):
        """
        Extracts phonemes and maps them to timed visemes dynamically using the appropriate language voice tag.
        """
        try:
            # Resolve the standard eSpeak-NG voice code
            voice_code = 'en-us'
            if language:
                if language in self.ESPEAK_VOICE_MAP:
                    voice_code = self.ESPEAK_VOICE_MAP[language]
                elif language.title() in self.ESPEAK_VOICE_MAP:
                    voice_code = self.ESPEAK_VOICE_MAP[language.title()]
                elif len(language) <= 5:
                    voice_code = language.lower()

            logger.info(f"Phonetic extraction using voice: '{voice_code}' for language: '{language}'")

            # -q (quiet), -x (phonemes), -v (voice)
            cmd = [self.espeak_path, "-q", "-x", "-v", voice_code, text]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            phonemes_raw = result.stdout.strip()
            
            # Remove stress marks and extra symbols
            phonemes = re.sub(r"[':%@&<>=#|\\]", "", phonemes_raw)
            
            visemes = []
            for char in phonemes:
                if char.lower() in self.viseme_map:
                    visemes.append(self.viseme_map[char.lower()])
                elif char.isspace():
                    visemes.append('Neutral')
            
            return visemes if visemes else ["Neutral"]
        except Exception as e:
            logger.error(f"Phoneme extraction error: {str(e)}")
            return ["Neutral"]

    def map_audio_duration(self, visemes, duration_sec):
        """
        Aligns visemes with audio duration.
        """
        if not visemes:
            return []
        
        interval = duration_sec / len(visemes)
        timeline = []
        current_time = 0
        for i, v in enumerate(visemes):
            timeline.append({"viseme": v, "time": round(current_time, 3)})
            current_time += interval
            
        return timeline
