import telebot
from telebot import types
from telebot.types import InputMediaPhoto
import time
from threading import Thread
import logging

# токен бота
TOKEN = '7751313417:AAGe0pw3a0t73SBo_vQOU6X-vD-lUGhm0V0'
bot = telebot.TeleBot(TOKEN)
subscribers = []  # Список подписчиков
is_sending = True  # Флаг для контроля рассылки

# Словарь для хранения времени последнего запроса пользователя
user_requests = {}
# Лимит запросов
REQUEST_LIMIT = 15 # Максимум запросов
TIME_FRAME = 10  # Время в секундах


def start_bot():
    try:
        # Обработчик команды /start
        @bot.message_handler(commands=['start'])
        def send_welcome(message):
            chat_id = message.chat.id
            if chat_id not in subscribers:
                subscribers.append(chat_id)
                bot.send_message(chat_id, "Вы подписались на рассылку! Для отмены напишите /stop")
                
                user_id = message.from_user.id
                current_time = time.time()
                
                # Проверка на превышение лимита запросов
                if user_id not in user_requests:
                    user_requests[user_id] = []  # Initialize the user's request times as an empty list
                    
                request_times = user_requests[user_id]
                
                # Удаляем старые запросы
                request_times = [t for t in request_times if current_time - t < TIME_FRAME]
                user_requests[user_id] = request_times

                if len(request_times) >= REQUEST_LIMIT:
                    bot.send_message(chat_id, "Слишком много запросов! Пожалуйста, подождите.")
                    return
                
                request_times.append(current_time)
                user_requests[user_id] = request_times
            # Получение никнейма пользователя
            username = message.from_user.username if message.from_user.username else "пользователь"
            
            # Создаем клавиатуру
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton("Подписаться")
            button2 = types.KeyboardButton("Индивидуальные консультации")
            button3 = types.KeyboardButton("Йога онлайн")
            button4 = types.KeyboardButton("Мероприятия")
            button5 = types.KeyboardButton("Тренинги и обучение")
            button6 = types.KeyboardButton("Йога туры и путешествия")
            keyboard.add(button1)
            keyboard.add(button2)
            keyboard.add(button3)
            keyboard.add(button4)
            keyboard.add(button5)
            keyboard.add(button6)

            # Приветственное сообщение
            with open('/tg_bot/img/join.jpg', 'rb') as photo:
                bot.send_photo(message.chat.id, photo=photo, caption='Приветствие пользователю и информация о боте', reply_markup=keyboard)

        @bot.message_handler(commands=['stop'])
        def stop_message(message):
            global is_sending
            is_sending = False
            chat_id = message.chat.id
            if chat_id in subscribers:
                subscribers.remove(chat_id)
                bot.send_message(chat_id, "Вы отписались от рассылки!")

        def send_periodic_messages():
            global is_sending
            while True:
                if is_sending:
                    for chat_id in subscribers:
                        try:
                            bot.send_message(chat_id, "Запись на личные консультации:\n\n@Harkiretpal \n\nИли WhatsApp по номеру +79856169945")
                        except Exception as e:
                            print(f"Ошибка при отправке сообщения пользователю {chat_id}: {e}")
                    time.sleep(86400)  # Задержка между отправками (в секундах)
                else:
                    time.sleep(1)  # Если рассылка остановлена, проверяем каждый 1 секунду

# Обработчик нажатий на кнопки
        @bot.message_handler(func=lambda message: True)
        def handle_buttons(message):
            username = message.from_user.first_name
            user_id = message.from_user.id
            current_time = time.time()

    # Проверка на превышение лимита запросов
            if user_id in user_requests:
                request_times = user_requests[user_id]
        # Удаляем старые запросы
                request_times = [t for t in request_times if current_time - t < TIME_FRAME]
                user_requests[user_id] = request_times

                if len(request_times) >= REQUEST_LIMIT:
                    bot.answer_callback_query(id, "Слишком много запросов! Пожалуйста, подождите.")
                    return

                request_times.append(current_time)
            else:
                user_requests[user_id] = [current_time]



            if message.text == "Подписаться":
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                register = types.InlineKeyboardButton("Подписка", url='https://t.me/ivanmorozovyogapro')
                keyboard.add(register)
                with open('/tg_bot/img/subscribe.jpg', 'rb') as photo:
                    bot.send_photo(message.chat.id, photo=photo, caption="Полезный контент для жизни и практики йоги. Анонсы мероприятий.", reply_markup=keyboard)

            elif message.text == "Индивидуальные консультации":
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                register = types.InlineKeyboardButton("Подписка", url='https://t.me/ivanmorozovyogapro')
                keyboard.add(register)
                with open('/tg_bot/img/individual.jpg', 'rb') as photo:
                    bot.send_photo(message.chat.id, photo=photo, reply_markup=keyboard)


            elif message.text == "Йога онлайн":
                bot.send_message(message.chat.id, "Скоро")

            elif message.text == "Мероприятия":
                bot.send_message(message.chat.id, "Скоро")


            elif message.text == "Тренинги и обучение":
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                register = types.InlineKeyboardButton("Регистрация", url='http://www.level-2.amritnam.ru/')
                keyboard.add(register)
                with open('/tg_bot/img/trainings.mp4', 'rb') as video:
                    bot.send_video(chat_id=message.chat.id, video=video, caption="Международный тренинг Кундалини Йоги: Уровень 2\n«Мы готовы выйти за горизонты своей личности и создать жизнь нового уровня».\nМОДУЛЬ «Путешествие в Слушание: От пустых разговоров к осознанной коммуникации» \n23 - 29 марта 2025 года\nПриглашаем всех, кто завершил обучение на первом уровне (допускаются студенты других школ). Ведущие – Сатйяврати Карта (Франция), Цивилева Светлана, Морозов Иван, Терентьева Татьяна, Бабенко Алексей\nМесто проведения: эко-отель «Территория Дзэн», Тверская область, поселение Щеколдино. \nТрансфер туда – 23 марта в 15:00 от метро «Молодежная»,\nобратно - 29 марта в 11:00 из отеля (оплачивается отдельно).\nСтоимость участия:\n- Москва: 30400 руб.\n- Иногородние: 28500 руб.\nСтоимость для семейной пары (близких родственников):\n- Москва: 28500 руб.\n- Иногородние: 26600 руб.\nСКИДКА:\nповторное участие – 19000 руб.\nСТОИМОСТЬ ПРОЖИВАНИЯ оплачивается дополнительно:\n- 27500 руб. за двухместное проживание\n- 54000 руб. за одноместное проживание", reply_markup=keyboard)
     

            elif message.text == "Йога туры и путешествия":
                with open('/tg_bot/img/camboja.jpg', 'rb') as photo:
                    keyboard = types.InlineKeyboardMarkup(row_width=1)
                    register = types.InlineKeyboardButton("Место СИЛЫ: КАМБОДЖА ТАИЛАНД 2025", url='https://vk.cc/cIhp9Y')
                    keyboard.add(register)
                    bot.send_photo(chat_id=message.chat.id, photo=photo, caption='🔥Старт бронирования! Только 3 места по супер цене‼️🔥\nДрузья, мы снова собираем команду для настоящего путешествия — путешествия, которое меняет внутренний мир так же, как и внешние горизонты.\nЗдесь будет сила единства, моменты, наполненные глубиной и осознанностью, утренние практики йоги под первыми лучами солнца и медитации в местах силы, где ощущается энергия веков. Это путешествие для тех, кто хочет не просто увидеть мир, но и почувствовать его.\nМы отправляемся в Тур Таиланд—Камбоджа — две страны, два мира, где древняя культура встречается с духом настоящего приключения.\nЧто вас ждет?\n🌏 От Чиангмая до райских островов\n✔ Горный север Таиланда: священные храмы, могучая энергия природы и чувство полной гармонии\n✔ Мистическая Камбоджа: легендарный Ангкор-Ват, древние святыни, затерянные в джунглях храмы и озеро Тонлесап с его уникальными плавучими деревнями\n✔ Финал — провинция Краби и Пхукет: море, солнце, белоснежные пляжи и волшебная природа залива Пханга\n🏍 Автомото-путешествие: свобода выбора✔Х', reply_markup=keyboard)

            else:
                bot.send_message(message.chat.id, "Выберите существующую кнопку.")
        
        bot.polling(none_stop=True)
        Thread(target=send_periodic_messages).start()

    except Exception as e:
        logging.error(f"Ошибка: {e}")
        time.sleep(5)  # Задержка перед перезапуском
        start_bot()  # Перезапуск бота 
        
        
# Запуск бота
if __name__ == '__main__':
    start_bot()

