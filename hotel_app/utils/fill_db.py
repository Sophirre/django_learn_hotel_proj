from random import choice, randint

from django.db import IntegrityError

from hotel_app.models import (
    City,
    Hotel,
    Room,
    Booking
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
    hotels = [Hotel(title=f"Hotel_{letter}") for letter in HOTELS_LETTERS]
    for hotel in hotels:
        hotel.city = choice(cities)
        try:
            # TODO: cities iteration and bulk_create()
            hotel.save()
            hotel_rooms_amount = randint(100, 1000)
            create_room(hotel, hotel_rooms_amount)
        except IntegrityError as e:
            print(f"{hotel} already exist in the {hotel.city}")


def create_room(hotel, hotel_rooms_amount):
    print(f"Create {hotel_rooms_amount} rooms for {hotel} hotel")
    # TODO: Finish function
    rooms = []
    for num in range(1, hotel_rooms_amount):
        room = Room(
            hotel=hotel,
            room_number=num,
            beds=randint(1,4)
        )
        rooms.append(room)
    Room.objects.bulk_create(rooms)
# 1. Write create_room logic in fill_db.py
# 2. Create url + view to show all available hotels in DB
def main():
     create_cities()
     create_hotel()
