from telebot import types
import datetime

import methods

stickers = {'Брови, вії': '👁', 'Нігтьовий сервіс':
            '💅🏻', 'Перукарські послуги': '✂'}
service_eyes = ['Корекція брів', 'Фарбування брів',
                'Фарбування вій', 'Нарощування вій',
                'Завивка вій', 'Ламінування вій',
                'Ботокс вій', 'Ламінування брів',
                'Нарощування брів']

service_haircut = []

service_nails = []


def back_and_delete():
    return types.InlineKeyboardButton(text="Повернутися", callback_data='del_message')


def to_menu():
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Меню",
                                                 callback_data='menu')
    keyboard.add(callback_button)
    return keyboard


def choose_role_button_menu():
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Меню",
                                                 callback_data='choose role menu')
    keyboard.add(callback_button)
    return keyboard


def choose_role_button_reg():
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="📝 Зареєструватись",
                                                 callback_data='choose role reg')
    keyboard.add(callback_button)
    return keyboard


def choose_role_menu():
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="💇🏻‍♂️ Клієнт",
                                                 callback_data='change_role 0')
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="💅🏻 Майстер",
                                                 callback_data='change_role 1')
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="🔄 Назад",
                                                 callback_data='del_message')
    keyboard.add(callback_button)
    return keyboard


def choose_role_reg():
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="💇🏻‍♂️ Клієнт",
                                                 callback_data='registration client')
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="💅🏻 Майстер",
                                                 callback_data='registration master')
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="🔄 Назад",
                                                 callback_data='del_message')
    keyboard.add(callback_button)
    return keyboard


def to_menu_2():
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Далі",
                                                 callback_data='menu')
    keyboard.add(callback_button)
    return keyboard


def choose_language_buttons():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    ua_button = types.InlineKeyboardButton(text="🇺🇦 Українська",
                                           callback_data='language UA')
    uk_button = types.InlineKeyboardButton(text="🇬🇧 English",
                                           callback_data='language UK')
    # keyboard.add(ua_button, uk_button)
    keyboard.add(ua_button)
    return keyboard


def client_menu(role):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Записатись на процедуру",
                                                 callback_data=f'order_1 {role}')
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Улюблені майстри",
                                                 callback_data='saved_masters')
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Мій профіль",
                                                 callback_data='check_profile')
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Мої записи",
                                                 callback_data='pre_check_order')
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Змінити роль",
                                                 callback_data='choose role menu')
    keyboard.add(callback_button)
    return keyboard


def client_check_order_buttons():
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="У процесі виконання",
                                                 callback_data='check_order_client 0')
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Виконані замовлення",
                                                 callback_data='check_order_client 1')
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="⬅ Повернутись",
                                                 callback_data='del_message')
    keyboard.add(callback_button)
    return keyboard


def master_menu_1(user_id):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Подивитись тайм слоти",
                                                 callback_data='check_time_slot' + ' ' + str(user_id))
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Подивитись чергу",
                                                 callback_data='check_order_master 0')
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Подивитись мої сертифікати",
                                                 callback_data='check_certificates' + ' ' + str(user_id))
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Подивитись мої роботи",
                                                 callback_data='check_sample_services' + ' ' + str(user_id))
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Подивитись мої послуги",
                                                 callback_data='check_services' + ' ' + str(user_id))
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Мій профіль",
                                                 callback_data='check_profile')
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Далі ➡",
                                                 callback_data='menu_2')
    keyboard.add(callback_button)
    return keyboard


def master_menu_2():
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Додати вільний тайм слот",
                                                 callback_data='add_time_slot')
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Додати свої роботи",
                                                 callback_data='add_sample_service')
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Додати сертифікат",
                                                 callback_data='add_media')
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Додати послугу",
                                                 callback_data='add_service')
    keyboard.add(callback_button)

    callback_button = types.InlineKeyboardButton(text="Подивитись виконані послуги",
                                                 callback_data='check_order_master 1')
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Змінити роль",
                                                 callback_data='choose role menu')
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Назад ⬅",
                                                 callback_data='menu_1')
    keyboard.add(callback_button)
    return keyboard


def service_segments(master_id, add):
    segments = methods.get_service_segments()
    keyboard = types.InlineKeyboardMarkup()
    if add:
        for segment in segments:
            callback_button = types.InlineKeyboardButton(text=stickers[segment.name] + ' ' + str(segment.name),
                                                         callback_data='service_segment ' + str(segment.id) + ' ')
            keyboard.add(callback_button)

    else:
        for segment in segments:
            callback_button = types.InlineKeyboardButton(text=stickers[segment.name] + ' ' + str(segment.name),
                                                         callback_data='order_service ' + str(segment.id) + ' '
                                                                       + str(master_id))
            keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="⬅ Повернутись",
                                                 callback_data='del_message')
    keyboard.add(callback_button)
    return keyboard


def city_buttons(role, reg):
    cities = methods.get_cities()
    keyboard = types.InlineKeyboardMarkup()
    for city in cities:
        callback_button = types.InlineKeyboardButton(text=city.name,
                                                     callback_data='set_city ' + str(city.id) + ' ' + str(role) +
                                                                   ' ' + reg)
        keyboard.add(callback_button)
    return keyboard


def set_placement_buttons(city_id, reg):
    placements = methods.get_placements(city_id)
    text = 'Оберіть цифру, де Ви працюєте💁🏼‍♀️: \n'
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    counter = 1
    for place in placements:
        text += str(counter) + '. ' + place.name + ' ' + str(place.address) + '\n'
        callback_button = types.InlineKeyboardButton(text=counter,
                                                     callback_data='set_placement ' + str(place.id) + ' ' + reg)
        counter += 1
        keyboard.add(callback_button)
    return [text, keyboard]


def master_back():
    return types.InlineKeyboardButton(text="Назад",
                                      callback_data='menu_1')


def send_contact():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Відправити контакт', request_contact=True))
    return markup


def del_button():
    return types.ReplyKeyboardRemove()


def edit_profile(role):
    return types.InlineKeyboardButton(text="Редагувати",
                                      callback_data=f'edit_profile {role}')


def moving_certificates_buttons(index, end_index, data_id, master_id, user_id):
    keyboard = types.InlineKeyboardMarkup()
    if str(user_id) == str(master_id):
        callback_button = types.InlineKeyboardButton(text="Редагувати",
                                                     callback_data='edit_certificate ' + str(data_id))
        keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Меню",
                                                 callback_data='menu')
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Повернутись",
                                                 callback_data='del_message')
    keyboard.add(callback_button)
    if int(index) < int(end_index):
        callback_button = types.InlineKeyboardButton(text="Далі",
                                                     callback_data='move_certificate ' + str(int(index) + 1) +
                                                                   ' ' + str(end_index) + ' ' + str(master_id))
        keyboard.add(callback_button)
    if int(index) > 0:
        callback_button = types.InlineKeyboardButton(text="Назад",
                                                     callback_data='move_certificate ' + str(int(index) - 1) +
                                                                   ' ' + str(end_index) + ' ' + str(master_id))
        keyboard.add(callback_button)
    return keyboard


def moving_services_buttons(index, end_index, data_id, master_id, user_id):
    keyboard = types.InlineKeyboardMarkup()
    if str(user_id) == str(master_id):
        callback_button = types.InlineKeyboardButton(text="Редагувати",
                                                     callback_data='edit_sample_services ' + str(data_id))
        keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Меню",
                                                 callback_data='menu')
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text=" Повернутись",
                                                 callback_data='del_message')
    keyboard.add(callback_button)
    if int(index) < int(end_index):
        callback_button = types.InlineKeyboardButton(text="Далі",
                                                     callback_data='move_services ' + str(int(index) + 1) +
                                                                   ' ' + str(end_index) + ' ' + str(master_id))
        keyboard.add(callback_button)
    if int(index) > 0:
        callback_button = types.InlineKeyboardButton(text="Назад",
                                                     callback_data='move_services ' + str(int(index) - 1) +
                                                                   ' ' + str(end_index) + ' ' + str(master_id))
        keyboard.add(callback_button)
    return keyboard


def edit_sample_service_buttons(service_id, user_id):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Змінити назву",
                                                 callback_data='edit_sample_serv_name ' + str(service_id))
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Змінити фото",
                                                 callback_data='edit_sample_serv_photo ' + str(service_id))
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Видалити",
                                                 callback_data='del_sample_service ' + str(service_id))
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text='Меню', callback_data='to_master_menu')
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Вийти",
                                                 callback_data='check_sample_services ' + str(user_id))
    keyboard.add(callback_button)
    return keyboard


def edit_certificate_buttons(certificate_id, user_id):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Змінити опис",
                                                 callback_data='edit_cer_description ' + str(certificate_id))
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Змінити фото",
                                                 callback_data='edit_cer_photo ' + str(certificate_id))
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Видалити",
                                                 callback_data='del_cer ' + str(certificate_id))
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text='Меню', callback_data='to_master_menu')
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Вийти",
                                                 callback_data='check_certificates ' + str(user_id))
    keyboard.add(callback_button)
    return keyboard


def date_buttons():
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    for i in range(0, 9, 3):
        date_creation_1 = datetime.date.today() + datetime.timedelta(days=i)
        date_creation_1 = date_creation_1.strftime("%y.%m.%d")
        callback_button_1 = types.InlineKeyboardButton(text=str(date_creation_1),
                                                       callback_data='date_create ' + str(date_creation_1))
        date_creation_2 = datetime.date.today() + datetime.timedelta(days=i + 1)
        date_creation_2 = date_creation_2.strftime("%y.%m.%d")
        callback_button_2 = types.InlineKeyboardButton(text=str(date_creation_2),
                                                       callback_data='date_create ' + str(date_creation_2))
        date_creation_3 = datetime.date.today() + datetime.timedelta(days=i + 2)
        date_creation_3 = date_creation_3.strftime("%y.%m.%d")
        callback_button_3 = types.InlineKeyboardButton(text=str(date_creation_3),
                                                       callback_data='date_create ' + str(date_creation_3))
        keyboard.add(callback_button_1, callback_button_2, callback_button_3)
    keyboard.add(back_and_delete())
    return keyboard


def order_placement_buttons(city_id):
    placements = methods.get_placements(city_id)
    text = 'Салони: \n'
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    counter = 1
    buttons = []
    for place in placements:
        text += str(counter) + '. ' + place.name + ' ' + str(place.address) + '\n'
        callback_button = types.InlineKeyboardButton(text=counter,
                                                     callback_data='order_placement ' + str(place.id))
        counter += 1
        buttons.append(callback_button)
    keyboard.add(*buttons)
    return [text, keyboard, placements]


def send_location():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Відправити геопозицію', request_location=True))
    return markup


def moving_masters_buttons(index, end_index, master_id, placement_id):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Подивитись роботи",
                                                 callback_data='check_sample_services' + ' ' + str(master_id))
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Подивитись сертифікати",
                                                 callback_data='check_certificates' + ' ' + str(master_id))
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Додати до улюблених",
                                                 callback_data='add_to_favorite' + ' ' + str(master_id))
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Обрати послугу",
                                                 callback_data='check_services' + ' ' + str(master_id))
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Меню",
                                                 callback_data='menu')
    keyboard.add(callback_button)
    if int(index) < int(end_index):
        callback_button = types.InlineKeyboardButton(text="Далі",
                                                     callback_data='move_masters ' + str(int(index) + 1) +
                                                                   ' ' + str(end_index) +
                                                                   ' ' + str(placement_id))
        keyboard.add(callback_button)
    if int(index) > 0:
        callback_button = types.InlineKeyboardButton(text="Назад",
                                                     callback_data='move_masters ' + str(int(index) - 1) +
                                                                   ' ' + str(end_index) +
                                                                   ' ' + str(placement_id))
        keyboard.add(callback_button)
    return keyboard


def time_slots_buttons(master_id, user_id, service_id):
    time_slots = methods.get_time_slots(master_id)
    if time_slots.__len__() == 0:
        return None
    text = 'Вільні тайм слоти: \n'
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    keyboard.add(types.InlineKeyboardButton(text="⬅ Повернутись",
                                            callback_data='del_message'))
    counter = 1
    buttons = []
    for slot in time_slots:
        text += str(counter) + '. Починаючи з: ' + str(slot.start_time) + ' до: ' + str(slot.end_time) + \
                '. Дата: ' + str(slot.date) + '\n'
        callback_button = types.InlineKeyboardButton(text=counter,
                                                     callback_data='order_time_slot ' + str(slot.id)
                                                                   + ' ' + str(service_id) + ' ' + str(master_id))
        counter += 1
        buttons.append(callback_button)
    if str(user_id) != str(master_id):
        keyboard.add(*buttons)
    else:
        keyboard.add(master_back())
    return [text, keyboard]


def saved_masters(user_id):
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    masters = methods.get_saved_masters(user_id)
    if masters.__len__() < 1:
        return None
    for master in masters:
        user = methods.get_master(master.master_id)
        callback_button = types.InlineKeyboardButton(text=user[0].name,
                                                     callback_data='sav_masters' + ' ' + str(user[0].user_id))
        keyboard.add(callback_button)
    return keyboard


def get_services(master_id, user_id, segment):
    services = methods.get_services(master_id, segment)
    if services.__len__() < 1:
        return None
    text = ''
    counter = 1
    keyboard = types.InlineKeyboardMarkup()
    if str(master_id) == str(user_id):
        for service in services:
            try:
                text += str(counter) + '. ' + service.name + ' Ціна: ' + service.money_cost + \
                        '₴, Час выконання: ' + service.time_cost + '\n'
            except TypeError as tp:
                print(tp)
            counter += 1
        keyboard.add(types.InlineKeyboardButton(text='Редагувати',
                                                callback_data='edit_service ' + segment),
                     types.InlineKeyboardButton(text="⬅ Повернутись",
                                                callback_data='del_message'))
    else:
        text = 'Доступні послуги'
        for service in services:
            callback_button = types.InlineKeyboardButton(text=service.name,
                                                         callback_data='choose_service '
                                                                       + str(master_id) + ' ' + str(service.id))
            keyboard.add(callback_button)
        callback_button = types.InlineKeyboardButton(text="⬅ Повернутись",
                                                     callback_data='del_message')
        keyboard.add(callback_button)
    return [text, keyboard]


def edit_service(user_id, segment):
    services = methods.get_services(user_id, segment)
    if services.__len__() < 1:
        return None
    keyboard = types.InlineKeyboardMarkup()
    for service in services:
        callback_button = types.InlineKeyboardButton(text=service.name,
                                                     callback_data='update_service ' + str(service.id) + ' '
                                                                   + str(segment))
        keyboard.add(callback_button)
    return keyboard


def edit_service_buttons(service_id, segment, user_id):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text='Змінити ціну',
                                                 callback_data='update_price ' + str(service_id) + ' ' +
                                                               str(segment))
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text='Змінити тривалість',
                                                 callback_data='update_time_cost ' + str(service_id) + ' ' +
                                                               str(segment))
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text='Видалити',
                                                 callback_data='delete_service ' + str(service_id) + ' ' + str(segment))
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text='Меню', callback_data='to_master_menu')
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text='Вийти', callback_data='check_services ' + str(user_id))
    keyboard.add(callback_button)
    return keyboard


def feedback_button(master_id):
    return types.InlineKeyboardButton(text="Залишити відгук",
                                      callback_data='send_feedback ' + str(master_id))


def rating_button(master_id):
    return types.InlineKeyboardButton(text="Оцінити майстра",
                                      callback_data='send_rating ' + str(master_id))


def set_rating_buttons(master_id):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text='1', callback_data='set_rating 1 ' + str(master_id)),
        types.InlineKeyboardButton(text='2', callback_data='set_rating 2 ' + str(master_id)),
        types.InlineKeyboardButton(text='3', callback_data='set_rating 3 ' + str(master_id)),
        types.InlineKeyboardButton(text='4', callback_data='set_rating 4 ' + str(master_id)),
        types.InlineKeyboardButton(text='5', callback_data='set_rating 5 ' + str(master_id)))
    return keyboard


def mark_as_done(order_id):
    return types.InlineKeyboardButton(text="Відмітити як виконано",
                                      callback_data='mark_as_done ' + str(order_id))


def empty_template():
    return types.InlineKeyboardMarkup()


def service_buttons(segment, services_name):
    keyboard = types.InlineKeyboardMarkup()
    data = [item[0] for item in services_name]
    if segment == '1':
        service = service_eyes
    elif segment == '2':
        service = service_nails
    elif segment == '3':
        service = service_haircut
    for service_name in service:
        if service_name not in data:
            callback_button = types.InlineKeyboardButton(text=service_name,
                                                         callback_data=f'add_instance {service_name}'
                                                                       + ' ' + str(segment))
            keyboard.add(callback_button)
    return keyboard


def add_more_button(segment):
    return types.InlineKeyboardButton(text='🆕 Додати ще', callback_data='service_segment ' + str(segment))


def edit_profile_buttons(role):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Ім'я",
                                                 callback_data=f'profile_edit name {role}')
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Телефон",
                                                 callback_data=f'profile_edit phone {role}')
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Посилання в телеграмі",
                                                 callback_data=f'profile_edit tg_link {role}')
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Місто",
                                                 callback_data=f'profile_edit edit_city {role}')
    keyboard.add(callback_button)
    if role == 'master':
        callback_button = types.InlineKeyboardButton(text="Номер картки",
                                                     callback_data='profile_edit card')
        keyboard.add(callback_button)
        callback_button = types.InlineKeyboardButton(text="Салон",
                                                     callback_data='profile_edit placement')
        keyboard.add(callback_button)
        callback_button = types.InlineKeyboardButton(text="Опис аккаунту",
                                                     callback_data='profile_edit details')
        keyboard.add(callback_button)
        callback_button = types.InlineKeyboardButton(text="Змінити фото",
                                                     callback_data='profile_edit photo')
        keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Повернутись",
                                                 callback_data='menu')
    keyboard.add(callback_button)
    return keyboard


def reg_as_master():
    keyboard = types.InlineKeyboardMarkup()
    callback_button1 = types.InlineKeyboardButton(text="Так✅",
                                                  callback_data='reg_as_master')
    callback_button2 = types.InlineKeyboardButton(text="Ні❌",
                                                  callback_data='del_message')
    keyboard.add(callback_button1, callback_button2)
    return keyboard


def to_completed_services():
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Повернутись",
                                                 callback_data='check_order_client 1')
    keyboard.add(callback_button)
    return keyboard
