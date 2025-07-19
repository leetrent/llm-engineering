import sys
from transformers import pipeline

def main():
    if len(sys.argv) < 2:
        print("❌ Please provide a prompt.")
        sys.exit(1)

    prompt = sys.argv[1]
    print(f"🧠 Prompt: {prompt}")
    
    classifier = pipeline(
        "sentiment-analysis",
        model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
        device="cuda"  # Or 0 if device ID is needed
    )
    result = classifier(prompt)
    print(result)

if __name__ == "__main__":
    main()
