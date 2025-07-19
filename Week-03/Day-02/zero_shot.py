import sys
from transformers import pipeline

def main():
    if len(sys.argv) < 2:
        print("❌ Please provide a prompt.")
        sys.exit(1)

    prompt = sys.argv[1]
    print(f"🧠 Prompt: {prompt}")

    candidate_labels = ["concerning", "neutral", "reassuring"]
    
    classifier = pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli",  # Strong general-purpose model
        device="cuda"
    )

    result = classifier(prompt, candidate_labels)
    print("\n🔍 Zero-Shot Classification Result:")
    for label, score in zip(result['labels'], result['scores']):
        print(f"{label:<12} → {score:.4f}")

if __name__ == "__main__":
    main()
