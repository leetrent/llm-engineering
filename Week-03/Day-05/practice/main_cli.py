from audio_transcriber import AudioTranscriber
from secretary import Secretary

def main():
    print("CONVERTING AUDIO TO TEXT")
    audio_file_name = "C:\\Users\\leetr\\Lee\\Learning\\SoftwareDev\\EdDonner\\LLM-Engineering\\Repo\\llm-engineering\\Week-03\\Day-05\\practice\\denver_extract.mp3"
    transcription = AudioTranscriber().transcribe(audio_file_name)
    print()
    print(transcription)
    print()
    print("CONVERTING TEXT TO MEETING MINUTES")
    user_prompt = {
    "role": "user",
    "content": ("Below is an extract transcript of a Denver council meeting. "
                "Please write minutes in markdown, including a summary with attendees, "
                "location and date; discussion points; takeaways; "
                f"and action items with owners.\n{transcription}")}  
    
                
    Secretary().create_minutes(user_prompt)

if __name__ == "__main__":
    main()