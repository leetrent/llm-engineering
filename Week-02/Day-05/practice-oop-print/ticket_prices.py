import json
from openai import OpenAI
from api_key import retrieve_api_key_value
from image import generate_image
from speech import generate_speech

class TicketPrices:
    def __init__(self):
        self.model = "gpt-4o-mini"
        self._set_system_message()
        self._set_ticket_prices()
        self._set_ticket_price_function()
        self.tools = [{"type": "function", "function": self.ticket_price_function}]
        
    def _set_system_message(self):
        self.system_message =   "You are a helpful assistant for an Airline called FlightAI. " \
                                "Give short, courteous answers, no more than 1 sentence. " \
                                "Always be accurate. If you don't know the answer, say so."
                                
    def _set_ticket_prices(self):
        self.ticket_prices = {  "london": "$199.99", 
                                "paris": "$299.99", 
                                "new york": "$399.99", 
                                "amsterdam": "$499.99",
                                "munich": "$599.99",
                                "milan": "$699.99",
                                "tokyo": "$799.99", 
                                "copenhagen": "$899.99",
                                "zurich": "$999.99",
                                "budapest": "$1,099.00",
                                "lisbon": "$1,199.99"}
        print()
        print(self.ticket_prices)
        print()
        
    def _set_ticket_price_function(self):
        self.ticket_price_function = {
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
    
    def get_ticket_price(self, p_destination):
        return self.ticket_prices.get(p_destination.lower(), "Unknown")
        
    def _handle_tool_call(self, message):
        log_snippet = "[ticket_prices.py][_handle_tool_call] =>"
        
        print()
        print(f"{log_snippet} (message):")
        print(message)
        print()
        
        tool_call = message.tool_calls[0]
        arguments = json.loads(tool_call.function.arguments)
        city = arguments.get('destination_city')
        price = self.get_ticket_price(city)
        
        print()
        print(f"{log_snippet} (tool_call):")
        print(tool_call)
        print()
        
        print()
        print(f"{log_snippet} (arguments):")
        print(arguments)
        print()
        
        print()
        print(f"{log_snippet} (city):")
        print(city)
        print()
        
        print()
        print(f"{log_snippet} (price):")
        print(price)
        print()
        
        
        response = {
            "role": "tool",
            "content": json.dumps({"destination_city": city,"price": price}),
            "tool_call_id": tool_call.id
        }
        
        print()
        print(f"{log_snippet} (response):")
        print(response)
        print()
        
        return response, city

    def _generate_image_prompt(self, destination):
        return f"An image, in an vibrant pop-art style, representing a vacation in {destination}, showing tourist spots and everything unique about {destination}."
        
        
    def generate_response(self, p_history):
        all_messages = [{"role": "system", "content": self.system_message}] + p_history
        openai = OpenAI(api_key=retrieve_api_key_value("OPENAI_API_KEY"))
        response = openai.chat.completions.create(model=self.model, messages=all_messages, tools=self.tools)
        image = None
        
        print()
        print("[ticket_prices.py][generate_response] => (response #1):")
        print(response)
        print()
        
        if response.choices[0].finish_reason=="tool_calls":
            message = response.choices[0].message
            response, city = self._handle_tool_call(message)
            all_messages.append(message)
            all_messages.append(response)
            image = generate_image(self._generate_image_prompt(city))
            response = openai.chat.completions.create(model=self.model, messages=all_messages)
            
        print()
        print("[ticket_prices.py][generate_response] => (response #2):")
        print(response)
        print()
            
        reply = response.choices[0].message.content
        p_history += [{"role":"assistant", "content":reply}]
        
        print()
        print("[ticket_prices.py][generate_response] => (reply):")
        print(reply)
        print()
        
        print()
        print("[ticket_prices.py][generate_response] => (p_history):")
        print(p_history)
        print()
        
        generate_speech(reply)
        
        return p_history, image