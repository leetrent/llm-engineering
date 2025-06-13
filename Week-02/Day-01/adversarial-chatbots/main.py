from chatgpt import ChatGPT
from claude import Claude

def main():
    chatGPT = ChatGPT()
    chatGPT.append_assistant_message("Hi there")
    chatGPT.append_user_message("Hi")
    print("ChatGPT: ", chatGPT.generate_text_response())
    
    claude = Claude()
    claude.append_user_message("Hi there")
    chatGPT.append_assistant_message("Hi")
    print("Claude: ", claude.generate_text_response())

if __name__ == "__main__":
    main()