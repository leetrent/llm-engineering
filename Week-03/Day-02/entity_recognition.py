import sys
from transformers import pipeline

def main():
    if len(sys.argv) < 2:
        print("❌ Please provide a prompt.")
        sys.exit(1)

    prompt = sys.argv[1]
    print(f"\n🧠 Prompt: {prompt}\n")

    ner = pipeline(
        "ner",
        model="dslim/bert-base-NER",
        aggregation_strategy="simple",
        device="cuda"
    )

    result = ner(prompt)

    # Pretty print header
    print(f"{'Entity':<20} {'Type':<10} {'Score':<8} {'Start':<6} {'End':<6}")
    print("-" * 60)

    # Pretty print each entity
    for entity in result:
        word = entity['word']
        ent_type = entity['entity_group']
        score = round(float(entity['score']), 4)
        start = entity['start']
        end = entity['end']

        print(f"{word:<20} {ent_type:<10} {score:<8} {start:<6} {end:<6}")

if __name__ == "__main__":
    main()
