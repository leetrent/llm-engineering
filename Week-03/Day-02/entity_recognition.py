import sys
from transformers import pipeline

def main():
    if len(sys.argv) < 2:
        print("❌ Please provide a prompt.")
        sys.exit(1)

    prompt = sys.argv[1]
    print(f"🧠 Prompt: {prompt}")
   
    ner = pipeline(
        "ner",
        model="dslim/bert-base-NER",
        grouped_entities=True,
        device="cuda"
    )
       
    result = ner(prompt)
    print(result)

if __name__ == "__main__":
    main()
