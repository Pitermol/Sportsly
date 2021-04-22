import telebot

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("firebase-sdk.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
import random
import string


def ref_link(length):
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = ''.join(random.sample(letters_and_digits, length))
    return (rand_string)

telebot.apihelper.proxy = {
    'https':'socks5://7Q6VEgMh:9h9dmuys@5.188.44.15:12993'}

token = "1717637269:AAExsIh3F3zPSEp6wqKHaYpFZSIUddCisro"
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    print(message.text[7:])
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    doc_ref = db.collection('users').document(str(message.chat.id))
    doc = doc_ref.get()
    doc = doc.to_dict()
    if doc['isAdmin']:
        keyboard.row('Прогнозы', 'Профиль', 'Функции админа')
    else:
        keyboard.row('Прогнозы', 'Профиль')
    keyboard.row('FAQ', 'Поддержка', 'Реф. система')
    bot.send_message(message.chat.id, 'Greetings', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def react_to_start_commands(message):
    #######  ЗДЕСЬ НАЧИНАЮТСЯ ГЛОБАЛЬНЫЕ КОМАНДЫ #######
    if message.text == 'Вернуться в начало':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Прогнозы', 'Профиль')
        keyboard.row('FAQ', 'Поддержка', 'Реф. система')
        bot.send_message(message.chat.id, 'Greetings', reply_markup=keyboard)

    ######## ЗДЕСЬ ЗАКАНЧИВАЮТСЯ ГЛОБАЛЬНЫЕ КОМАНДЫ

    ####### ЗДЕСЬ НАЧИНАЕТСЯ ПРОФИЛЬ #######
    if message.text == "Профиль":
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Купить подписку', 'Вернуться в начало')
        doc_ref = db.collection('users').document(str(message.chat.id))
        doc = doc_ref.get()
        if doc.exists:
            doc = doc.to_dict()
            bets_left = doc['bets_left']
            hours_left = doc['subscription_time']
            profile_info = 'Осталось часов подписки:  ' + str(hours_left) + '\n' + 'Осталось прогнозов:  ' + str(bets_left)
            bot.send_message(message.chat.id, profile_info, reply_markup=keyboard)


    if message.text == 'Купить подписку' or message.text == 'Купить' or message.text == 'Выбрать другое время':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('На месяц', 'На неделю', 'На 3 дня')
        keyboard.row('Что дает подписка', 'Вернуться в начало')
        bot.send_message(message.chat.id, 'Выбери пункт меню', reply_markup=keyboard)
    if message.text == 'На месяц':
        # тут будет ссылка на оплату на месяц
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Выбрать другое время', 'Вернуться в начало')
        bot.send_message(message.chat.id, 'Для покупки подписки вам необходимо пройти по ссылке:',
                         reply_markup=keyboard)
    if message.text == 'На неделю':
        # тут будет ссылка на оплату на неделю
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Выбрать другое время', 'Вернуться в начало')
        bot.send_message(message.chat.id, 'Для покупки подписки вам необходимо пройти по ссылке:',
                         reply_markup=keyboard)
    if message.text == 'На 3 дня':
        # тут будет ссылка на оплату на 3 дня
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Выбрать другое время', 'Вернуться в начало')
        bot.send_message(message.chat.id, 'Для покупки подписки вам необходимо пройти по ссылке:',
                         reply_markup=keyboard)
    if message.text == 'Что дает подписка':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Купить', 'Вернуться в начало')
        bot.send_message(message.chat.id, 'Подписка дает вам право сосать хуй', reply_markup=keyboard)
    ###### ЗДЕСЬ ЗАКАНЧИВАЕТСЯ ПРОФИЛЬ ######



    ###### ЗДЕСЬ НАЧИНАЕТСЯ РЕФЕРАЛЬНАЯ СИСТЕМА ######
    if message.text == 'Реф. система':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Мои рефералы', 'Реф.ссылка')
        bot.send_message(message.chat.id, 'Выберите пункт меню', reply_markup=keyboard)
    if message.text == 'Реф.ссылка':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Реф. система', 'Вернуться в начало')
        bot.send_message(message.chat.id, 'Ваша реферальная ссылка - ссылка из базы данных', reply_markup=keyboard)
    if message.text == 'Мои рефералы':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Реф. система', 'Вернуться в начало')
        bot.send_message(message.chat.id, 'Ваши рефералы', reply_markup=keyboard)
    ###### ЗДЕСЬ ЗАКАНЧИВАЕТСЯ РЕФЕРАЛЬНАЯ СИСТЕМА ######


    ##### ЗДЕСЬ НАЧИНАЕТСЯ ПОДДЕРЖКА #########
    if message.text == 'Поддержка':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Вернуться в начало')
        bot.send_message(message.chat.id, 'Чтобы задать вопрос, заполните форму', reply_markup=keyboard)
    ####### ЗДЕСЬ ЗАКАНЧИВАЕТСЯ ПОДДЕРЖКА #########



    ####### ЗДЕСЬ НАЧИНАЕТСЯ FAQ ########
    if message.text == 'FAQ':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Ответы на часто задаваемые вопросы', 'Правила')
        keyboard.row('Информация о боте', 'Вернуться в начало')
        bot.send_message(message.chat.id, 'Выберите пункт меню', reply_markup=keyboard)
    if message.text == 'Ответы на часто задаваемые вопросы':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('FAQ', 'Вернуться в начало')
        bot.send_message(message.chat.id, 'Тут ответы на часто задаваемые', reply_markup=keyboard)
    if message.text == 'Правила':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('FAQ', 'Вернуться в начало')
        bot.send_message(message.chat.id, 'Тут правила', reply_markup=keyboard)
    if message.text == 'Информация о боте':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('FAQ', 'Вернуться в начало')
        bot.send_message(message.chat.id, 'Тут информация о боте', reply_markup=keyboard)
    ####### ЗДЕСЬ ЗАКАНЧИВАЕТСЯ FAQ #########



    ####### ЗДЕСЬ НАЧИНАЮТСЯ ПРОГНОЗЫ ########
    if message.text == 'Прогнозы':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('НХЛ', 'КХЛ')
        keyboard.row('Случайная ставка', 'Вернуться в начало')
        bot.send_message(message.chat.id, 'Выберите пункт меню', reply_markup=keyboard)
    if message.text == 'НХЛ':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Прогнозы', 'Вернуться в начало')
        bot.send_message(message.chat.id, 'Тут прогноз для НХЛ', reply_markup=keyboard)
    if message.text == 'КХЛ':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Прогнозы', 'Вернуться в начало')
        bot.send_message(message.chat.id, 'Тут прогноз для КХЛ', reply_markup=keyboard)
    if message.text == 'Случайная ставка':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Прогнозы', 'Вернуться в начало')
        bot.send_message(message.chat.id, 'Тут случайный прогноз', reply_markup=keyboard)

        ####### ЗДЕСЬ ЗАКАНЧИВАЮТСЯ ПРОГНОЗЫ ########


bot.polling(none_stop=True, interval=0)