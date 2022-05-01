START_MESSAGE_TEXT = 'Hello, {}!\n' \
       'Welcome in Smart Bookings Bot\n '\
       'Here you have opportunity to reserve a hotel for your vacation or a business trip\n' \
       'To get information about functionality type "/help"'

HELP_MESSAGE_TEXT = 'Commands:\n' \
       '\t /hotels - Get a list of hotels in your chosen city\n' \
       '\t /my_bookings - Get a list of your bookings\n' \
       '\t /book_a_hotel - Create a reservation'


HOTELS_NOT_FOUND = 'Data about the hotels in your city are not available.'

CITY_NOT_FOUND = "No information about the city"

BOOKINGS_NOT_FOUND = "You don't have any bookings yet\n" \
                     "But you can fix it!\n" \
                     "TYPE: /book_a_hotel"
BOOKINGS_INFO_TEMPLATE = "Name: {} \n" \
                   "{} \n" \
                   "Arriving_date: {} \n" \
                   "Leaving_date: {} \n" \
                   "Persons: {}"
