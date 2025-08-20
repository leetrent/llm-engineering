import os
from dotenv import load_dotenv
from openai import OpenAI

class AudioTranscriber:
    def __init__(self):
        self.audio_model = "whisper-1"
        self.response_format = "text"
        self._load_api_key()
        self.openai = OpenAI(api_key=self.api_key)
                
    def _load_api_key(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError("❌ No API key found in .env for ChatGPT.")
        
    def transcribe(self, audio_file_name):
        audio_file = open(audio_file_name, "rb")
        return self.openai.audio.transcriptions.create(model=self.audio_model, file=audio_file, response_format=self.response_format)
        
        
        
    