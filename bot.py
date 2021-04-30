# coding=utf-8
import telebot
import numpy
# from test_file import go
# import sys

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


# reload(sys)
# sys.setdefaultencoding('utf-8')

telebot.apihelper.proxy = {
    'https': 'socks5://7Q6VEgMh:9h9dmuys@5.188.44.15:12993'}

token = "1717637269:AAExsIh3F3zPSEp6wqKHaYpFZSIUddCisro"
bot = telebot.TeleBot(token)
subs_time = 0
MONTH_COST = 499
WEEK_COST = 199
THREE_DAY_COST = 89
ONE_BET_COST = 25
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
                                                                   'reffed_by': reffed_by, 'bought_KHL': [],
                                                                   'subscription_time': '0',
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
    if message.text == 'Вернуться в начало':
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
        keyboard.row('Купить подписку', 'Купить прогнозы' 'Вернуться в начало')
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
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        doc = db.collection('users').document(str(message.chat.id)).get().to_dict()
        if doc['isAdmin']:
            keyboard.row('Прогнозы', 'Профиль', 'Функции админа')
        else:
            keyboard.row('Прогнозы', 'Профиль')
        keyboard.row('FAQ', 'Поддержка', 'Реф. система')
        bot.send_message(message.chat.id, str(message.chat.id), reply_markup=keyboard1)
        bot.send_message(message.chat.id, 'ВНИМАНИЕ❗'
                                          ' Не забудьте указать комментарий к платежу, он в предыдущем сообщении'
                                          '\nОбработка платежа может занять до 5 часов', reply_markup=keyboard)

    if message.text == 'На неделю':
        keyboard1 = telebot.types.InlineKeyboardMarkup()
        url_button = telebot.types.InlineKeyboardButton(text="Перейти к оплате", url=url.format(nickname=QIWI_NICKNAME,
                                                                                                amount_rub=str(
                                                                                                    WEEK_COST),
                                                                                                amount_kop='99'))
        keyboard1.add(url_button)
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        doc = db.collection('users').document(str(message.chat.id)).get().to_dict()
        if doc['isAdmin']:
            keyboard.row('Прогнозы', 'Профиль', 'Функции админа')
        else:
            keyboard.row('Прогнозы', 'Профиль')
        keyboard.row('FAQ', 'Поддержка', 'Реф. система')
        bot.send_message(message.chat.id, str(message.chat.id), reply_markup=keyboard1)
        bot.send_message(message.chat.id, 'ВНИМАНИЕ❗'
                                          ' Не забудьте указать комментарий к платежу, он в предыдущем сообщении'
                                          '\nОбработка платежа может занять до 5 часов', reply_markup=keyboard)
    if message.text == 'На 3 дня':
        keyboard1 = telebot.types.InlineKeyboardMarkup()
        url_button = telebot.types.InlineKeyboardButton(text="Перейти к оплате", url=url.format(nickname=QIWI_NICKNAME,
                                                                                                amount_rub=str(
                                                                                                    THREE_DAY_COST),
                                                                                                amount_kop='99'))
        keyboard1.add(url_button)
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        doc = db.collection('users').document(str(message.chat.id)).get().to_dict()
        if doc['isAdmin']:
            keyboard.row('Прогнозы', 'Профиль', 'Функции админа')
        else:
            keyboard.row('Прогнозы', 'Профиль')
        keyboard.row('FAQ', 'Поддержка', 'Реф. система')
        bot.send_message(message.chat.id, str(message.chat.id), reply_markup=keyboard1)
        bot.send_message(message.chat.id, 'ВНИМАНИЕ❗'
                                          ' Не забудьте указать комментарий к платежу, он в предыдущем сообщении'
                                          '\nОбработка платежа может занять до 5 часов', reply_markup=keyboard)
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
        bot.send_message(message.chat.id, 'Ваши рефералы:\n     ' + "\n     ".join(doc['ref_owns']),
                         reply_markup=keyboard)
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
        # keyboard = telebot.types.ReplyKeyboardMarkup(True)
        # keyboard.row('Прогнозы', 'Вернуться в начало')
        # bot.send_message(message.chat.id, 'Тут прогноз для НХЛ', reply_markup=keyboard)
    if message.text == 'КХЛ':
        matches = list(db.collection('bets').document("KHL").get().to_dict().keys())
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        for match in matches:
            keyboard.row(" | ".join(match.split(",")))
        keyboard.row('Прогнозы', 'Вернуться в начало')
        bot.send_message(message.chat.id, 'Доступные матчи:', reply_markup=keyboard)

    if message.text == 'Случайная ставка':
        user = db.collection('users').document(str(message.chat.id)).get().to_dict()
        if user['bets_left'] > 0:
            bets_left = int(db.collection('users').document(str(message.chat.id)).get().to_dict()['bets_left'])
            db.collection('users').document(str(message.chat.id)).update({'bets_left': bets_left - 1})
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row('Прогнозы', 'Вернуться в начало')
            matches = list(db.collection('bets').document("KHL").get().to_dict().keys())
            bought = user['bought_KHL']
            free_matches = []
            for match in matches:
                if match not in bought:
                    free_matches.append(match)
            if len(free_matches) > 0:
                chosen_match = random.choice(free_matches)
                bought.append(chosen_match)
                db.collection('users').document(str(message.chat.id)).update({'bought_KHL': bought})
                bets_left = int(db.collection('users').document(str(message.chat.id)).get().to_dict()['bets_left'])
                db.collection('users').document(str(message.chat.id)).update({'bets_left': bets_left - 1})
                bot.send_message(message.chat.id,
                                 "Поздравляем! Получен прогноз на матч " + " | ".join(chosen_match.split(",")),
                                 reply_markup=keyboard)
            else:
                bot.send_message(message.chat.id, "У вас уже есть все матчи, попробуйте позже", reply_markup=keyboard)
        else:
            keyboard = telebot.types.ReplyKeyboardMarkup(True, one_time_keyboard=True)
            keyboard.row('Купить больше прогнозов')
            bot.send_message(message.chat.id,
                             "У вас не осталось прогнозов, купите их прямо сейчас", reply_markup=keyboard)

            ####### ЗДЕСЬ ЗАКАНЧИВАЮТСЯ ПРОГНОЗЫ ########

    ###### ЗДЕСЬ НАЧИНАЕТСЯ АДМИН ПАНЕЛЬ  #############
    if message.text == 'Функции админа':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Добавить матч', 'Удалить матч')
        keyboard.row('Начислить подписку', 'Начислить прогнозы', 'Вернуться в начало')
        bot.send_message(message.chat.id, 'Админ панель для хуесосов кстати егор пидор', reply_markup=keyboard)
    if message.text == 'Начислить прогнозы':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Вернуться в начало')
        msg = bot.send_message(message.chat.id, 'Введите в виде: ID количество_прогнозов', reply_markup=keyboard)
        bot.register_next_step_handler(msg, ask_bets)
    if message.text == 'Начислить подписку':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Вернуться в начало')
        msg = bot.send_message(message.chat.id, 'Введите в виде: ID количество_часов', reply_markup=keyboard)
        bot.register_next_step_handler(msg, ask_subscription)
    if message.text == 'Добавить матч':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Вернуться в начало')
        msg = bot.send_message(message.chat.id,
                               'Введите в виде: Команда1 Команда2 Последние_5_игр_Команды1'
                               ' Положение_таблицы_Команды1 Индекс_Силы_Команды1 Последние_5_игр_Команды2'
                               ' Положение_таблицы_Команды2 Индекс_Силы_Команды2',
                               reply_markup=keyboard)
        bot.register_next_step_handler(msg, add_match)
    if message.text == 'Удалить матч':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Вернуться в начало')
        msg = bot.send_message(message.chat.id,
                               'Введите в виде: Команда1 Команда2',
                               reply_markup=keyboard)
        bot.register_next_step_handler(msg, del_match)

    if ",".join(message.text.split(" | ")) in list(db.collection('bets').document("KHL").get().to_dict().keys()):
        match = ",".join(message.text.split(" | "))
        user = db.collection('users').document(str(message.chat.id)).get().to_dict()
        users_bets = user['bought_KHL']
        print(match)
        if match in users_bets:
            params = db.collection('bets').document("KHL").get().to_dict()[match]
            params1 = list(map(float, params[0].split(",")))
            params2 = list(map(float, params[1].split(",")))
            params = []
            for i in range(len(params1)):
                params.append(params1[i] - params2[i])
            print(params)
            with open("weights", "r") as file:
                weights = list(map(float, file.read().split("\n")))
            file.close()
            bet = sigmoid(numpy.dot(params, weights))
            if bet < 0.25:
                bet = ["П1", str((bet * 100).round())]
            elif 0.25 <= bet <= 0.75:
                if 0.45 <= bet <= 0.55:
                    bet = ["X", str((bet * 100).round())]
                else:
                    if bet < 0.5:
                        bet = ["X1", str((bet * 100).round())]
                    else:
                        bet = ["X2", str((bet * 100).round())]
            else:
                bet = ["П2", str((bet * 100).round())]
            bot.send_message(message.chat.id, bet[0] + ", Вероятность победы второго ≈ " + bet[1][:-2] + "%")
        else:
            bets_left = user["bets_left"]
            if int(bets_left):
                keyboard = telebot.types.ReplyKeyboardMarkup(True)
                keyboard.row('Получить прогноз на матч ' + message.text)
                bot.send_message(message.chat.id,
                                 "У вас нет этого прогноза, но вы можете его получить\nОсталось прогнозов: "
                                 + str(bets_left), reply_markup=keyboard)
            else:
                keyboard = telebot.types.ReplyKeyboardMarkup(True, one_time_keyboard=True)
                keyboard.row('Купить больше прогнозов')
                bot.send_message(message.chat.id,
                                 "У вас нет этого прогноза, чтобы его получить, купите прогнозы", reply_markup=keyboard)


    if message.text.startswith("Получить прогноз на матч"):
        if ",".join(message.text[25:].split(" | ")) not in \
                db.collection('users').document(str(message.chat.id)).get().to_dict()['bought_KHL']:
            bets_left = int(db.collection('users').document(str(message.chat.id)).get().to_dict()['bets_left'])
            db.collection('users').document(str(message.chat.id)).update({'bets_left': bets_left - 1})
            bought = db.collection('users').document(str(message.chat.id)).get().to_dict()['bought_KHL']
            bought.append(",".join(message.text[25:].split(" | ")))
            db.collection('users').document(str(message.chat.id)).update({'bought_KHL': bought})
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        doc = db.collection('users').document(str(message.chat.id)).get().to_dict()
        if doc['isAdmin']:
            keyboard.row('Прогнозы', 'Профиль', 'Функции админа')
        else:
            keyboard.row('Прогнозы', 'Профиль')
        keyboard.row('FAQ', 'Поддержка', 'Реф. система')
        bot.send_message(message.chat.id, "Поздравляем! Прогноз получен", reply_markup=keyboard)

    if message.text == "Купить больше прогнозов" or message.text == 'Купить прогнозы':
        msg = bot.send_message(message.chat.id, "Сколько вы хотите купить?")
        bot.register_next_step_handler(msg, ask_how_many_buy)


def ask_bets(message):
    chat_id = message.chat.id
    text = message.text.split()
    try:
        user_id = text[0]
        amount = int(text[1])
        doc_ref = db.collection('users')
        amount = amount + int(doc_ref.document(user_id).get().to_dict()['bets_left'])
        doc_ref.document(user_id).set({'bets_left': str(amount)}, merge=True)
        ref = doc_ref.document(user_id).get().to_dict()['reffed_by']
        if ref != "-1":
            pass  # ТУТ ЧТО ТО ДЕЛАЕТСЯ ЧЕЛОВЕКУ С ID "ref"
        bot.send_message(chat_id, "Начислено успешно")
    except:
        bot.send_message(chat_id, "Неправильный ввод")
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Добавить матч', 'Удалить матч')
        keyboard.row('Начислить подписку', 'Начислить прогнозы', 'Вернуться в начало')
        bot.send_message(message.chat.id, 'Админ панель для хуесосов кстати егор пидор', reply_markup=keyboard)


def ask_how_many_buy(message):
    chat_id = message.chat.id
    text = message.text
    try:
        amount = int(text)
        keyboard1 = telebot.types.InlineKeyboardMarkup()
        url_button = telebot.types.InlineKeyboardButton(text="Перейти к оплате", url=url.format(nickname=QIWI_NICKNAME,
                                                                                                amount_rub=str(
                                                                                                    ONE_BET_COST * amount),
                                                                                                amount_kop='98'))
        keyboard1.add(url_button)
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        doc = db.collection('users').document(str(message.chat.id)).get().to_dict()
        if doc['isAdmin']:
            keyboard.row('Прогнозы', 'Профиль', 'Функции админа')
        else:
            keyboard.row('Прогнозы', 'Профиль')
        keyboard.row('FAQ', 'Поддержка', 'Реф. система')
        bot.send_message(message.chat.id, str(message.chat.id), reply_markup=keyboard1)
        bot.send_message(message.chat.id, 'ВНИМАНИЕ❗'
                                          ' Не забудьте указать комментарий к платежу, он в предыдущем сообщении'
                                          '\nОбработка платежа может занять до 5 часов', reply_markup=keyboard)
    except:
        bot.send_message(chat_id, "Неправильный ввод")
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Прогнозы', 'Вернуться в начало')
        bot.send_message(message.chat.id, 'Доступные матчи:', reply_markup=keyboard)


def ask_subscription(message):
    chat_id = message.chat.id
    text = message.text.split()
    try:
        user_id = text[0]
        amount = int(text[1])
        doc_ref = db.collection('users')
        amount = amount + int(doc_ref.document(user_id).get().to_dict()['subscription_time'])
        doc_ref.document(user_id).set({'subscription_time': str(amount)}, merge=True)
        ref = doc_ref.document(user_id).get().to_dict()['reffed_by']
        if ref != "-1":
            pass  # ТУТ ЧТО ТО ДЕЛАЕТСЯ ЧЕЛОВЕКУ С ID "ref"
        bot.send_message(chat_id, "Начислено успешно")
    except:
        bot.send_message(chat_id, "Неправильный ввод")
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Добавить матч', 'Удалить матч')
        keyboard.row('Начислить подписку', 'Начислить прогнозы', 'Вернуться в начало')
        bot.send_message(message.chat.id, 'Админ панель для хуесосов кстати егор пидор', reply_markup=keyboard)


def add_match(message):
    chat_id = message.chat.id
    text = message.text.split()
    try:
        doc_ref = db.collection('bets').document('KHL')
        doc_ref.set({text[0] + ',' + text[1]: [text[2] + ',' + text[3] + ',' + text[4],
                                               text[5] + ',' + text[6] + ',' + text[7]]}, merge=True)
        users = db.collection('users').stream()
        params = [text[2] + ',' + text[3] + ',' + text[4], text[5] + ',' + text[6] + ',' + text[7]]
        params1 = list(map(float, params[0].split(",")))
        params2 = list(map(float, params[1].split(",")))
        params = []
        for i in range(len(params1)):
            params.append(params1[i] - params2[i])
        print(params)
        with open("weights", "r") as file:
            weights = list(map(float, file.read().split("\n")))
        file.close()
        bet = sigmoid(numpy.dot(params, weights))
        if bet < 0.25:
            bet = ["П1", str((bet * 100).round())]
        if 0.25 <= bet <= 0.75:
            if 0.45 <= bet <= 0.55:
                bet = ["X", str((bet * 100).round())]
            else:
                if bet < 0.5:
                    bet = ["X1", str((bet * 100).round())]
                else:
                    bet = ["X2", str((bet * 100).round())]
        bet = ["П2", str((bet * 100).round())]


        match = text[0] + ',' + text[1]
        for user in users:
            user_id = user.id
            if user.to_dict()['subscription_time'] > 0:
                bot.send_message(user_id, "Добавлен новый прогноз на матч {match}:\n"
                                 .format(match=" | ".join(match.split(","))) + bet)
                user.update({'bought_KHL': user.to_dict()['bought_KHL'] + [match]})
        bot.send_message(chat_id, "Добавлено успешно")
    except:
        bot.send_message(chat_id, "Неправильный ввод")
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Добавить матч', 'Удалить матч')
        keyboard.row('Начислить подписку', 'Начислить прогнозы', 'Вернуться в начало')
        bot.send_message(message.chat.id, 'Админ панель для хуесосов кстати егор пидор', reply_markup=keyboard)


def del_match(message):
    chat_id = message.chat.id
    text = message.text
    match = ",".join(text.split())
    doc_ref = db.collection('bets').document('KHL')
    users = db.collection('users').stream()
    try:
        new_matches = doc_ref.get().to_dict()
        del new_matches[match]
        # print(new_matches)
        # doc_ref.set(new_matches)
        for user in users:
            user_id = user.id
            user_matches = user.to_dict()['bought_KHL']
            # print(user_matches)
            if match in user_matches:
                del user_matches[user_matches.index(match)]
                print(user_matches)
                db.collection('users').document(str(user_id)).update({'bought_KHL': user_matches})
        bot.send_message(chat_id, "Удалено успешно")
    except:
        bot.send_message(chat_id, "Неправильный ввод")
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Добавить матч', 'Удалить матч')
        keyboard.row('Начислить подписку', 'Начислить прогнозы', 'Вернуться в начало')
        bot.send_message(message.chat.id, 'Админ панель для хуесосов кстати егор пидор', reply_markup=keyboard)


def sigmoid(x):
    return 1 / (1 + numpy.exp(-x))


bot.polling(none_stop=False, interval=0)
