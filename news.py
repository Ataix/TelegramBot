import telebot
import csv
import pars_news
from telebot import types
from datetime import date

pars_news.main()

bot = telebot.TeleBot("1496404659:AAGeyg6FtcTKoTIq3dURIVnovmGLNKA9p6A")

addi_keyboard = types.InlineKeyboardMarkup(row_width=2)
d_btn = types.InlineKeyboardButton('Полная новость', callback_data='description')
i_btn = types.InlineKeyboardButton('Фотография', callback_data='img')
addi_keyboard.add(d_btn, i_btn)

exit_keyboard = types.InlineKeyboardMarkup(row_width=1)
exit_btn = types.InlineKeyboardButton('Выход', callback_data='exit')
exit_keyboard.add(exit_btn)

@bot.message_handler(commands=['start'])
def start_message(message):
    """Извлекаем из файла заголовки новостей.Отправляем пользователю"""
    global output_title
    output_title = []
    chat_id = message.chat.id
    today_news = str(date.today()).split('-')  
    bot.send_message(chat_id, f'Текущие новости. {today_news[0]}.{today_news[1]}.{today_news[2]}')

    with open('news.csv', 'r') as news_file:
        news_reader = csv.reader(news_file, delimiter=',')
        count = 0
        for row in news_reader:
            output_title.append(str(count + 1)+ ' | ' + row[0] + '\n\n')
            count += 1
        """Запрашиваем номер заголовка"""
        bot.send_message(chat_id, ' '.join(output_title[:20]))
        msg = bot.send_message(chat_id, 'Укажите номер новости для показа полного текста и фото')
        bot.register_next_step_handler(msg, get_news_id)


def get_news_id(message):
    """Получаем номер заголовка.Запрашиваем дальнейщее действие"""
    global news_id
    news_id = message.text
    bot.send_message(message.chat.id, output_title[int(message.text) - 1])
    bot.send_message(message.chat.id, 'Полный текст или фото?', reply_markup=addi_keyboard)
    
@bot.callback_query_handler(func=lambda x:True)
def callback(x):
    """Отправка описания или фотографии по номеру заголовка"""
    chat_id = x.message.chat.id
    output_de = []
    output_img = []
    if x.data == 'description':
        with open('news.csv', 'r') as news_file:
            news_reader = csv.reader(news_file, delimiter=',')
            for row in news_reader:
                output_de.append('\t' + row[2] + '\n\n')
        bot.send_message(chat_id, output_de[int(news_id) - 1], reply_markup=exit_keyboard)
    elif x.data == 'img':
        with open('news.csv', 'r') as news_file:
            news_reader = csv.reader(news_file, delimiter=',')
            for row in news_reader:
                output_img.append(row[1])
        try: 
            bot.send_photo(chat_id, output_img[int(news_id) - 1], reply_markup=exit_keyboard)
        except:
            bot.send_message(chat_id, 'Фото нет', reply_markup=exit_keyboard)
    elif x.data == 'exit':
        bot.send_message(chat_id, 'До свидания')

bot.polling()