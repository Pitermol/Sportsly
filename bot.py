# coding=utf-8
import telebot
#import sys

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
    return str(rand_string)

#reload(sys)
#sys.setdefaultencoding('utf-8')

telebot.apihelper.proxy = {
    'https':'socks5://7Q6VEgMh:9h9dmuys@5.188.44.15:12993'}

token = "1717637269:AAExsIh3F3zPSEp6wqKHaYpFZSIUddCisro"
bot = telebot.TeleBot(token)
subs_time = 0
MONTH_COST = 499
WEEK_COST = 199
THREE_DAY_COST = 89
QIWI_PHONE = 89163275063
QIWI_NICKNAME = "TAGEP869"
url = "https://qiwi.com/payment/form/99999?extra%5B%27account%27%5D={nickname}&amountInteger={amount_rub}&" \
      "amountFraction={amount_kop}&currency=643&blocked[0]=account&blocked[1]=sum&extra%5B%27accountType%27%5D=nickname"


@bot.message_handler(commands=['start'])
def start_message(message):
    print(message.text)
    reffed_by = "-1"
    if message.text != "/start":
        link = message.text[7:]
        ref_by = 'https://t.me/SportslyBot?start=' + link
        collection = db.collection('users')
        for doc in collection.stream():
            if doc.to_dict()['ref_link'] == ref_by:
                d = doc.to_dict()['ref_owns']
                d.append(str(message.chat.id))
                collection.document(doc.id).update({'ref_owns': d})
                reffed_by = str(doc.id)

    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    doc_ref = db.collection('users').document(str(message.chat.id))
    doc = doc_ref.get()
    if not doc.exists:
        db.collection('users').document(str(message.chat.id)).set({'bets_left': '0', 'isAdmin': False, 'ref_owns': [],
                                                                   'reffed_by': reffed_by, 'bought_KHL': [], 'subscription_time': '0',
                                                                   'ref_link': 'https://t.me/SportslyBot?start='
                                                                               + ref_link(16)})
        keyboard.row('Прогнозы', 'Профиль')
    else:
        doc = doc.to_dict()
        if doc['isAdmin']:
            keyboard.row('Прогнозы', 'Профиль', 'Функции админа')
        else:
            keyboard.row('Прогнозы', 'Профиль')
    keyboard.row('FAQ', 'Поддержка', 'Реф. система')
    bot.send_message(message.chat.id, 'Greetings', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def react_to_start_commands(message):
    doc_ref = db.collection('users').document(str(message.chat.id))
    doc = doc_ref.get()
    #######  ЗДЕСЬ НАЧИНАЮТСЯ ГЛОБАЛЬНЫЕ КОМАНДЫ #######
    if message.text == 'Вернуться в начало' or message.text == 'Готово':
        doc = doc.to_dict()
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        if doc['isAdmin']:
            keyboard.row('Прогнозы', 'Профиль', 'Функции админа')
        else:
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
            profile_info = 'Осталось часов подписки:  ' + str(hours_left) + '\n' + 'Осталось прогнозов:  ' + str(
                bets_left)
            bot.send_message(message.chat.id, profile_info, reply_markup=keyboard)

    if message.text == 'Купить подписку' or message.text == 'Купить' or message.text == 'Выбрать другое время':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('На месяц', 'На неделю', 'На 3 дня')
        keyboard.row('Что дает подписка', 'Вернуться в начало')
        bot.send_message(message.chat.id, 'Выбери пункт меню', reply_markup=keyboard)
    if message.text == 'На месяц':
        keyboard1 = telebot.types.InlineKeyboardMarkup()
        url_button = telebot.types.InlineKeyboardButton(text="Перейти к оплате",
                                                        url=url.format(nickname=QIWI_NICKNAME,
                                                                       amount_rub=str(MONTH_COST), amount_kop='99'))
        keyboard1.add(url_button)
        bot.send_message(message.chat.id, 'ВНИМАНИЕ❗'
                         ' Не забудьте указать комментарий к платежу: ' + str(message.chat.id) +
                         '\nОбработка платежа может занять до 5 часов',
                         reply_markup=keyboard1)
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        doc = doc.to_dict()
        if doc['isAdmin']:
            keyboard.row('Прогнозы', 'Профиль', 'Функции админа')
        else:
            keyboard.row('Прогнозы', 'Профиль')
        keyboard.row('FAQ', 'Поддержка', 'Реф. система')
        bot.send_message(message.chat.id, 'Greetings', reply_markup=keyboard)

    if message.text == 'На неделю':
        keyboard1 = telebot.types.InlineKeyboardMarkup()
        url_button = telebot.types.InlineKeyboardButton(text="Перейти к оплате", url=url.format(nickname=QIWI_NICKNAME,
                                                                                                amount_rub=str(
                                                                                                    WEEK_COST),
                                                                                                amount_kop='99'))
        keyboard1.add(url_button)
        bot.send_message(message.chat.id, 'ВНИМАНИЕ❗'
                                          ' Не забудьте указать комментарий к платежу: ' + str(message.chat.id) +
                         '\nОбработка платежа может занять до 5 часов',
                         reply_markup=keyboard1)
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        doc = doc.to_dict()
        if doc['isAdmin']:
            keyboard.row('Прогнозы', 'Профиль', 'Функции админа')
        else:
            keyboard.row('Прогнозы', 'Профиль')
        keyboard.row('FAQ', 'Поддержка', 'Реф. система')
        bot.send_message(message.chat.id, 'Greetings', reply_markup=keyboard)
    if message.text == 'На 3 дня':
        keyboard1 = telebot.types.InlineKeyboardMarkup()
        url_button = telebot.types.InlineKeyboardButton(text="Перейти к оплате", url=url.format(nickname=QIWI_NICKNAME,
                                                                                                amount_rub=str(
                                                                                                    THREE_DAY_COST),
                                                                                                amount_kop='99'))
        keyboard1.add(url_button)
        bot.send_message(message.chat.id, 'ВНИМАНИЕ❗'
                                          ' Не забудьте указать комментарий к платежу: ' + str(message.chat.id) +
                         '\nОбработка платежа может занять до 5 часов',
                         reply_markup=keyboard1)
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        doc = doc.to_dict()
        if doc['isAdmin']:
            keyboard.row('Прогнозы', 'Профиль', 'Функции админа')
        else:
            keyboard.row('Прогнозы', 'Профиль')
        keyboard.row('FAQ', 'Поддержка', 'Реф. система')
        bot.send_message(message.chat.id, 'Greetings', reply_markup=keyboard)
    if message.text == 'Что дает подписка':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Купить', 'Вернуться в начало')
        bot.send_message(message.chat.id, 'Подписка дает вам право сосать хуй', reply_markup=keyboard)
    ###### ЗДЕСЬ ЗАКАНЧИВАЕТСЯ ПРОФИЛЬ ######



    ###### ЗДЕСЬ НАЧИНАЕТСЯ РЕФЕРАЛЬНАЯ СИСТЕМА ######
    if message.text == 'Реф. система':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Мои рефералы', 'Реф.ссылка', 'Вернуться в начало')
        bot.send_message(message.chat.id, 'Выберите пункт меню', reply_markup=keyboard)
    if message.text == 'Реф.ссылка':
        doc = doc.to_dict()
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Реф. система', 'Вернуться в начало')
        bot.send_message(message.chat.id, doc['ref_link'], reply_markup=keyboard)
    if message.text == 'Мои рефералы':
        doc = doc.to_dict()
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Реф. система', 'Вернуться в начало')
        bot.send_message(message.chat.id, 'Ваши рефералы:\n     ' + "\n     ".join(doc['ref_owns']), reply_markup=keyboard)
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
        bot.send_message(message.chat.id, 'Пока что не работает')
        #keyboard = telebot.types.ReplyKeyboardMarkup(True)
        #keyboard.row('Прогнозы', 'Вернуться в начало')
        #bot.send_message(message.chat.id, 'Тут прогноз для НХЛ', reply_markup=keyboard)
    if message.text == 'КХЛ':
        matches = list(db.collection('bets').document("KHL").get().to_dict().keys())
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        for match in matches:
            keyboard.row(" | ".join(match.split(",")))
        keyboard.row('Прогнозы', 'Вернуться в начало')
        bot.send_message(message.chat.id, 'Доступные матчи:', reply_markup=keyboard)

    if message.text == 'Случайная ставка':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Прогнозы', 'Вернуться в начало')
        bot.send_message(message.chat.id, 'Тут случайный прогноз', reply_markup=keyboard)

        ####### ЗДЕСЬ ЗАКАНЧИВАЮТСЯ ПРОГНОЗЫ ########

    ###### ЗДЕСЬ НАЧИНАЕТСЯ АДМИН ПАНЕЛЬ  #############
    if message.text == 'Функции админа':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Добавить матч', 'Удалить матч')
        keyboard.row('Начислить подписку', 'Вернуться в начало')
        bot.send_message(message.chat.id, 'Админ панель для хуесосов кстати егор пидор', reply_markup=keyboard)
    if message.text == 'Начислить подписку':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Готово')
        msg = bot.send_message(message.chat.id, 'Введите в виде: ID количество_часов', reply_markup=keyboard)
        bot.register_next_step_handler(msg, ask_subscription)
    if message.text == 'Добавить матч':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Готово')
        msg = bot.send_message(message.chat.id,
                         'Введите в виде: Команда1 Команда2 Последние_5_игр_Команды1'
                         ' Положение_таблицы_Команды1 Индекс_Силы_Команды1 Последние_5_игр_Команды2'
                         ' Положение_таблицы_Команды2 Индекс_Силы_Команды2',
                         reply_markup=keyboard)
        bot.register_next_step_handler(msg, add_match)
    if message.text == 'Удалить матч':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Готово')
        msg = bot.send_message(message.chat.id,
                         'Введите в виде: Команда1 Команда2 Последние_5_игр_Команды1'
                         ' Положение_таблицы_Команды1 Индекс_Силы_Команды1 Последние_5_игр_Команды2'
                         ' Положение_таблицы_Команды2 Индекс_Силы_Команды2',
                         reply_markup=keyboard)
        bot.register_next_step_handler(msg, del_match)

    if ",".join(message.text.split(" | ")) in list(db.collection('bets').document("KHL").get().to_dict().keys()):
        user = db.collection('users').document(str(message.chat.id)).get().to_dict()
        users_bets = user['bought_KHL']
        if message.text in users_bets:
            print("PROGNOZ")
        else:
            bets_left = user["bets_left"]
            if bets_left:
                keyboard = telebot.types.ReplyKeyboardMarkup(True)
                keyboard.row('Получить прогноз на матч ' + message.text)
                bot.send_message(message.chat.id,
                                 "У вас нет этого прогноза, но вы можете его получить\nОсталось прогнозов: "
                                 + str(bets_left), reply_markup=keyboard)
            else:
                keyboard = telebot.types.ReplyKeyboardMarkup(True)
                keyboard.row('Купить больше прогнозов')
                bot.send_message(message.chat.id,
                                 "У вас нет этого прогноза, чтобы его получить, купите прогнозы", reply_markup=keyboard)

    if message.text.startswith("Получить прогноз на матч"):
        user = db.collection('users').document(str(message.chat.id)).get().to_dict()


def ask_subscription(message):
    chat_id = message.chat.id
    text = message.text.split()
    try:
        user_id = text[0]
        amount = int(text[1])
        doc_ref = db.collection('users')
        amount = amount + int(doc_ref.document(user_id).get().to_dict()['subscription_time'])
        doc_ref.document(user_id).set({'subscription_time' : str(amount)})
        ref = doc_ref.document(user_id).get().to_dict()['reffed_by']
        if ref != "-1":
            pass # ТУТ ЧТО ТО ДЕЛАЕТСЯ ЧЕЛОВЕКУ С ID "ref"
        bot.send_message(chat_id, "Начислено успешно")
    except:
        bot.send_message(chat_id, "Неправильный ввод")
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Начислить подписку', 'Добавить матч')
        bot.send_message(message.chat.id, 'Админ панель для хуесосов кстати егор пидор', reply_markup=keyboard)

def add_match(message):
    chat_id = message.chat.id
    text = message.text.split()
    try:
        doc_ref = db.collection('bets').document('KHL')
        doc_ref.set({text[0] + ',' + text[1]: [text[2] + ',' + text[3] + ',' + text[4], text[5] + ',' + text[6] + ',' + text[7]]}, merge=True)
        bot.send_message(chat_id, "Добавлено успешно")
    except:
        bot.send_message(chat_id, "Неправильный ввод")
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Начислить подписку', 'Добавить матч')
        bot.send_message(message.chat.id, 'Админ панель для хуесосов кстати егор пидор', reply_markup=keyboard)

def del_match(message):
    chat_id = message.chat.id
    text = message.text.split()
    try:
        doc_ref = db.collection('bets').document('KHL')
        doc_ref.set({text[0] + ',' + text[1]: [text[2] + ',' + text[3] + ',' + text[4], text[5] + ',' + text[6] + ',' + text[7]]}, merge=True)
        bot.send_message(chat_id, "Добавлено успешно")
    except:
        bot.send_message(chat_id, "Неправильный ввод")
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Начислить подписку', 'Добавить матч')
        bot.send_message(message.chat.id, 'Админ панель для хуесосов кстати егор пидор', reply_markup=keyboard)


bot.polling(none_stop=False, interval=0)
