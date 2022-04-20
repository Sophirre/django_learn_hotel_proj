from rest_framework.decorators import api_view
from rest_framework.response import Response
from hotel_app.models import (
    Hotel,
    Booking,
    City,
)
from rest_framework import status
from hotel_app.serializers import (HotelSerializer, BookingSerializer)
from django.core.exceptions import ObjectDoesNotExist


@api_view(['GET'])
def api_hotels(req):
    if req.method == 'GET':
        city = req.query_params.get('city')
        if city:
            try:
                city = City.objects.get(title=city)
                hotels = city.hotels.all()
            except ObjectDoesNotExist as e:
                return Response(f"Error: City: {city} can't be handled")
        else:
            hotels = Hotel.objects.all()
        serializer = HotelSerializer(hotels, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def api_booking(req):
    if req.method == "GET":
        name = req.query_params.get('guest_name')
        if name:
            print(name)
            booking = Booking.objects.filter(guest_name=name)
        else:
            booking = Booking.objects.all()
        serializer = BookingSerializer(booking, many=True)
        print(serializer.data)
        return Response(serializer.data)
    elif req.method == "POST":
        serializer = BookingSerializer(data=req.data, many=True)
        print(f'Before: {serializer}')
        if serializer.is_valid():
            print(f'After: {serializer}')
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

