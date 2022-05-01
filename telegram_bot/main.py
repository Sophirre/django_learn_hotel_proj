from telebot import TeleBot, types
from json import dumps

from hotel_API_requests import ApiData

from msg_templates import (
    START_MESSAGE_TEXT,
    HELP_MESSAGE_TEXT,
    HOTELS_NOT_FOUND,
    CITY_NOT_FOUND,
    BOOKINGS_NOT_FOUND,
    BOOKINGS_INFO_TEMPLATE,
)
from const import TOKEN, REQUEST_INDEX

api = ApiData()
bot = TeleBot(TOKEN)
req = [{}]


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    bot.send_message(message.chat.id, START_MESSAGE_TEXT.format(message.from_user.first_name))


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, HELP_MESSAGE_TEXT)


@bot.message_handler(commands=['hotels'])
def get_hotels(message: types.Message):
    msg = bot.send_message(message.chat.id, 'Type the city you want to visit:')
    bot.register_next_step_handler(msg, get_hotels_by_city)


def get_hotels_by_city(message):
    try:
        hotels = api.get_hotels(message.text)
        if hotels:
            for hotel in hotels:
                bot.send_message(message.chat.id, hotel)
        else:
            bot.send_message(message.chat.id, HOTELS_NOT_FOUND)
    except AttributeError:
        bot.send_message(message.chat.id, CITY_NOT_FOUND)


@bot.message_handler(commands=['my_bookings'])
def get_bookings(message: types.Message):
    msg = bot.send_message(message.chat.id, 'Type the name on which the hotel was booked:')
    bot.register_next_step_handler(msg, bookings_unpacker)


def bookings_unpacker(message: types.Message):
    bookings = api.get_bookings(message.text)
    if not bookings:
        bot.send_message(message.chat.id, BOOKINGS_NOT_FOUND)
    print(bookings)
    for booking in bookings:
        template = BOOKINGS_INFO_TEMPLATE.format(
                                            booking.get('guest_name'),
                                            booking.get('place'),
                                            booking.get('booking_start'),
                                            booking.get('booking_end'),
                                            booking.get('persons')
                                                                        )

        print(booking)
        bot.send_message(message.chat.id, template)


@bot.message_handler(commands=['book_a_hotel'])
def book_a_hotel_entry(message):
    bot.send_message(message.chat.id, 'Type your name:')
    bot.register_next_step_handler(message, lambda msg: book_hotel_collector(msg, "get_name"))


func_mapper = {
    "get_name": {
        "next_func": "get_booking_start",
        "prev_func": None,
        "dict_key": "guest_name",
        "ok_msg_text": "Type booking start date (YYYY-MM-DD):",
        "err_msg_text": ""
    },
    "get_booking_start": {
        "next_func": "get_booking_end",
        "prev_func": "get_name",
        "dict_key": "booking_start",
        "ok_msg_text": "Type booking end date (YYYY-MM-DD):",
        "err_msg_text": ""
    },
    "get_booking_end": {
        "next_func": "get_persons",
        "prev_func": "get_booking_start",
        "dict_key": "booking_end",
        "ok_msg_text": "How many residents are there?",
        "err_msg_text": ""
    },
    "get_persons": {
        "next_func": "get_city",
        "prev_func": "get_booking_end",
        "dict_key": "persons",
        "ok_msg_text": "Type the city you want to visit:",
        "err_msg_text": ""
    },
    "get_city": {
        "next_func": "get_hotel",
        "prev_func": "get_persons",
        "dict_key": "city",
        "ok_msg_text": "Choose the hotel:",
        "err_msg_text": ""
    },
    "get_hotel": {
        "next_func": None,
        "prev_func": "get_city",
        "dict_key": "hotel",
        "ok_msg_text": "",
        "err_msg_text": ""
    }
}


def book_hotel_collector(message, current_func):
    print(message.text)
    key = func_mapper[current_func]["dict_key"]
    next_func = func_mapper[current_func]["next_func"]
    ok_msg = func_mapper[current_func]["ok_msg_text"]
    prev_func = func_mapper[current_func]['prev_func']

    req[REQUEST_INDEX].update({key: message.text})
    if message.text == "/edit":
        print("Editing")
        bot.register_next_step_handler(
            message,
            lambda msg: book_hotel_collector(msg, prev_func)
        )
        return None
    if next_func:
        bot.send_message(message.chat.id, ok_msg)
        bot.register_next_step_handler(
            message,
            lambda msg: book_hotel_collector(msg, next_func)
        )
    else:
        r = api.make_reservation(dumps(req))
        bot.send_message(message.chat.id, "Success")
        bot.send_message(message.chat.id, f"Your request is {r.text}")
        return r


bot.infinity_polling()
