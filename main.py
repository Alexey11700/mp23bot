import telebot
from telebot import types

bot = telebot.TeleBot('5367324988:AAH-vbdXLimLjzt2r_QGpKTrpjr6AHhfZiA')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    calculation = types.KeyboardButton('Да')
    markup.add(calculation)
    mess = f'Здравствуйте <b>{message.from_user.first_name} {message.from_user.last_name}!\n</b>Вас приветствует компания <b>MagiсPrint23!</b>\nМы занимаемся интерьерной печатью и нанесением любых рисунков на любые поверхности. \nХотите расчитать стоимость вашего рисунка?'
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)

@bot.message_handler(commands=['calculation'])
def calculation(message):
    dlina = '<b>Ввведите ширину рисунка</b>'
    bot.send_message(message.chat.id, dlina, parse_mode='html')





bot.polling(none_stop=True)