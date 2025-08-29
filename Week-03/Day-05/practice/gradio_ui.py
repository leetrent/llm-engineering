import gradio as gr
from audio_transcriber import AudioTranscriber
from secretary import Secretary

def process(mp3_path: str):
    if not mp3_path:
        yield "### Please upload an MP3 to begin."
        return
    
    ####################################################
    # 1) Transcribe with Whisper-1"
    ####################################################
    yield "### 1) Transcibe with Whisper-1"
    transcript = AudioTranscriber().transcribe(mp3_path)
    
    ####################################################
    # 2) Stream meeting minutes from Phi-3
    ####################################################
    yield "### 2) Generating Meeting Minutes with Phi-3..."

    user_prompt = {
        "role": "user",
        "content": (
            "Below is a meeting transcript. Please write minutes in markdown, including "
            "a summary with attendees, location and date; discussion points; takeaways; "
            "and action items with owners.\n" + transcript
        ),
    }
    
    for chunck in Secretary().stream_minutes(user_prompt):
        yield chunck
        
####################################################
# UI (top level, not inside a function)
####################################################  
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
             