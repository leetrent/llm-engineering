import os
import argparse
from website_summary.scraper import Website
from website_summary.summarizer import summarize_text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape and summarize a webpage")
    parser.add_argument("url", help="The URL of the website to summarize")
    parser.add_argument("llm", help="The larguage language model to be used.")
    args = parser.parse_args()
    
    print("args.url", args.url)
    print("args.llm", args.llm)

    site = Website(args.url)

    print(f"\n🌐 Title: {site.title}")
    #print("🧠 Summarizing page content using llama3.2...")
    print(f"Summarizing page content using {args.llm}:")

    summary = summarize_text(site.text, model=args.llm)

    print(f"\n📄 Summary:\n{summary}")

    # Create output folder if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Generate output filename from domain
    domain = site.url.split("//")[-1].split("/")[0]
    filename = f"{domain.replace('.', '_')}_summary.txt"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(f"🌐 Title: {site.title}\n\n")
        file.write("📄 Raw Page Text:\n")
        file.write(site.text)
        file.write("\n\n🧠 GPT-4o Summary:\n")
        file.write(summary)

    print(f"\n✅ Summary saved to: {filepath}")
