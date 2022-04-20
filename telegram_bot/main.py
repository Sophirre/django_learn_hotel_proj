from const import TOKEN
from telebot import TeleBot, types

from get_data import ApiGet
api = ApiGet()
bot = TeleBot(TOKEN)

class Booking:
    req = {}
    def book_a_hotel(self, message):
        pass

    def get_bookings(self, message: types.Message):
        msg = bot.send_message(message.chat.id, 'Введите имя на которое был забронирован отель:')
        bot.register_next_step_handler(msg, self.bookings_unpacker)

    def bookings_unpacker(self, message: types.Message):

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

booking = Booking()

@bot.message_handler(commands=['book_a_hotel'])
def book_a_hotel(message):
    return booking.book_a_hotel(message)

@bot.message_handler(commands=['my_bookings'])
