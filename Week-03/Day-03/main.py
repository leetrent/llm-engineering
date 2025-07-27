import sys
from tokenizer import Tokenizer

def main():
    if len(sys.argv) < 3:
        print("❌ Usage: python main.py <MODEL_TYPE> <TEXT_TO_TOKENIZE>")
        sys.exit(1)
    
    model_type = sys.argv[1].upper()
    text = sys.argv[2]
    
    if model_type == 'LLAMA':
        model = "meta-llama/Meta-Llama-3.1-8B"
    elif model_type == "PHI3":
        model = "microsoft/Phi-3-mini-4k-instruct"
    else:
        print("❌ Invalid model type. Supported: LLAMA")
        sys.exit(1)
    
    tokenizer = Tokenizer(model, text)
    tokenizer.print_all()

if __name__ == "__main__":
    main()
