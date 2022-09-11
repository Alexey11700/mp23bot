import sqlite3
import telebot
from telebot import types

bot = telebot.TeleBot('')
mess_dlina = '<b>Ввведите пожалуйста длину рисунка в сантиметрах: пример "125"</b>'
mess_shirina = '<b>Ввведите пожалуйста ширину рисунка в сантиметрах: \nпример "125"</b>'
messno = '<b>Всего доброго! Если захотите сделать расчет, воспользуйтесь командой /start </b>'


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    bat1 = types.KeyboardButton('Да')
    bat2 = types.KeyboardButton('Нет')
    markup.add(bat1, bat2)
    mess = f'Здравствуйте <b>{message.from_user.first_name} {message.from_user.last_name}!\n</b>Вас приветствует компания <b>MagiсPrint23!</b>\nМы занимаемся интерьерной печатью и нанесением любых рисунков на любые поверхности. \nХотите расчитать стоимость вашего рисунка?'
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def calculation(message):
    if message.text.lower() == "да":
        connect = sqlite3.connect('datab.db')
        cursor = connect.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS area(
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        dlina1 INTEGER,
                        shirina1 INTEGER 
                    )""")
        cursor.execute("DELETE FROM area")
        connect.commit()

        bot.send_message(message.chat.id, mess_dlina, parse_mode='html')
        bot.register_next_step_handler(message, get_length)

    elif message.text.lower() == "нет":
        bot.send_message(message.chat.id, messno, parse_mode='html')

    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммирован..")


def get_length(message):

    try:
        length = message.text
        d1 = []
        d1.append(length)

        if length.isdigit():
            connect = sqlite3.connect('datab.db')
            cursor = connect.cursor()
            cursor.execute("INSERT INTO area(dlina1) VALUES(?);", d1)
            connect.commit()
            bot.send_message(message.chat.id, mess_shirina, parse_mode='html')
            bot.register_next_step_handler(message, get_width)
        else:
            bot.send_message(message.chat.id, 'Цифрами пожалуйста', parse_mode='html')
            bot.register_next_step_handler(message, get_length)
    except Exception:
            bot.reply_to(message, 'Длина должна быть в сантиметрах')
            bot.register_next_step_handler(message, get_length)


def get_width(message,):

    try:
        width = message.text
        d2 = []
        d2.append(width)
        if width.isdigit():
            connect = sqlite3.connect('datab.db')
            cursor = connect.cursor()
            cursor.execute("UPDATE area SET shirina1 = ?", d2)
            cursor.execute("SELECT (((dlina1) * (shirina1))*30)/100 FROM area")
            result = cursor.fetchall()
            rez = ([x[0] for x in result])
            final = (rez[0])
            connect.commit()

            bot.send_message(message.chat.id, 'Ориентировочная цена вашего рисунка составляет: \n' +  str(final)  + ' рублей', parse_mode='html')

            markup = types.InlineKeyboardMarkup(row_width=2)
            bat1 = types.InlineKeyboardButton(text='ЗАЯВКА', url='https://magicprint23.ru/')
            bat2 = types.InlineKeyboardButton(text='РАБОТЫ', url='http://www.instagram.com/magicprint23krd')
            markup.add(bat1, bat2)
            mess = f'Вау, цена очень даже привлекательная, согласны <b>{message.from_user.first_name} {message.from_user.last_name}?\n</b>Если хотите оставить заявку и обсудить детали с менеджером, то жмите "ЗАЯВКА".\nЕсли хотите посмотреть наши работы в instagram, тогда жмите "РАБОТЫ"'
            bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)


        else:
            bot.send_message(message.chat.id, 'Цифрами пожалуйста', parse_mode='html')
            bot.register_next_step_handler(message, get_width)
    except Exception:
            bot.reply_to(message, 'Ширина должна быть в сантиметрах')
            bot.register_next_step_handler(message, get_width)


bot.polling(none_stop=True)