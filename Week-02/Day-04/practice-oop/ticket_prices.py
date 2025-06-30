class TicketPrices:
    def __init__(self):
        self.ticket_prices = {"london": "$199", 
                              "paris": "$299", 
                              "new york": "399", 
                              "amsterdam": "$499",
                              "munich": "$599",
                              "milan": "$699",
                              "tokyo": "$799", 
                              "copenhagen": "$899"}
        
def get_ticket_price(self, destination_city):
    #print(f"Tool get_ticket_price called for {destination_city}")
    city = destination_city.lower()
    return self.ticket_prices.get(city, "Unknown")