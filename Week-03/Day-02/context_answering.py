import sys
from transformers import pipeline

def main():
    question_answerer = pipeline("question-answering", device="cuda")
    result = question_answerer(question="Who was the 44th president of the United States?", context="Barack Obama was the 44th president of the United States.")
    print(result)

if __name__ == "__main__":
    main()
