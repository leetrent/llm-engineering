from chatgpt import ChatGPT
from claude import Claude

def main():
    
    ################################################################################        
    # Instantiate both the ChatGPT and Claude classes
    ################################################################################
    chatGPT = ChatGPT()
    claude = Claude()
    
    ################################################################################        
    # ChatGPT initiates conversation
    ################################################################################
    chatGPT.append_assistant_message("Hi there") 
    claude.append_user_message("Hi there") 
    
    ################################################################################        
    # Claude replies back first
    ################################################################################
    claude_first_reply = claude.generate_text_response()
    print(f"\n[{-1}] Claude: ", claude_first_reply)
    
    ################################################################################        
    # Append Claude's first reply to ChatGPT's list of user messages
    ################################################################################
    chatGPT.append_user_message(claude_first_reply)
     
    ################################################################################        
    # Append Claude's first reply to Claude's list of assistant messages
    ################################################################################   
    claude.append_assistant_message(claude_first_reply)
                
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
        


    # print("\nChatGPT Initial Messages:")
    # for message in chatGPT.messages:
    #     print(f"\nRole: {message['role']}\nContent: {message['content']}")
        
    # print("\nClaude Initial Messages:")
    # for message in claude.messages:
    #     print(f"\nRole: {message['role']}\nContent: {message['content']}")

if __name__ == "__main__":
    main()