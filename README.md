# django_learn_hotel_proj

## Hotels
### GET
http://127.0.0.1:8000/hotels/api/hotels/ or
http://127.0.0.1:8000/hotels/api/hotels/?city=<CityName>

## Bookings
### GET
http://127.0.0.1:8000/hotels/api/bookings/ or
http://127.0.0.1:8000/hotels/api/bookings/?guest_name=<Name>
### POST
[
    {
        "guest_name": str,
        "booking_start":,
        "booking_end":,
        "city": str,
        "hotel": HotelName,
        "persons": int(1-4)
    }
]

# BOT

@smart_booking_bot