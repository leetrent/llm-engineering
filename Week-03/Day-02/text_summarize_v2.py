import sys
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

def split_into_chunks(text, tokenizer, max_tokens=1024, stride=100):
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = []
    current_tokens = 0

    for sentence in sentences:
        sentence_tokens = len(tokenizer.encode(sentence, add_special_tokens=False))
        if current_tokens + sentence_tokens > max_tokens:
            chunks.append(" ".join(current_chunk))
            # Keep a bit of overlap for context
            current_chunk = current_chunk[-stride:] if stride > 0 else []
            current_tokens = sum(len(tokenizer.encode(s, add_special_tokens=False)) for s in current_chunk)

        current_chunk.append(sentence)
        current_tokens += sentence_tokens

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def summarize_chunks(chunks, model, tokenizer, device):
    summaries = []
    for i, chunk in enumerate(chunks, 1):
        print(f"🧩 Summarizing chunk {i}/{len(chunks)}...")
        inputs = tokenizer(chunk, return_tensors="pt", truncation=True, max_length=1024).to(device)

        summary_ids = model.generate(
            inputs["input_ids"],
            max_length=150,
            min_length=40,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True
        )
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        summaries.append(summary)
    return summaries

def main():
    if len(sys.argv) < 2:
        print("❌ Please provide the input filename.")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = "summary.txt"

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            full_text = f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {input_file}")
        sys.exit(1)

    model_name = "facebook/bart-large-cnn"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)

    # Step 1: Chunk the input
    chunks = split_into_chunks(full_text, tokenizer, max_tokens=1024, stride=100)

    # Step 2: Summarize each chunk
    summaries = summarize_chunks(chunks, model, tokenizer, device)

    # Step 3: Optionally, summarize the summaries (recursive)
    combined_summary = " ".join(summaries)
    inputs = tokenizer(combined_summary, return_tensors="pt", truncation=True, max_length=1024).to(device)
    final_summary_ids = model.generate(
        inputs["input_ids"],
        max_length=150,
        min_length=40,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )
    final_summary = tokenizer.decode(final_summary_ids[0], skip_special_tokens=True)

    # Output
    print(f"\n📝 FINAL SUMMARY:\n{'-' * 80}\n{final_summary}\n")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_summary)
    print(f"✅ Summary saved to: {output_file}")

if __name__ == "__main__":
    main()
