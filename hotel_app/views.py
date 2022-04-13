from rest_framework.decorators import api_view
from rest_framework.response import Response
from hotel_app.models import (
    Hotel,
    Room,
    City
)

from hotel_app.serializers import HotelSerializer


@api_view(['GET'])
def api_hotels(req):
    if req.method == 'GET':
        hotels = Hotel.objects.all()
        serializer = HotelSerializer(hotels, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def api_booking(req):
    if req.method == "GET":
        print(f'Request data: {req.data}')