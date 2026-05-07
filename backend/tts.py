import edge_tts
import asyncio
import os

class TextToSpeech:
    def __init__(self):
        # We'll auto-detect language
        self.voice_en = "en-IN-NeerjaNeural"  # Indian English
        self.voice_hi = "hi-IN-SwaraNeural"   # Hindi
    
    async def speak(self, text: str, save_path: str = None):
        """Convert text to speech with auto language detection"""
        
        # Simple language detection
        if any('\u0900' <= char <= '\u097F' for char in text):
            # Contains Devanagari (Hindi) characters
            voice = self.voice_hi
            print(f"🇮🇳 Using Hindi voice")
        else:
            # English
            voice = self.voice_en
            print(f"🇬🇧 Using English voice")
        
        try:
            communicate = edge_tts.Communicate(text, voice)
            
            if save_path:
                await communicate.save(save_path)
                print(f"🔊 Audio saved: {save_path}")
            else:
                temp_path = "temp_response.mp3"
                await communicate.save(temp_path)
                print(f"🔊 Audio saved: {temp_path}")
            
            return save_path
        except Exception as e:
            print(f"❌ TTS Error: {e}")
            # Fallback to English voice
            communicate = edge_tts.Communicate(text, self.voice_en)
            await communicate.save(save_path)
            return save_path