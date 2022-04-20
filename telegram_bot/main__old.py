from const import TOKEN
from telebot import TeleBot, types

from get_data import ApiGet
api = ApiGet()
bot = TeleBot(TOKEN)


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
    except AttributeError as e:
        bot.send_message(message.chat.id, 'Такого города нет в базе')


@bot.message_handler(commands=['book_a_hotel'])
def book_a_hotel(message):
    req = {}
    bot.send_message(message.chat.id, 'Введите ваше имя:')
    bot.register_next_step_handler(message, )


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


bot.infinity_polling()
