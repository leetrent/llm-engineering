import sys
import argparse
from instruct_models import get_model
from messages import append_user_message, get_messages
from generator import generate

def parse_args():
    p = argparse.ArgumentParser(description="Run a local LLM.")
    p.add_argument("MODEL", help="Model key (e.g., PHI3, QWEN2, GEMMA2, TINY)")
    p.add_argument("MESSAGE", nargs="+", help="User message (can contain spaces)")
    p.add_argument("--tokens", type=int, default=256, help="Max new tokens (default: 256)")
    return p.parse_args()

def main():
    if len(sys.argv) < 3:
        print("❌ Usage; python main.py <MODEL> <MESSAGE>")
        sys.exit(1)
        
    args = parse_args()
    model_key = args.MODEL
    user_message = " ".join(args.MESSAGE)
    
    print("model_key...:", model_key)
    print("user_message:", user_message)
    
    try:
        model_name = get_model(model_key)
        print("model_name:", model_name)
    except KeyError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)   
        
    print("messages[BEFORE]", get_messages())
    append_user_message(user_message)
    print("messages[AFTER]", get_messages())
    
    generate(model_name, get_messages(), max_new_tokens=args.tokens)
    
if __name__ == "__main__":
    main()