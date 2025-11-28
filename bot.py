import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# Твой токен от BotFather (создай бота в Telegram через @BotFather и вставь токен здесь)
TOKEN = '8318410343:AAFpLxtj4bnqjaOIku3wY_N-kU9vPtGw3vg'

# Твои реф-ссылки из LeadGid
REF_DJUNIOR = 'https://go.lead-gid.ru/aff_c?aff_id=137697&offer_id=5066&p=adnetwork'  # Джуниор
REF_MOLODEZHNAYA = 'https://go.lead-gid.ru/aff_c?aff_id=137697&offer_id=6299&p=adnetwork'  # Молодёжная
REF_STANDARD = 'https://go.lead-gid.ru/aff_c?aff_id=137697&offer_id=4001&p=adnetwork'  # Стандарт Black
REF_PRO = 'https://go.lead-gid.ru/aff_c?aff_id=137697&offer_id=6432&p=adnetwork'  # Black с Pro

bot = telebot.TeleBot(TOKEN)

# Хранение состояния пользователя
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'step': 1}
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Начать тест"))
    bot.send_message(chat_id, "Привет! За 30 секунд подберём карту Тинькофф с бонусом 5000 руб + 250 руб от меня после первой покупки. Нажми 'Начать тест'!", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    if chat_id not in user_data:
        start(message)
        return

    step = user_data[chat_id]['step']

    if step == 1 and message.text == "Начать тест":
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(KeyboardButton("14–17 лет"), KeyboardButton("18–22 года"))
        markup.add(KeyboardButton("23+ лет"), KeyboardButton("У меня ребёнок 6–14 лет"))
        bot.send_message(chat_id, "Шаг 1: Сколько тебе лет?", reply_markup=markup)
        user_data[chat_id]['step'] = 2

    elif step == 2:
        user_data[chat_id]['age'] = message.text
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(KeyboardButton("Да"), KeyboardButton("Нет"))
        bot.send_message(chat_id, "Шаг 2: У тебя уже есть дебетовая карта Тинькофф?", reply_markup=markup)
        user_data[chat_id]['step'] = 3

    elif step == 3:
        user_data[chat_id]['has_card'] = message.text
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(KeyboardButton("Игры/развлечения"), KeyboardButton("Еда/доставка"))
        markup.add(KeyboardButton("Одежда/техника"), KeyboardButton("Всё подряд"))
        bot.send_message(chat_id, "Шаг 3: На что тратишь больше?", reply_markup=markup)
        user_data[chat_id]['step'] = 4

    elif step == 4:
        user_data[chat_id]['spending'] = message.text
        age = user_data[chat_id]['age']
        has_card = user_data[chat_id]['has_card']
        spending = user_data[chat_id]['spending']

        # Логика выбора оффера
        if age in ["14–17 лет", "У меня ребёнок 6–14 лет"]:
            ref_link = REF_DJUNIOR
            offer_name = "Джуниор (детская карта)"
        elif age == "18–22 года":
            ref_link = REF_MOLODEZHNAYA
            offer_name = "Молодёжная Black"
        else:
            ref_link = REF_STANDARD
            offer_name = "Стандарт Black"

        if has_card == "Да":
            ref_link = REF_PRO
            offer_name = "Black с подпиской Pro"

        # Итоговое сообщение
        text = f"Идеально! Тебе подойдёт {offer_name} с кэшбэком до 30 % на {spending.lower()} + 5000 руб бонус от банка.\nЯ лично переведу 250 руб после твоей первой покупки (хоть на 100 руб).\nОформи за 3 минуты — карта придёт за 1–2 дня!"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Оформить + получить 250 руб", url=ref_link))
        bot.send_message(chat_id, text, reply_markup=markup)

        # Сброс состояния
        del user_data[chat_id]

# Запуск бота
bot.polling()