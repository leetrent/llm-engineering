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
    
    for ii in range(5):
        gpt_next_message = chatGPT.generate_text_response()
        print(f"\n[{ii}] ChatGPT: ", gpt_next_message)
        chatGPT.append_assistant_message(gpt_next_message)
        claude.append_user_message(gpt_next_message)
        
        claude_next_message = claude.generate_text_response()
        print(f"\n[{ii}] Claude: ", claude_next_message)
        claude.append_assistant_message(claude_next_message)
        chatGPT.append_user_message(claude_next_message)

if __name__ == "__main__":
    main()