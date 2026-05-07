from faster_whisper import WhisperModel
import os

class SpeechToText:
    def __init__(self, model_size="small"):
        # Use small/medium for speed on Colab/free tier
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")
    
    def transcribe(self, audio_path: str):
        segments, info = self.model.transcribe(
            audio_path,
            beam_size=5,
            word_timestamps=True,
            language=None  # auto-detect (good for Hinglish)
        )
        
        transcript = " ".join(segment.text for segment in segments)
        print(f"📝 Transcript: {transcript}")
        return transcript.strip()