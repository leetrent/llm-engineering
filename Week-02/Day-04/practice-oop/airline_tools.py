import json
from ticket_prices import TicketPrices

class AirlineTools:
    def __init__(self):
        self._set_price_function()
        self.price_function_tool = [{"type": "function", "function": self.price_function}]
    
    def _set_price_function(self):
        self.price_function = {
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
        
        
    def handle_price_function_tool_call(self, message):
        tool_call = message.tool_calls[0]
        arguments = json.loads(tool_call.function.arguments)
        city = arguments.get('destination_city')
        price = TicketPrices().get_ticket_price(city)
        response = {
            "role": "tool",
            "content": json.dumps({"destination_city": city,"price": price}),
            "tool_call_id": tool_call.id
        }
        return response, city
            
        
    