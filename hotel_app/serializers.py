from rest_framework import serializers

from hotel_app.models import (
    Hotel,
    Booking
)

from hotel_app.utils.common import find_room


class HotelSerializer(serializers.ModelSerializer):
    rooms_bed = serializers.ReadOnlyField(source='get_rooms_beds')
    city = serializers.CharField(source="city.title")

    class Meta:
        model = Hotel
        fields = ('title', 'city', 'rooms_bed')


class BookingSerializer(serializers.ModelSerializer):
    city = serializers.CharField(read_only=True)
    hotel = serializers.CharField(read_only=True)

    class Meta:
        model = Booking
        fields = (
            'guest_name',
            'booking_start',
            'booking_end',
            'city',
            'hotel',
            'persons',
        )

    def to_internal_value(self, data):
        print(f'Raw Booking data: {data}')
        internal_data = super(BookingSerializer, self).to_internal_value(data)
        print('Internal Booking Data')

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
            room=room
        )
        print(f'Booking Instance: {booking}')
        return booking