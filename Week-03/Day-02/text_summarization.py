import sys
from transformers import pipeline

def main():
    if len(sys.argv) < 2:
        print("❌ Please provide a prompt.")
        sys.exit(1)

    prompt = sys.argv[1]
    print(f"\n🧠 Prompt: {prompt}\n")
   
    summarizer = pipeline(
        "summarization",
        model="facebook/bart-large-cnn",
        device="cuda"
    )
    
    summary = summarizer(prompt, max_length=50, min_length=25, do_sample=False)
    print(summary[0]['summary_text'])

if __name__ == "__main__":
    main()
