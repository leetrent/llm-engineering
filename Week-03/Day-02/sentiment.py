from transformers import pipeline

def main():
    classifier = pipeline(
        "sentiment-analysis",
        model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
        device="cuda"  # Or 0 if device ID is needed
    )
    result = classifier("I'm super excited to be on the way to LLM mastery!")
    print(result)

if __name__ == "__main__":
    main()
