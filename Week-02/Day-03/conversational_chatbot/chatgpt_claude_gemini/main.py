import os
from dotenv import load_dotenv
from chatgpt import ChatGPT
from claude import Claude
from gemini import Gemini
import gradio as gr

model = "Gemini"
system_message = "You are a friendly, helpful and honest assistant who answers all questions pertaining to veganism and only veganism and responds in markdown."

def convert_to_claude(messages):
    return [
        {
            "role": msg["role"],
            "content": msg["content"]
        }
        for msg in messages
    ]

def convert_to_gemini(messages):
    return [
        {
            "role": msg["role"],
            "parts": [{"text": msg["content"]}]
        }
        for msg in messages
    ]

def chat_with_llm(message, history):
    try:     
        load_dotenv(override=True)   
        model = os.getenv("TARGET_MODEL", "ChatGPT")
        
        ##########################################################################
        # MESSAGE
        ##########################################################################   
        print(f"\nTARGET_MODEL:")  
        print(model)    
        
        ##########################################################################
        # MESSAGE
        ##########################################################################   
        print(f"\nMESSAGE:")  
        print(message)    
               
        ##########################################################################
        # HISTORY
        ##########################################################################   
        print(f"\nHISTORY:")  
        for hist in history:
            print(f"\n{hist}")     
    
        ##########################################################################
        # USER AND ASSISTANT MESSAGES
        ##########################################################################
        user_assistant_messages = history + [{"role": "user", "content": message}]
            
        ##########################################################################
        # ALL MESSAGES
        ##########################################################################
        all_messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
               
        if model == "ChatGPT":
            result = ChatGPT(all_messages).stream_response()
        elif model == "Claude":
            result = Claude(system_message, convert_to_claude(user_assistant_messages)).stream_response()
        elif model == "Gemini":
            result = Gemini(system_message, convert_to_gemini(user_assistant_messages)).stream_response()
        else:
            raise ValueError(f"Unsupported model: {model}")
    
        yield from result
    except Exception as e:
        raise RuntimeError(f"Call to {model} failed: {e}")
  
def main():
    gr.ChatInterface(fn=chat_with_llm, type="messages").launch(share=True)
    
if __name__ == "__main__":
  main()