from rest_framework.decorators import api_view
from rest_framework.response import Response
from hotel_app.models import (
    Hotel,
    Booking,
)
from rest_framework import status
from hotel_app.serializers import (HotelSerializer, BookingSerializer)


@api_view(['GET'])
def api_hotels(req):
    if req.method == 'GET':
        hotels = Hotel.objects.all()
        serializer = HotelSerializer(hotels, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def api_booking(req):
    if req.method == "GET":
        bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
    elif req.method == "POST":
        serializer = BookingSerializer(data=req.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

