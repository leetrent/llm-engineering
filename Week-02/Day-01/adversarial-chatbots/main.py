from chatgpt import ChatGPT
from claude import Claude

def main():
    
    ################################################################################
    # ChatGPT
    ################################################################################
    chatGPT = ChatGPT()
    chatGPT.append_assistant_message("Hi there")
    chatGPT.append_user_message("Hi")
    
    print("\nChatGPT Initial Messages:")
    for message in chatGPT.messages:
        print(f"\nRole: {message['role']}\nContent: {message['content']}")
    
    ################################################################################        
    # Claude
    ################################################################################
    claude = Claude()
    claude.append_user_message("Hi there")
    claude.append_assistant_message("Hi")
    
    print("\nClaude Initial Messages:")
    for message in claude.messages:
        print(f"\nRole: {message['role']}\nContent: {message['content']}")
        
    ################################################################################
    # ChatGPT Intial Response
    ################################################################################
    print("\nChatGPT (first reply): ", chatGPT.generate_text_response())
    
    ################################################################################
    # Claude Intial Response
    ################################################################################
    print("\nClaude (first reply): ", claude.generate_text_response())
       
    ################################################################################
    # Conversation Loop
    ################################################################################
    print("\n=== Conversation Loop ===")   
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