from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from hotel_app.models import (
    Hotel,
    Booking,
    City,
    Room
)

from hotel_app.utils.common import find_room


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ('room_number', 'beds', 'hotel')


class HotelSerializer(serializers.ModelSerializer):
    rooms_bed = serializers.ReadOnlyField(source='get_rooms_beds')
    city = serializers.CharField(source="city.title")

    class Meta:
        model = Hotel
        fields = ('title', 'city', 'rooms_bed')


class BookingSerializer(serializers.ModelSerializer):
    city = serializers.CharField(read_only=True)
    hotel = serializers.CharField(read_only=True)
    place = serializers.CharField(source="room.hotel")

    class Meta:
        model = Booking
        fields = (
            'guest_name',
            'booking_start',
            'booking_end',
            'city',
            'hotel',
            'persons',
            'place'
        )

    @staticmethod
    def get_hotel(city, hotel):
        try:
            city = City.objects.get(title=city)
            hotel = city.hotels.get(title=hotel)
        except ObjectDoesNotExist as e:
            raise serializers.ValidationError(
                {'error': f'{city}:{hotel} - {e}'}
            )
        print("Hotel Detected")
        return hotel

    def to_internal_value(self, data):
        print(f'Raw Booking data: {data}')
        internal_data = super(BookingSerializer, self).to_internal_value(data)
        self.city = data.get("city")
        self.hotel = self.get_hotel(self.city, data.get('hotel'))
        print('Internal Booking Data')
        return internal_data

    def create(self, validated_data):
        print(f"Validated Data: {validated_data}")
        booking_start = validated_data.pop("booking_start")
        booking_end = validated_data.pop("booking_end")
        persons = validated_data.pop("persons")
        room = find_room(persons, booking_start, booking_end, self.hotel)
        booking = Booking.objects.create(
            guest_name=validated_data.pop('guest_name'),
            persons=persons,
            booking_start=booking_start,
            booking_end=booking_end,
            room=room,
        )
        print(f'Booking Instance: {booking}')
        return booking
