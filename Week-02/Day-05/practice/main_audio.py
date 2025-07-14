import base64
from io import BytesIO
from PIL import Image
import os
from dotenv import load_dotenv
from openai import OpenAI
import platform
import subprocess

def get_api_key():
    load_dotenv(override=True)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("❌ No API key found in .env.")
    return api_key

def talker(message):
    openai = OpenAI(api_key=get_api_key())

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

if __name__ == "__main__":
    talker("Does anybody really know what time it is?")
