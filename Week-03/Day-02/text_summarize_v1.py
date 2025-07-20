import sys
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

def main():
    if len(sys.argv) < 2:
        print("❌ Please provide the input filename.")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = "summary.txt"

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            prompt = f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {input_file}")
        sys.exit(1)

    # Load model and tokenizer manually
    model_name = "facebook/bart-large-cnn"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to("cuda")

    # Tokenize with truncation (max 1024 tokens for BART)
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024).to("cuda")

    # Generate summary
    summary_ids = model.generate(
        inputs["input_ids"],
        max_length=150,
        min_length=40,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )
    summary_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    # Output results
    print(f"📝 SUMMARY:\n{'-' * 80}\n{summary_text}\n")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(summary_text)

    print(f"✅ Summary saved to: {output_file}")

if __name__ == "__main__":
    main()
