import telebot
from telebot import types
from telebot.types import InputMediaPhoto
import time
import os
import sys

# токен бота
TOKEN = '7520260408:AAGuLeCI9f8Jybp_fFQFyWi5WHaA69fkSYY'
bot = telebot.TeleBot(TOKEN)

def resource_path(relative_path):
   # """ Получает абсолютный путь к ресурсу, работающий и при разработке, и в замороженном exe. """
    try:
        # PyInstaller создает временную папку и сохраняет путь в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

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
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("Подписаться", callback_data="button1")
    button2 = types.InlineKeyboardButton("Индивидуальные консультации", callback_data="button2")
    button3 = types.InlineKeyboardButton("Йога онлайн", callback_data="button3")
    button4 = types.InlineKeyboardButton("Тренинги и обучение", callback_data="button4")
    button5 = types.InlineKeyboardButton("Йога туры и путешествия", callback_data="button5")
    #button4 = types.InlineKeyboardButton("Тренинги и обучение", web_app=types.WebAppInfo(url="https://vk.cc/cIhp9Y"))
    keyboard.add(button1, button2, button3, button4, button5)
    
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

        with open('img/individual.jpg', 'rb') as photo:
            media = InputMediaPhoto(photo, caption='Индивидуальные занятия')
            bot.edit_message_media(media=media, chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)

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
        
        bot.edit_message_text("Международный тренинг Кундалини Йоги: Уровень 2\n«Мы готовы выйти за горизонты своей личности и создать жизнь нового уровня».\nМОДУЛЬ «Путешествие в Слушание: От пустых разговоров к осознанной коммуникации» \n23 - 29 марта 2025 года\nПриглашаем всех, кто завершил обучение на первом уровне (допускаются студенты других школ). Ведущие – Сатйяврати Карта (Франция), Цивилева Светлана, Морозов Иван, Терентьева Татьяна, Бабенко Алексей\nМесто проведения: эко-отель «Территория Дзэн», Тверская область, поселение Щеколдино. \nТрансфер туда – 23 марта в 15:00 от метро «Молодежная»,\nобратно - 29 марта в 11:00 из отеля (оплачивается отдельно).\nСтоимость участия:\n- Москва: 30400 руб.\n- Иногородние: 28500 руб.\nСтоимость для семейной пары (близких родственников):\n- Москва: 28500 руб.\n- Иногородние: 26600 руб.\nСКИДКА:\nповторное участие – 19000 руб.\nСТОИМОСТЬ ПРОЖИВАНИЯ оплачивается дополнительно:\n- 27500 руб. за двухместное проживание\n- 54000 руб. за одноместное проживание", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    
    if call.data == "button5":
        # Создаем клавиатуру с кнопками
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        button1 = types.InlineKeyboardButton("Место СИЛЫ: КАМБОДЖА ТАИЛАНД", url="https://vk.cc/cIhp9Y")
        back_button = types.InlineKeyboardButton("Назад", callback_data="back")
        keyboard.add(button1, back_button)

        # Открываем файл изображения и отправляем его вместе с кнопками
        with open('img/camboja.jpg', 'rb') as photo:
            media = InputMediaPhoto(photo, caption='Текст')
            bot.edit_message_media(media=media, chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)



#bot.edit_message_text("🔥Старт бронирования! Только 3 места по супер цене‼️🔥\nДрузья, мы снова собираем команду для настоящего путешествия — путешествия, которое меняет внутренний мир так же, как и внешние горизонты.\nЗдесь будет сила единства, моменты, наполненные глубиной и осознанностью, утренние практики йоги под первыми лучами солнца и медитации в местах силы, где ощущается энергия веков. Это путешествие для тех, кто хочет не просто увидеть мир, но и почувствовать его.\nМы отправляемся в Тур Таиланд—Камбоджа — две страны, два мира, где древняя культура встречается с духом настоящего приключения.\nЧто вас ждет?\n🌏 От Чиангмая до райских островов\n✔ Горный север Таиланда: священные храмы, могучая энергия природы и чувство полной гармонии\n✔ Мистическая Камбоджа: легендарный Ангкор-Ват, древние святыни, затерянные в джунглях храмы и озеро Тонлесап с его уникальными плавучими деревнями\n✔ Финал — провинция Краби и Пхукет: море, солнце, белоснежные пляжи и волшебная природа залива Пханга\n🏍 Автомото-путешествие: свобода выбора✔ Х                    ", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)    
  
    elif call.data == "back":
        # Возвращаемся в главное меню, обновляя текущее сообщение
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        button1 = types.InlineKeyboardButton("Подписаться", callback_data="button1")
        button2 = types.InlineKeyboardButton("Индивидуальные консультации", callback_data="button2")
        button3 = types.InlineKeyboardButton("Йога онлайн", callback_data="button3")
        button4 = types.InlineKeyboardButton("Тренинги и обучение", callback_data="button4")
        button5 = types.InlineKeyboardButton("Йога туры и путешествия", callback_data="button5")
        keyboard.add(button1, button2, button3, button4, button5)
        bot.send_message(call.message.chat.id, "Главное меню:", reply_markup=keyboard)

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
