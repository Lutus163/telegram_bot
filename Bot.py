import telebot
from telebot import types
import time

# токен бота
TOKEN = '7939072349:AAEmXZ1C78fyXcfXYrfK2eymZeRHJwXNV6U'
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения времени последнего запроса пользователя
user_requests = {}
# Лимит запросов
REQUEST_LIMIT = 5  # Максимум запросов
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
    button1 = types.InlineKeyboardButton("Кнопка 1", callback_data="button1")
    button2 = types.InlineKeyboardButton("Кнопка 2", callback_data="button2")
    button3 = types.InlineKeyboardButton("Кнопка 3", callback_data="button3")
    button4 = types.InlineKeyboardButton("Веб сайт", web_app=types.WebAppInfo(url="https://docs.python-telegram-bot.org/en/stable/examples.timerbot.html"))
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
        
        bot.edit_message_text("Вы выбрали кнопку 1! Нажмите 'Назад', чтобы вернуться.", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)

    if call.data == "button2":
        # Обновляем текст сообщения и инлайн-кнопки
        keyboard = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton("Назад", callback_data="back")
        keyboard.add(back_button)
        
        bot.edit_message_text("Вы выбрали кнопку 2! Нажмите 'Назад', чтобы вернуться.", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)

    if call.data == "button3":
        # Обновляем текст сообщения и инлайн-кнопки
        keyboard = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton("Назад", callback_data="back")
        keyboard.add(back_button)
        
        bot.edit_message_text("Вы выбрали кнопку 3! Нажмите 'Назад', чтобы вернуться.", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    
    elif call.data == "back":
        # Возвращаемся в главное меню, обновляя текущее сообщение
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Кнопка 1", callback_data="button1")
        button2 = types.InlineKeyboardButton("Кнопка 2", callback_data="button2")
        button3 = types.InlineKeyboardButton("Кнопка 3", callback_data="button3")
        button4 = types.InlineKeyboardButton("Веб сайт", web_app=types.WebAppInfo(url="https://docs.python-telegram-bot.org/en/stable/examples.timerbot.html"))
        keyboard.add(button1, button2, button3, button4)

        bot.edit_message_text(f'Привет, {username}! Выберите одну из кнопок:', chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
