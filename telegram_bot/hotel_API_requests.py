import requests


class ApiData:
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
        headers = {'content-types': 'application/javascript',
                   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                                 'AppleWebKit/537.36 (KHTML, like Gecko)'
                                 'Chrome/99.0.4844.84'
                                 'Safari/537.36 OPR/85.0.4341.75',
                   'Content-type': 'application/json',
                   'Accept': '*/*'}
        r = requests.post(f"{self.URL}/bookings/", data=data, headers=headers)
        return r
