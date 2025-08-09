import sys
from instruct_models import get_model
from messages import append_user_message, get_messages

def main():
    if len(sys.argv) < 3:
        print("❌ Usage; python main.py <MODEL> <MESSAGE>")
        sys.exit(1)
        
    model_name = sys.argv[1]
    user_message = sys.argv[2]
    
    print("model_name:", model_name)
    print("user_message:", user_message)
    
    try:
        model = get_model(model_name)
        print("model:", model)
    except KeyError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)   
        
    print("messages[BEFORE]", get_messages())
    append_user_message(user_message)
    print("messages[AFTER]", get_messages())
    
if __name__ == "__main__":
    main()