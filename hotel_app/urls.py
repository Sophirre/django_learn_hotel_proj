from django.urls import path

from hotel_app.views import (
    api_hotels,
    api_booking
)

# TODO: Create path for show all hotels endpoint
urlpatterns = [
    path('hotels/', api_hotels),
    path('bookings/', api_booking)
]
