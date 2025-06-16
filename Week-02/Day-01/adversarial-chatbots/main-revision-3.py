from chatgpt import ChatGPT
from claude import Claude
from pathlib import Path

def log_to_transcript(role, turn, message, path):
    with path.open("a", encoding="utf-8") as f:
        f.write(f"[{turn}] {role}: {message}\n")

def main():

    transcript_path = Path("AdversarialChatbotConversation.txt")
    transcript_path.write_text("")  # Clear transcript at start

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
    print(f"[-1] Claude: ", claude_first_reply)
    log_to_transcript("Claude", -1, claude_first_reply, transcript_path)

    ################################################################################        
    # Append Claude's first reply
    ################################################################################
    chatGPT.append_user_message(claude_first_reply)
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
        log_to_transcript("ChatGPT", ii, gpt_next_message, transcript_path)

        claude_next_message = claude.generate_text_response()
        print(f"\n[{ii}] Claude: ", claude_next_message)
        claude.append_assistant_message(claude_next_message)
        chatGPT.append_user_message(claude_next_message)
        log_to_transcript("Claude", ii, claude_next_message, transcript_path)

if __name__ == "__main__":
    main()