import sys
from instruct_models import get_model

def main():
    if len(sys.argv) < 3:
        print("❌ Usage; python main.py <MODEL> <MESSAGE>")
        sys.exit(1)
        
    model_name = sys.argv[1]
    message = sys.argv[2]
    
    print("model_name:", model_name)
    print("message:", message)
    
    try:
        model = get_model(model_name)
        print("model:", model)
    except KeyError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)   
    
if __name__ == "__main__":
    main()