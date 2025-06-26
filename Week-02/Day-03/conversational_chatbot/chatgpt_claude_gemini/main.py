import os
import sys
from chatgpt import ChatGPT
from claude import Claude
from gemini import Gemini
import gradio as gr

model = "Claude"
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


def chat_with_gpt(message, history):
    try:
        ##########################################################################
        # MESSAGE
        ##########################################################################   
        print(f"\nMESSAGE:")
        print(f"\n{message}")  
            
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
        print(f"\nUSER AND ASSISTANT MESSAGES:")  
        for ua_message in user_assistant_messages:
            print(f"\n{ua_message}")
            
        ##########################################################################
        # CONVERT TO GEMINI
        ##########################################################################  
        gemini_messages = convert_to_gemini(user_assistant_messages)   
        print(f"\nGEMINI MESSAGES:")  
        for gemini_message in gemini_messages:
            print(f"\n{gemini_message}")
            
        ##########################################################################
        # ALL MESSAGES
        ##########################################################################
        all_messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
        print(f"\nALL  MESSAGES:")  
        for all_message in all_messages:
            print(f"\n{all_message}")      
               
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
    gr.ChatInterface(fn=chat_with_gpt, type="messages").launch(share=True)
    
if __name__ == "__main__":
  main()