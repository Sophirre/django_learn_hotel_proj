from random import choice, randint

from django.db import IntegrityError

from hotel_app.models import (
    City,
    Hotel,
    Room,
)
from hotel_app.utils.constants import (
    CITIES,
    HOTELS_LETTERS,
)


def create_cities():
    cities = [City(title=city) for city in CITIES]
    # IntegrityError -> django.db
    try:
        City.objects.bulk_create(cities)
    except IntegrityError:
        print(f"{cities}: some of these cities already exists")


def create_hotel():
    cities = City.objects.all()
    hotels = []
    for city in cities:
        letters = HOTELS_LETTERS.copy()
        print(f'Create hotels for city: {city}')
        for _ in range(4, 11):
            letter = choice(HOTELS_LETTERS)
            try:
                letters.pop(letters.index(letter))

            except ValueError:
                continue
            title = f"Hotel_{letter}"
            print(title)
            city = city
            hotel_obj = Hotel(title=title, city=city)
            hotels.append(hotel_obj)
    Hotel.objects.bulk_create(hotels)


def create_room():
    hotels = Hotel.objects.all()
    rooms = []
    for hotel in hotels:
        hotel_rooms_amount = randint(20, 500)
        print(f"Create {hotel_rooms_amount} rooms for {hotel}")
        for num in range(1, hotel_rooms_amount):
            room = Room(
                hotel=hotel,
                room_number=num,
                beds=randint(1, 4)
            )
            rooms.append(room)
    Room.objects.bulk_create(rooms)


def main():
    create_cities()
    create_hotel()
    create_room()
