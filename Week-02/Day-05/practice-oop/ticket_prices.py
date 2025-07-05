class TicketPrices:
    def __init__(self):
        self.model = "gpt-4o-mini"
        self.tools = [{"type": "function", "function": self.ticket_price_function}]
        self._set_system_message()
        self._set_ticket_prices()
        self._set_ticket_price_function()
        
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