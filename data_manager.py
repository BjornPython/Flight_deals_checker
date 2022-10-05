import requests
from datetime import datetime as dt, timedelta


class DataManager:

    def __init__(self, sheety_token, sheety_project, sheety_sheet, tequila_api, days=31):
        self.sheety_token = sheety_token
        self.sheety_project = sheety_project
        self.sheet = sheety_sheet
        self.sheet_endpoint = f"https://api.sheety.co/7aa1d32afbdba9a0220c39f7d9030478/{self.sheety_project}/{self.sheet}"

        self.sheety_header = {
            "Authorization": f"Bearer {sheety_token}"
        }
        self.tequila_api = tequila_api
        self.tequila_endpoint = "https://tequila-api.kiwi.com"
        self.tequila_header = {"apikey": self.tequila_api}
        self.data = self.get_data()["prices"]
        self.can_buy = []
        self.date_now = dt.now().strftime("%#d/%#m/%Y")
        self.date_to = (dt.now() + timedelta(days=days)).strftime("%#d/%#m/%Y")

    def get_data(self):
        """Gets the data from the Google sheet."""
        sheet_response = requests.get(
            self.sheet_endpoint,
            headers=self.sheety_header
        )
        print(sheet_response.json())
        return sheet_response.json()

    def update_codes(self):
        """Gets the IATA code for every
        city in the Google sheet."""
        for city in self.data:
            if city["iataCode"] == "":
                new_data = {
                    "price": {
                        "iataCode": self.get_code(city["city"])
                    }
                }
                response = requests.put(url=f"{self.sheet_endpoint}/{city['id']}",
                                        json=new_data,
                                        headers=self.sheety_header)
                print(response.text)

    def get_code(self, city):
        """Uses an api from tequila to get
        the IATA code of a given city name."""
        location_endpoint = f"{self.tequila_endpoint}/locations/query"
        query = {"term": city, "location_types": "city"}
        response = requests.get(url=location_endpoint, headers=self.tequila_header, params=query)
        code = response.json()["locations"][0]["code"]
        return code

    def search_flights(self):
        """Searches the flights available and
         are in your budget in your Google sheet."""
        for city in self.data:
            price, link = self.search_price(city["iataCode"])
            budget = int(city["lowestPrice"])
            print(f"{price} vs {budget}")
            if price and price <= budget:
                print("can buy")
                self.can_buy.append([city["city"], price, link])
            else:
                print("cannot buy")

    def search_price(self, to_city, from_city="MNL"):
        search_endpoint = f"{self.tequila_endpoint}/v2/search"
        print(to_city)
        query = {
            "fly_from": from_city,
            "fly_to": to_city,
            "date_from": self.date_now,
            "date_to": self.date_to,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "PHP"
        }

        response = requests.get(url=search_endpoint, headers=self.tequila_header, params=query,
                                )
        print("response: ", response.json())
        try:
            data = response.json()["data"][0]

        except KeyError:
            return None, None

        except IndexError:
            return None, None

        else:
            price = data["price"]
            link = data["deep_link"]
            print("price: ", price, "link: ", link)
            return int(price), link
