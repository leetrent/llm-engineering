from transformers import AutoTokenizer
from huggingface_hub import login
from api_key import retrieve_api_key_value

class Tokenizer:
    def __init__(self, model, text):
        self.model = model
        self.text = text
        
        # Authenticate with Hugging Face
        #login(retrieve_api_key_value("HF_TOKEN"), add_to_git_credential=True)
    
        tokenizer = AutoTokenizer.from_pretrained(model, trust_remote_code=True)
        self.encoded_tokens = tokenizer.encode(text)
        self.decoded_tokens = tokenizer.decode(self.encoded_tokens)
        self.batch_decoded_tokens = tokenizer.batch_decode(self.encoded_tokens)
        self.added_vocab = tokenizer.get_added_vocab()
        
    def print_all(self):
        print()
        print("Model:")
        print(self.model)
        print()
        print("Text:")
        print(self.text)
        print()
        print("Encoded Tokens:")
        print(self.encoded_tokens)
        print()
        print("Decoded Tokens:")
        print(self.decoded_tokens)
        print()
        print("Batch Decoded Tokens:")
        print(self.batch_decoded_tokens)
        print()
        print("Added Vocab (showing up to 10 items):")
        for i, token in enumerate(self.added_vocab):
            print(f"{token}")
            if i == 9:
                remaining = len(self.added_vocab) - 10
                if remaining > 0:
                    print(f"... and {remaining} more.")
                break
