import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic
import gradio as gr

MODEL = "claude-3-haiku-20240307"

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
    "input_schema": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"]
    }
}

tools = [price_function]

def get_api_key():
    load_dotenv(override=True)
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("❌ No API key found for Anthropic in .env.")
    return api_key

def get_ticket_price(destination_city):
    #print(f"Tool get_ticket_price called for {destination_city}")
    city = destination_city.lower()
    return ticket_prices.get(city, "Unknown")
    
def handle_tool_call(tool_use):
    city = tool_use.input.get('destination_city')
    price = get_ticket_price(city)
    response = {
        "type": "tool_result",
        "tool_use_id": tool_use.id,
        "content": json.dumps({"destination_city": city, "price": price})
    }
    return response, city
    
def chat(message, history):
    print("MESSAGE:\n", message)
    print("HISTORY:\n", history)
    for hist in history:
        print(f"\n{hist}")
    
    # Convert history to Anthropic format
    messages = []
    for hist in history:
        messages.append({"role": hist["role"], "content": hist["content"]})
    
    messages.append({"role": "user", "content": message})
    
    client = Anthropic(api_key=get_api_key())
    response = client.messages.create(
        model=MODEL, 
        max_tokens=1000,
        system=system_message,
        messages=messages, 
        tools=tools
    )

    # Handle tool calls
    if response.stop_reason == "tool_use":
        tool_use = None
        for content in response.content:
            if content.type == "tool_use":
                tool_use = content
                break
        
        if tool_use:
            tool_result, city = handle_tool_call(tool_use)
            
            # Add assistant's response with tool use
            messages.append({
                "role": "assistant", 
                "content": response.content
            })
            
            # Add tool result
            messages.append({
                "role": "user",
                "content": [tool_result]
            })
            
            # Get final response
            response = client.messages.create(
                model=MODEL,
                max_tokens=1000,
                system=system_message,
                messages=messages
            )

    return response.content[0].text
  
def main():
    gr.ChatInterface(fn=chat, type="messages").launch()
    
if __name__ == "__main__":
    main()