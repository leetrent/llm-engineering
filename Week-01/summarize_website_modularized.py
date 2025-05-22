import argparse
from webscraper import Website
from summarizer import summarize_text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape and summarize a webpage")
    parser.add_argument("url", help="The URL of the website to summarize")
    args = parser.parse_args()

    site = Website(args.url)

    print(f"\n🌐 Title: {site.title}")
    print("🧠 Summarizing page content using GPT-4o...")

    summary = summarize_text(site.text)

    print(f"\n📄 Summary:\n{summary}")

    # Save results to file
    domain = site.url.split("//")[-1].split("/")[0]
    filename = f"{domain.replace('.', '_')}_summary.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"🌐 Title: {site.title}\n\n")
        file.write("📄 Raw Page Text:\n")
        file.write(site.text)
        file.write("\n\n🧠 GPT-4o Summary:\n")
        file.write(summary)

    print(f"\n✅ Summary saved to: {filename}")
