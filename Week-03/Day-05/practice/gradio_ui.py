# ---- app.py ----
# Disable Brotli BEFORE any Gradio imports (prevents h11 content-length issues on Windows)
import os
os.environ["GRADIO_USE_BROTLI"] = "0"
os.environ["GRADIO_DISABLE_BROTLI"] = "1"

import gradio as gr
from audio_transcriber import AudioTranscriber
from secretary import Secretary

def process(mp3_path: str):
    if not mp3_path:
        yield "### Please upload an MP3 to begin."
        return

    # 1) Transcribe (status first so UI stays responsive)
    yield "### 1) Transcribe with Whisper-1…"
    transcript = AudioTranscriber().transcribe(mp3_path)
    if not transcript or not transcript.strip():
        yield "### Error\nTranscription returned empty text."
        return

    # 2) Stream minutes as Markdown
    prefix = "# Meeting Minutes\n\n"
    yield gr.update(value=prefix + "_Generating with Phi-3…_")

    user_prompt = {
        "role": "user",
        "content": (
            "Below is a meeting transcript. Please write minutes in markdown, including "
            "a summary with attendees, date, and location; discussion points; decisions; "
            "and action items with owners and due dates.\n" + transcript
        ),
    }

    for chunk in Secretary().stream_minutes(user_prompt):
        yield gr.update(value=prefix + chunk)

with gr.Blocks(title="MP3 → Meeting Minutes") as demo:
    gr.Markdown("# 📝 MP3 → Meeting Minutes\nUpload on the left; streaming minutes on the right.")
    with gr.Row():
        with gr.Column(scale=1):
            # Only uploads; nothing runs on upload alone
            audio = gr.Audio(type="filepath", sources=["upload"], label="Upload MP3")
            run = gr.Button("Transcribe & Summarize", variant="primary")
        with gr.Column(scale=2):
            out = gr.Markdown()

    # Only the button triggers the pipeline
    run.click(process, inputs=audio, outputs=out)

if __name__ == "__main__":
    demo.launch()  # plain launch = max compatibility across Gradio versions
