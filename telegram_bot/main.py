from telebot import TeleBot, types
from json import dumps

from const import TOKEN, REQUEST_INDEX
from hotel_API_requests import ApiData
api = ApiData()
bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}!\n'
                                      f'Welcome in Smart Bookings Bot\n'
                                      f'Here you have opportunity to reserve a hotel for your vacation or a business trip\n'
                                      f'To get information about functionality type "/help"')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, f'Commands:\n'
                                      f'\t /hotels - Get a list of hotels in your chosen city\n'
                                      f'\t /my_bookings - Get a list of your bookings\n'
                                      f'\t /book_a_hotel - Create a reservation')


# ---------------------HOTELS---------------------
# ----------------------GET-----------------------


@bot.message_handler(commands=['hotels'])
def get_hotels(message: types.Message):
    msg = bot.send_message(message.chat.id, 'Type the city you want to visit:')
    bot.register_next_step_handler(msg, hotels_unpacker)


def hotels_unpacker(message):
    try:
        hotels = api.get_hotels(message.text)
        if hotels:
            for hotel in hotels:
                bot.send_message(message.chat.id, hotel)
        else:
            bot.send_message(message.chat.id, 'Data about the hotels in your city are not available ')
    except AttributeError:
        bot.send_message(message.chat.id, "No information about the city")

# --------------------------------------------------
# ---------------------BOOKINGS---------------------
# -----------------------GET------------------------


@bot.message_handler(commands=['my_bookings'])
def get_bookings(message: types.Message):
    msg = bot.send_message(message.chat.id, 'Type the name on which the hotel was booked:')
    bot.register_next_step_handler(msg, bookings_unpacker)


def bookings_unpacker(message: types.Message):
    bookings = api.get_bookings(message.text)
    if not bookings:
        bot.send_message(message.chat.id, "")
    print(bookings)
    for booking in bookings:
        template = f"Name: {booking.get('guest_name')} \n" \
                   f"{booking.get('place')} \n" \
                   f"Arriving_date: {booking.get('booking_start')} \n" \
                   f"Leaving_date: {booking.get('booking_end')} \n" \
                   f"Persons: {booking.get('persons')}"

        print(booking)
        bot.send_message(message.chat.id, template)

# -----------------------POST------------------------
# TODO: To realize POST Request for bookings


@bot.message_handler(commands=['book_a_hotel'])
def book_a_hotel(message):
    req = [{}]
    bot.send_message(message.chat.id, 'Type your name:')

    def get_name(message):
        nonlocal req
        req[REQUEST_INDEX].update({"guest_name": message.text})
        bot.send_message(message.chat.id, 'Type booking start date:')
        bot.register_next_step_handler(message, get_booking_start)

    def get_booking_start(message):
        nonlocal req
        req[REQUEST_INDEX].update({"booking_start": message.text})
        bot.send_message(message.chat.id, 'Type booking end date:')
        bot.register_next_step_handler(message, get_booking_end)

    def get_booking_end(message):
        nonlocal req
        req[REQUEST_INDEX].update({"booking_end": message.text})
        bot.send_message(message.chat.id, 'How many residents are there?')
        bot.register_next_step_handler(message, get_persons)

    def get_persons(message):
        nonlocal req
        req[REQUEST_INDEX].update({"persons": message.text})
        bot.send_message(message.chat.id, 'Type the city you want to visit:')
        bot.register_next_step_handler(message, get_city)

    def get_city(message):
        # TODO: Finish get_city and get_hotels functions
        nonlocal req
        req[REQUEST_INDEX].update({"city": message.text})
        bot.send_message(message.chat.id, 'Choose the hotel')
        bot.register_next_step_handler(message, get_hotel)

    def get_hotel(message):
        nonlocal req
        req[REQUEST_INDEX].update({"hotel": message.text})
        r = api.make_reservation(dumps(req))
        bot.send_message(message.chat.id, r)
    bot.register_next_step_handler(message, get_name)


bot.infinity_polling()
