import telebot
from telebot import types
import time

# токен бота
TOKEN = '6779027788:AAGrfHq5F11bvIfW0Gnw6uGpZ9xAr6pVI_k'
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения времени последнего запроса пользователя
user_requests = {}
# Лимит запросов
REQUEST_LIMIT = 15 # Максимум запросов
TIME_FRAME = 10  # Время в секундах

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    current_time = time.time()

    # Проверка на превышение лимита запросов
    if user_id in user_requests:
        request_times = user_requests[user_id]
        # Удаляем старые запросы
        request_times = [t for t in request_times if current_time - t < TIME_FRAME]
        user_requests[user_id] = request_times

        if len(request_times) >= REQUEST_LIMIT:
            bot.send_message(message.chat.id, "Слишком много запросов! Пожалуйста, подождите.")
            return

        request_times.append(current_time)
    else:
        user_requests[user_id] = [current_time]

    # Получение никнейма пользователя
    username = message.from_user.username if message.from_user.username else "пользователь"
    
    # Инлайн-кнопки
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Подписаться", callback_data="button1")
    button2 = types.InlineKeyboardButton("Консультации", callback_data="button2")
    button3 = types.InlineKeyboardButton("Йога онлайн", callback_data="button3")
    button4 = types.InlineKeyboardButton("Тренинги и обучение", callback_data="button4")
    #button4 = types.InlineKeyboardButton("Тренинги и обучение", web_app=types.WebAppInfo(url="https://docs.python-telegram-bot.org/en/stable/examples.timerbot.html"))
    keyboard.add(button1, button2, button3, button4)

    # Приветственное сообщение с ником и инлайн-кнопками
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Выберите одну из кнопок:', reply_markup=keyboard)

# Обработчик нажатий на инлайн-кнопки
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    username = call.from_user.first_name
    user_id = call.from_user.id
    current_time = time.time()

    # Проверка на превышение лимита запросов
    if user_id in user_requests:
        request_times = user_requests[user_id]
        # Удаляем старые запросы
        request_times = [t for t in request_times if current_time - t < TIME_FRAME]
        user_requests[user_id] = request_times

        if len(request_times) >= REQUEST_LIMIT:
            bot.answer_callback_query(call.id, "Слишком много запросов! Пожалуйста, подождите.")
            return

        request_times.append(current_time)
    else:
        user_requests[user_id] = [current_time]

    if call.data == "button1":
        # Обновляем текст сообщения и инлайн-кнопки
        keyboard = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton("Назад", callback_data="back")
        keyboard.add(back_button)
        
        bot.edit_message_text("https://t.me/ivanmorozovyogapro\nПолезный контент для жизни и практики йоги. Анонсы мероприятий.", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)

    if call.data == "button2":
        # Обновляем текст сообщения и инлайн-кнопки
        keyboard = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton("Назад", callback_data="back")
        keyboard.add(back_button)
        
        bot.edit_message_text("Кнопка 2", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)

    if call.data == "button3":
        # Обновляем текст сообщения и инлайн-кнопки
        keyboard = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton("Назад", callback_data="back")
        keyboard.add(back_button)
        
        bot.edit_message_text("Кнопка 3", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    
    if call.data == "button4":
        # Обновляем текст сообщения и инлайн-кнопки
        keyboard = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton("Назад", callback_data="back")
        keyboard.add(back_button)
        
        bot.edit_message_text(" Международный тренинг Кундалини Йоги: Уровень 2\n«Мы готовы выйти за горизонты своей личности и создать жизнь нового уровня».\nМОДУЛЬ «Путешествие в Слушание: От пустых разговоров к осознанной коммуникации» \n23 - 29 марта 2025 года\nПриглашаем всех, кто завершил обучение на первом уровне (допускаются студенты других школ). Ведущие – Сатйяврати Карта (Франция), Цивилева Светлана, Морозов Иван, Терентьева Татьяна, Бабенко Алексей\nМесто проведения: эко-отель «Территория Дзэн», Тверская область, поселение Щеколдино. \nТрансфер туда – 23 марта в 15:00 от метро «Молодежная»,\nобратно - 29 марта в 11:00 из отеля (оплачивается отдельно).\nСтоимость участия:\n- Москва: 30400 руб.\n- Иногородние: 28500 руб.\nСтоимость для семейной пары (близких родственников):\n- Москва: 28500 руб.\n- Иногородние: 26600 руб.\nСКИДКА:\nповторное участие – 19000 руб.\nСТОИМОСТЬ ПРОЖИВАНИЯ оплачивается дополнительно:\n- 27500 руб. за двухместное проживание\n- 54000 руб. за одноместное проживание", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    
    elif call.data == "back":
        # Возвращаемся в главное меню, обновляя текущее сообщение
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Подписаться", callback_data="button1")
        button2 = types.InlineKeyboardButton("Консультации", callback_data="button2")
        button3 = types.InlineKeyboardButton("Йога онлайн", callback_data="button3")
        button4 = types.InlineKeyboardButton("Тренинги и обучение", callback_data="button4")
        keyboard.add(button1, button2, button3, button4)

        bot.edit_message_text(f'Привет, {username}!', chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
