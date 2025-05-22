# WebSummary

**WebSummary** is a command-line Python tool that scrapes the visible text content of a webpage and summarizes it using OpenAI's GPT-4o model.

## 📦 Features

- Extracts meaningful text from webpages using `BeautifulSoup`
- Sends content to OpenAI's GPT-4o model for summarization
- Saves both raw text and the summary to a local `output/` folder
- CLI support: pass the URL directly via command line

## 🚀 Usage

```bash
python summarize_website.py https://example.com
