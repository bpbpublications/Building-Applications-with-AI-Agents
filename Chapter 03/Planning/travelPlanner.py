

# This code is a simple travel planner agent that uses the SearchAPI.io to search for flights and hotels.
import requests

SEARCHAPI_KEY = "your_searchapi_key" # Replace with your actual SearchAPI.io key


class TripPlannerAgent:
    def __init__(self, origin, destination, departure_date, return_date=None):
        self.origin = origin
        self.destination = destination
        self.departure_date = departure_date
        self.return_date = return_date

    def search_flights(self, origin, destination, departure_date,return_date=None):
        url = "https://www.searchapi.io/api/v1/search"
        params = {"engine":"google_flights","flight_type": "round_trip","departure_id": origin,"arrival_id": destination,
            "outbound_date": departure_date,"return_date": return_date,"api_key": SEARCHAPI_KEY}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            try:
                flight = data['best_flights'][0]
                info= flight['flights'][0]
                airline = info['airline']
                departure_airport = info['departure_airport']['name']    
                arrival_airport = info['arrival_airport']['name']
                return f"Flight: {airline} from {departure_airport} to {arrival_airport} at {flight['price']}"
            except:
                return "No flights found."
        return "Flight search failed."

    def search_hotels(self, city, departure_date, return_date):
        url = "https://www.searchapi.io/api/v1/search"
        city='Mumbai' 
        params = {"engine": "google_hotels","q": f"hotels in {city}", "check_in_date": departure_date,
            "check_out_date": return_date,"api_key": SEARCHAPI_KEY}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            hotel= data['properties'][0]
            try:
                hotel = data['properties'][0]
                return f"Hotel: {hotel['name']} at {hotel ['city']} - {hotel['price_per_night']['price'] } per night"  
            except:
                return "No hotels found."
        return "Hotel search failed."

    def plan_trip(self):
        print("Planning your trip...\n")
        flight_info = self.search_flights(self.origin, self.destination, self.departure_date,self.return_date) #Searching Flights
        hotel_info = self.search_hotels(self.destination, self.departure_date, self.return_date) #Searching Hotels

        print("Trip Plan:")
        print(flight_info)
        print(hotel_info)

if __name__ == "__main__": # Example usage
    planner = TripPlannerAgent("DEL", "BOM", "2025-05-31","2025-06-02")  # DEL = Delhi, BOM = Mumbai
    planner.plan_trip()

#Output: 
# Trip Plan:
# Flight: IndiGo from Indira Gandhi International Airport to Chhatrapati Shivaji Maharaj International Airport Mumbai at 120
# Hotel: Fairfield by Marriott Mumbai International Airport at Mumbai - $86 per night