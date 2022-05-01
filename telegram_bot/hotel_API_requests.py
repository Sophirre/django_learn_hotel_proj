import requests


class ApiData:
    def __init__(self):
        self.URL = "http://127.0.0.1:8000/hotels/api"

    @staticmethod
    def hotel_titles_parser(res):
        return [el.get('title') for el in res]

    def get_hotels(self, city):
        api_url = self.URL + "/hotels"
        res = requests.get(api_url, params={"city": city})
        print(f"[GET] response from {api_url}: {res.json()}")
        return self.hotel_titles_parser(res.json())

    def get_bookings(self, name=None):
        api_url = self.URL + "/bookings"
        if name:
            res = requests.get(f"{api_url}", params={'guest_name': name})
            print(f"[GET] response from {api_url}: {res.json()}")
        else:
            res = requests.get(f"{api_url}/bookings")
            print(f"[GET] response from {api_url}: {res.json()}")
        return res.json()

    def make_reservation(self, data):
        api_url = self.URL + "/bookings/"
        headers = {'content-types': 'application/javascript',
                   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                                 'AppleWebKit/537.36 (KHTML, like Gecko)'
                                 'Chrome/99.0.4844.84'
                                 'Safari/537.36 OPR/85.0.4341.75',
                   'Content-type': 'application/json',
                   'Accept': '*/*'}
        req = requests.post(api_url, data=data, headers=headers)
        print(f"[POST] request to {api_url}: {req.json()}")
        return req
