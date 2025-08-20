from audio_transcriber import AudioTranscriber

def main():
    audio_file_name = "C:\\Users\\leetr\\Lee\\Learning\\SoftwareDev\\EdDonner\\LLM-Engineering\\Repo\\llm-engineering\\Week-03\\Day-05\\practice\\denver_extract.mp3"
    transcription = AudioTranscriber().transcribe(audio_file_name)
    print()
    print(transcription)
    print()

if __name__ == "__main__":
    main()