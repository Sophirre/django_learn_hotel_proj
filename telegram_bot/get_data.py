import requests


class ApiGet:
    URL = "http://127.0.0.1:8000/hotels/api"

    @staticmethod
    def parser(req):
        return [el.get('title') for el in req]

    def get_hotels(self, city):
        req = requests.get(f"{self.URL}/hotels", params={"city": city})
        print(req.json())
        return self.parser(req.json())

    def get_bookings(self, name=None):
        if name:
            req = requests.get(f"{self.URL}/bookings", params={'guest_name': name})
            print(req.text)
        else:
            req = requests.get(f"{self.URL}/bookings")
        return req.json()

    def make_reservation(self, data):
        return requests.post(f"{self.URL}/bookings", data=data)
