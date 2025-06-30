import os
import json
from dotenv import load_dotenv
from chatgpt import ChatGPT
import gradio as gr

def chat_with_llm(message, history):
    try:     
        load_dotenv(override=True)   
        model = os.getenv("TARGET_MODEL", "ChatGPT")
        
        ##########################################################################
        # MESSAGE
        ##########################################################################   
        print(f"\nMAIN (target_model):")  
        print(model)    
               
        system_message = "You are a helpful assistant for an Airline called FlightAI. "
        system_message += "Give short, courteous answers, no more than 1 sentence. "
        system_message += "Always be accurate. If you don't know the answer, say so."
               
        if model == "ChatGPT":
            result = ChatGPT(system_message, history, message).generate_text_response()
        else:
            raise ValueError(f"Unsupported model: {model}")
           
        return result
    except Exception as e:
        raise RuntimeError(f"Call to {model} failed: {e}")
  
def main():
    gr.ChatInterface(fn=chat_with_llm, type="messages").launch(share=True)
    
if __name__ == "__main__":
  main()