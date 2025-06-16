from chatgpt import ChatGPT
from claude import Claude
from transcript import Transcript

def main():
    
    ################################################################################        
    # Instantiate the ChatGPT and Claude classes
    ################################################################################
    chatGPT = ChatGPT()
    claude = Claude()
    
    ################################################################################        
    # Instantiate Transcript class and wipe the transcript clean
    ################################################################################
    transcript = Transcript("AdversarialChatbotConversation-Lee.txt")
    
    ################################################################################        
    # ChatGPT initiates conversation
    ################################################################################
    chatGPT.append_assistant_message("Hi there") 
    claude.append_user_message("Hi there") 
    
    ################################################################################        
    # Claude replies back first
    ################################################################################
    claude_first_reply = claude.generate_text_response()
    
    ################################################################################        
    # Write Claude's first reply to the transcript log and to the console.
    ################################################################################
    transcript.log("Claude", -1, claude_first_reply)
    print(f"\n[{-1}] Claude:\n", claude_first_reply)
    
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
        ################################################################################        
        # Process ChatGPT's next message
        ################################################################################    
        gpt_next_message = chatGPT.generate_text_response()
        chatGPT.append_assistant_message(gpt_next_message)
        claude.append_user_message(gpt_next_message)
        
        ################################################################################        
        # Write ChatGPT's message to the transcript log and to the console.
        ################################################################################
        transcript.log("ChatGPT", ii, gpt_next_message)
        print(f"\n[{ii}] ChatGPT:\n", gpt_next_message)
        
        ################################################################################        
        # Process Claude's next message
        ################################################################################ 
        claude_next_message = claude.generate_text_response()
        claude.append_assistant_message(claude_next_message)
        chatGPT.append_user_message(claude_next_message)
        
        ################################################################################        
        # Write Claude's message to the transcript log and to the console.
        ################################################################################
        transcript.log("Claude", ii, claude_next_message)
        print(f"\n[{ii}] Claude:\n", claude_next_message)
     

    # print("\nChatGPT Initial Messages:")
    # for message in chatGPT.messages:
    #     print(f"\nRole: {message['role']}\nContent: {message['content']}")
        
    # print("\nClaude Initial Messages:")
    # for message in claude.messages:
    #     print(f"\nRole: {message['role']}\nContent: {message['content']}")

if __name__ == "__main__":
    main()