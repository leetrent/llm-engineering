import sys
import os
import platform
import subprocess
from io import BytesIO
from openai import OpenAI
from api_key import retrieve_api_key_value

def generate_speech(message):
    openai = OpenAI(api_key=retrieve_api_key_value("OPENAI_API_KEY"))

    response = openai.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=message
    )

    audio_stream = BytesIO(response.content)
    output_filename = "output_audio.mp3"
    with open(output_filename, "wb") as f:
        f.write(audio_stream.read())

    # Play the audio using a platform-specific command
    if platform.system() == "Windows":
        os.startfile(output_filename)
    elif platform.system() == "Darwin":  # macOS
        subprocess.run(["open", output_filename])
    else:  # Linux
        subprocess.run(["xdg-open", output_filename])

def main():
    if len(sys.argv) < 2:
        print("Usage: python image.py <TEXT>")
        sys.exit(1)

    text = sys.argv[1]
    generate_speech(text)
    
if __name__ == "__main__":
  main()