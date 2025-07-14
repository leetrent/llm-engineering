import csv

CSV_FILE = "airline_tickets.csv"

def load_ticket_prices(filename=CSV_FILE):
    """Load ticket prices and booking status from the CSV file."""
    prices = {}
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            prices[row["Destination"]] = {
                "Price": float(row["Price"]),
                "Booked": row["Booked"]
            }
    return prices

def mark_as_booked(destination, filename=CSV_FILE):
    """Update 'Booked' status to 'Yes' for the given destination."""
    rows = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    for row in rows:
        if row["Destination"].lower() == destination.lower():
            row["Booked"] = "Yes"

    with open(filename, mode="w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Destination", "Price", "Booked"])
        writer.writeheader()
        writer.writerows(rows)
        
def print_ticket_prices(title, ticket_prices):
    print()
    print(title)
    for destination, info in ticket_prices.items():
        print(f"{destination}: Price ${info['Price']}, Booked: {info['Booked']}")
    print()

def main():
    print_ticket_prices("Original ticket prices:", load_ticket_prices())
    
    mark_as_booked("Miami")

    print_ticket_prices("Updated ticket prices:", load_ticket_prices())
    
if __name__ == "__main__":
  main()