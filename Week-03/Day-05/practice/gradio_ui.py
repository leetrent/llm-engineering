import gradio as gr
from audio_transcriber import AudioTranscriber
from secretary import Secretary

def process(mp3_path: str):
    if not mp3_path:
        yield "### Please upload an MY3 to begin."
        return
    
    transcript = AudioTranscriber().transcribe(mp3_path)
    
    yield "### 2) Generating Meeting Minutes with Phi-3..."

    user_prompt = {
        "role": "user",
        "content": (
            "Below is a meeting transcript. Please write minutes in markdown, including "
            "a summary with attendees, location and date; discussion points; takeaways; "
            "and action items with owners.\n" + transcript
        )
    }
    
    for chunck in Secretary().stream_minutes(user_prompt):
        yield chunck
        
with gr.Blocks(title="MP3 - Minutes") as demo:
    gr.Markdown("# 📝 MP3 → Meeting Minutes\nUpload on the left; streaming minutes on the right.")
    
    with gr.Row():
        with gr.Column(scale=1):
                audio = gr.Audio(type="filepath", label="Upload MP3")
                run = gr.Button("Transcribe & Summarize", variant="primary")
        with gr.Column(scale=2):
            out = gr.Markdown()
                
run.click(process, inputs=audio, outputs=out)
    
if __name__ == "__main__":
    demo.launch()
             