from const import TOKEN
from telebot import TeleBot, types

from get_data import ApiGet
api = ApiGet()
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
                                      f'\t /book_a_hotel - Create a reservation(Not Working)')


# ---------------------HOTELS---------------------
# ----------------------GET-----------------------


@bot.message_handler(commands=['hotels'])
def get_hotels(message: types.Message):
    msg = bot.send_message(message.chat.id, 'Введите город который вы хотите посетить:')
    bot.register_next_step_handler(msg, hotels_unpacker)


def hotels_unpacker(message):
    try:
        hotels = api.get_hotels(message.text)
        if hotels:
            for hotel in hotels:
                bot.send_message(message.chat.id, hotel)
        else:
            bot.send_message(message.chat.id, 'Нет данных об отелях в этом городе')
    except AttributeError:
        bot.send_message(message.chat.id, 'Такого города нет в базе')

# --------------------------------------------------
# ---------------------BOOKINGS---------------------
# -----------------------GET------------------------


@bot.message_handler(commands=['my_bookings'])
def get_bookings(message: types.Message):
    msg = bot.send_message(message.chat.id, 'Введите имя на которое был забронирован отель:')
    bot.register_next_step_handler(msg, bookings_unpacker)


def bookings_unpacker(message: types.Message):
    bookings = api.get_bookings(message.text)
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
    req = {}
    bot.send_message(message.chat.id, 'Введите ваше имя:')

    def get_name(message):
        nonlocal req
        req.update({"guest_name": message.text})
        bot.send_message(message.chat.id, 'Начало бронирования:')
        bot.register_next_step_handler(message, get_booking_start)

    def get_booking_start(message):
        nonlocal req
        req.update({"booking_start": message.text})
        bot.send_message(message.chat.id, 'Конец бронирования:')
        bot.register_next_step_handler(message, get_booking_end)

    def get_booking_end(message):
        nonlocal req
        req.update({"booking_end": message.text})
        bot.register_next_step_handler(message, get_city)

    def get_city(message):
        # TODO: Finish get_city and get_hotels functions
        nonlocal req
        req.update({"booking_start": message.text})
        get_hotels(message)
        bot.register_next_step_handler(message, get_hotel)

    def get_hotel(message):
        pass

    bot.register_next_step_handler(message, get_name)


bot.infinity_polling()
