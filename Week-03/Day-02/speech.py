import os
import sys
import numpy as np
from huggingface_hub import login
from transformers import pipeline
import soundfile as sf
import torch
from api_key import retrieve_api_key_value

def generate_speech(message):
    login(retrieve_api_key_value("HF_TOKEN"), add_to_git_credential=True)
    
    device_check = 0 if torch.cuda.is_available() else -1
    synthesiser = pipeline("text-to-speech", "microsoft/speecht5_tts", device=device_check)

    xvector_path = "cmu-arctic-xvectors/spkrec-xvect/cmu_us_rms_arctic-wav-arctic_a0012.npy"
    xvector = np.load(xvector_path)
    speaker_embedding = torch.tensor(xvector).unsqueeze(0)
    speech = synthesiser(message, forward_params={"speaker_embeddings": speaker_embedding})
    sf.write("speech.wav", speech["audio"], samplerate=speech["sampling_rate"])
    os.startfile("speech.wav")  # This will open it in the default audio player

def main():
    print(torch.cuda.is_available())
    
    if len(sys.argv) < 2:
        print("Usage: python image.py <TEXT>")
        sys.exit(1)

    text = sys.argv[1]
    generate_speech(text)
    
if __name__ == "__main__":
  main()