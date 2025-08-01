import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

MODEL = "gpt-4o-mini"

system_message = "You are a helpful assistant for an Airline called FlightAI. "
system_message += "Give short, courteous answers, no more than 1 sentence. "
system_message += "Always be accurate. If you don't know the answer, say so."

ticket_prices = {"london": "$199", 
                "paris": "$299", 
                "new york": "399", 
                "amsterdam": "$499",
                "munich": "$599",
                "milan": "$699",
                "tokyo": "$799", 
                "copenhagen": "$899"}

price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city. Call this whenever you need to know the ticket price, for example when a customer asks 'How much is a ticket to this city'",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": price_function}]

def get_api_key():
    load_dotenv(override=True)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("❌ No API key found for OpenAI in .env.")
    return api_key

def get_ticket_price(destination_city):
    #print(f"Tool get_ticket_price called for {destination_city}")
    city = destination_city.lower()
    return ticket_prices.get(city, "Unknown")
    
def handle_tool_call(message):
    print("")
    print(f"[ChatGPT][handle_tool_call] => (message)")
    print(message)
    print("")
    
    tool_call = message.tool_calls[0]
    print("")
    print(f"[ChatGPT][handle_tool_call] => (tool_call)")
    print(tool_call)
    print("")
     
    arguments = json.loads(tool_call.function.arguments)
    print("")
    print(f"[ChatGPT][handle_tool_call] => (arguments)")
    print(arguments)
    print("")
    
    city = arguments.get('destination_city')
    print("")
    print(f"[ChatGPT][handle_tool_call] => (city)")
    print(city)
    print("")
    
    price = get_ticket_price(city)
    print("")
    print(f"[ChatGPT][handle_tool_call] => (price)")
    print(price)
    print("")  
    
    response = {
        "role": "tool",
        "content": json.dumps({"destination_city": city,"price": price}),
        "tool_call_id": tool_call.id
    }
    print("")
    print(f"[ChatGPT][handle_tool_call] => (response)")
    print(response)
    print("")    
    
    return response, city
    
def chat(message, history):   
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    openai = OpenAI(api_key=get_api_key())
    response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)

    print("")
    print(f"[ChatGPT][chat] => (response #1):")
    print(response)
    print("")   

    if response.choices[0].finish_reason=="tool_calls":
        message = response.choices[0].message
        response, city = handle_tool_call(message)
        messages.append(message)
        messages.append(response)
        response = openai.chat.completions.create(model=MODEL, messages=messages)
        
    print("")
    print(f"[ChatGPT][chat] => (response #2):")
    print(response)
    print("")   

    return response.choices[0].message.content
  
def main():
    gr.ChatInterface(fn=chat, type="messages").launch()
    
if __name__ == "__main__":
  main()