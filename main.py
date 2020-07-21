import random
import re
import buttons
from methods import *
import os
import telebot
import base64
# import time

from config import token

bot = telebot.TeleBot(token=token)
data_path = os.curdir + '\\data\\'


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = buttons.choose_language_buttons()
    bot.send_message(message.from_user.id, 'Обери мову/Choose a language', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    flag = check_user(call.from_user.id)
    if 'registration' in call.data:
        data = call.data.split(' ')
        registration(call.message, data[1])
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return
    elif 'language' in call.data:
        greetings = ('Привіт, мене звуть Лола! 💁‍♀️\n\n'
                     '🤖 Я робот і буду виконувати роль твого'
                     ' персонального менеджера. \n\n')
        if flag:
            keyboard = buttons.choose_role_button_menu()
        else:
            keyboard = buttons.choose_role_button_reg()
            greetings += 'Але перед початком треба  зареєструватись👇🏻'
        bot.send_message(call.from_user.id, greetings,
                         reply_markup=keyboard)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return
    elif "choose role" in call.data:
        data = call.data.split(' ')
        keyboard = buttons.empty_template()
        if data[2] == 'reg':
            keyboard = buttons.choose_role_reg()
        elif data[2] == 'menu':
            keyboard = buttons.choose_role_menu()
        bot.send_message(call.from_user.id, "Оберіть вашу роль 👤",
                         reply_markup=keyboard)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return
    elif 'change_role' in call.data:
        data = call.data.split(' ')
        user_instance = get_user_role(call.from_user.id)
        if data[1] == '1':
            if user_instance:
                set_current_role(call.from_user.id, 1)
                to_menu(call)
                bot.answer_callback_query(call.id, text=" ", show_alert=False)
                return
            else:
                keyboard = buttons.reg_as_master()
                bot.send_message(call.from_user.id, 'Ви не зареєстровані як майстер. Бажаєте зареєструватися?',
                                 reply_markup=keyboard)
            return
        else:
            set_current_role(call.from_user.id, 0)
            to_menu(call)
            bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return
    elif 'set_placement' in call.data:
        bot.delete_message(call.from_user.id, call.message.message_id)
        data = call.data.split(' ')
        update_placement(call.from_user.id, data[1])
        if data[2] == 'reg':
            update_master_flag(call.from_user.id)
            set_current_role(call.from_user.id, True)
            keyboard = buttons.to_menu()
            bot.send_message(call.from_user.id, "Супер! Тепер ви зареєстровані і до вас вже можна записуватись 🥳",
                             reply_markup=keyboard)
        else:
            edit_profile(call.from_user.id, 'master')
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return
    if not flag:
        keyboard = buttons.choose_role_button_reg()
        bot.send_message(call.from_user.id, "Спочатку зареєструйтесь!", reply_markup=keyboard)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return
    if call.data == 'menu':
        to_menu(call)
    elif call.data == 'menu_1':
        bot.edit_message_reply_markup(call.from_user.id, call.message.message_id,
                                      reply_markup=buttons.master_menu_1(call.from_user.id))
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
    elif call.data == 'menu_2':
        bot.edit_message_reply_markup(call.from_user.id, call.message.message_id,
                                      reply_markup=buttons.master_menu_2())
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
    elif 'set_city' in call.data:
        bot.delete_message(call.from_user.id, call.message.message_id)
        data = call.data.split(' ')
        update_city(call.from_user.id, data[1], data[2])
        create_user_role(call.from_user.id)
        if data[3] == 'reg':
            if data[2] == 'master':
                update_to_master(call.from_user.id)
                master_reg_start(call.message, call.from_user.id)
                bot.answer_callback_query(call.id, text=" ", show_alert=False)
                return
            else:
                set_current_role(call.from_user.id, False)
                keyboard = buttons.to_menu()
                bot.send_message(call.from_user.id, "Супер! Тепер ви зареєстровані 🥳",
                                 reply_markup=keyboard)
                bot.answer_callback_query(call.id, text=" ", show_alert=False)
                return
        else:
            edit_profile(call.from_user.id, data[2])
            bot.answer_callback_query(call.id, text=" ", show_alert=False)
            return
    elif call.data == 'check_profile':
        if get_user_role(call.from_user.id):
            show_profile(call.from_user.id, 'master')
        else:
            show_profile(call.from_user.id, 'client')
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return
    elif call.data == 'add_media':
        add_certificate(call.message)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return
    elif call.data == 'add_sample_service':
        bot.send_message(call.from_user.id, 'Напишіть назву послуги (назва послуги повинна відрізнятися від '
                                            'доданих раніше)')
        bot.register_next_step_handler(call.message, add_sample_service)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return
    elif 'check_certificates' in call.data:
        data = call.data.split(' ')
        certificates = get_certificates(data[1])
        end_index = certificates.__len__() - 1
        if end_index == -1:
            bot.answer_callback_query(call.id, text="На жаль, сертифікати не загружені  :(!")
            return
        index = 0
        show_certificates(index, end_index, certificates, call.from_user.id)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
    elif 'move_certificate' in call.data:
        indexes = call.data.split(' ')
        bot.delete_message(call.from_user.id, call.message.message_id)
        certificates = get_certificates(indexes[3])
        show_certificates(indexes[1], indexes[2], certificates, call.from_user.id)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return
    elif 'check_sample_services' in call.data:
        data = call.data.split(' ')
        services = get_sample_services(data[1])
        end_index = services.__len__() - 1
        if end_index == -1:
            bot.answer_callback_query(call.id, text="На жаль, роботи не загружені  :(!")
            return
        index = 0
        show_services(index, end_index, services, call.from_user.id)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
    elif 'move_services' in call.data:
        indexes = call.data.split(' ')
        bot.delete_message(call.from_user.id, call.message.message_id)
        services = get_sample_services(indexes[3])
        show_services(indexes[1], indexes[2], services, call.from_user.id)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return
    elif call.data == 'reg_as_master':
        master_reg_start(call.message, call.from_user.id)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return
    elif call.data == 'add_time_slot':
        keyboard = buttons.date_buttons()
        bot.send_message(call.from_user.id, 'Оберіть дату', reply_markup=keyboard)
        bot.answer_callback_query(call.id, text=' ', show_alert=False)
    elif 'date_create' in call.data:
        data = call.data.split(' ')
        bot.send_message(call.from_user.id, 'Напишіть час початку вільного тайм слоту. (Приклад: 9:00, 14:20): ')
        bot.register_next_step_handler(message=call.message, date=data[1], callback=set_start_time)
        bot.answer_callback_query(call.id, text=' ', show_alert=False)
        return
    elif 'order_1' in call.data:
        data = call.data.split(' ')
        if data == 'client':
            user_instance = get_client(call.from_user.id)
        else:
            user_instance = get_master(call.from_user.id)
        keyboard = buttons.order_placement_buttons(user_instance[0].city_id)
        bot.send_message(call.from_user.id, keyboard[0],
                         reply_markup=keyboard[1])
        bot.answer_callback_query(call.id, text=' ', show_alert=False)
    elif 'order_placement' in call.data:
        data = call.data.split(' ')
        masters = get_masters(data[1])
        end_index = masters.__len__() - 1
        if end_index == -1:
            bot.answer_callback_query(call.id, text="На жаль, у даному салоні майстри ще не зареєестровані :(")
            return
        bot.send_message(call.from_user.id, 'А зараз оберіть майстра',
                         reply_markup=buttons.del_button())
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        index = 0
        show_masters(index, end_index, masters, call.from_user.id)
    elif 'move_masters' in call.data:
        bot.delete_message(call.from_user.id, call.message.message_id)
        indexes = call.data.split(' ')
        masters = get_masters(indexes[3])
        show_masters(indexes[1], indexes[2], masters, call.from_user.id)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return
    elif 'check_time_slot' in call.data:
        data = call.data.split(' ')
        check_time_slot(data[1], call, None)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
    elif call.data == 'del_message':
        bot.delete_message(call.from_user.id, call.message.message_id)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
    elif 'add_to_favorite' in call.data:
        data = call.data.split(' ')
        if str(data[1]) != str(call.from_user.id):
            if check_saved_masters(master_id=data[1], user_id=call.from_user.id):
                save_master(master_id=data[1], user_id=call.from_user.id)
                bot.answer_callback_query(call.id, text="Додано!")
            else:
                bot.answer_callback_query(call.id, text="Ви вже додали цього майстра до улюблених!")
        else:
            bot.answer_callback_query(call.id, text="Ви не можете додати самого"
                                                    " себе до улюблених майстрів!")
    elif call.data == 'saved_masters':
        keyboard = buttons.saved_masters(call.from_user.id)
        if keyboard is None:
            bot.answer_callback_query(call.id, text="Ви не додали жодного майстра до улюблених")
            return
        bot.send_message(call.from_user.id, "Улюблені майстри:", reply_markup=keyboard)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
    elif 'check_services' in call.data:
        data = call.data.split(' ')
        if str(data[1]) == str(call.from_user.id):
            bot.answer_callback_query(call.id, text="Ви не можете записатися до самого себе!")
            return
        keyboard = buttons.service_segments(data[1], False)
        bot.send_message(call.from_user.id, 'Оберіть сегмент послуг 🧚🏻‍',
                         reply_markup=keyboard)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
    elif 'order_service' in call.data:
        data = call.data.split(' ')
        keyboard = buttons.get_services(data[2], call.from_user.id, data[1])
        if keyboard is None:
            bot.answer_callback_query(call.id, text="На жаль, послуги не додані")
            return
        if str(call.from_user.id) is str(data[2]):
            bot.send_message(call.from_user.id, 'Уточніть процедуру 🗂',
                             reply_markup=keyboard[1])
        else:
            bot.send_message(call.from_user.id, keyboard[0],
                             reply_markup=keyboard[1])
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
    elif call.data == 'add_service':
        keyboard = buttons.service_segments(call.from_user.id, True)
        bot.send_message(call.from_user.id,
                         'Оберіть сегмент послуг, що надаєте 🧚🏻‍♀',
                         reply_markup=keyboard)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
    elif 'service_segment' in call.data:
        data = call.data.split(' ')
        services_name = get_service_names(call.from_user.id, data[1])
        keyboard = buttons.service_buttons(data[1], services_name)
        bot.send_message(call.from_user.id, 'Тепер уточніть процедуру 🗂',
                         reply_markup=keyboard)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
    elif 'add_instance' in call.data:
        data = call.data.split(' ')
        service = data[1]
        segment = data[2]
        if data.__len__() == 4:
            service = data[1] + ' ' + data[2]
            segment = data[3]
        service_id = create_service(call.from_user.id, str(service), str(segment))
        bot.send_message(call.from_user.id, '💵 Яка вартість процедури?')
        bot.register_next_step_handler(message=call.message, service_id=service_id, segment=segment,
                                       callback=set_money_cost, reg='reg')
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
    elif 'sav_masters' in call.data:
        data = call.data.split(' ')
        masters = get_master_by_id(data[1])
        show_masters(0, 0, masters, call.from_user.id)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
    elif 'choose_service ' in call.data:
        data = call.data.split(' ')
        check_time_slot(data[1], call, data[2])
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
    elif 'order_time_slot' in call.data:
        bot.delete_message(call.from_user.id, call.message.message_id)
        data = call.data.split(' ')
        bot.send_message(call.from_user.id, 'предоплата', reply_markup=buttons.to_menu())
        create_order(data[1], call.from_user.id, data[3], data[2])
        set_busy_time_slot(data[1])
        bot.answer_callback_query(call.id, text="Заявку створено")
    elif call.data == 'pre_check_order':
        keyboard = buttons.client_check_order_buttons()
        bot.send_message(call.from_user.id, 'Оберіть опцію', reply_markup=keyboard)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
    elif 'check_order_client' in call.data:
        data = call.data.split(' ')
        orders = get_orders_for_client(call.from_user.id, data[1])
        if orders.__len__() < 1:
            bot.answer_callback_query(call.id, text="Замовлення не знайденні")
            return
        show_orders(orders, call.from_user.id, False)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
    elif 'check_order_master' in call.data:
        data = call.data.split(' ')
        orders = get_orders_for_master(call.from_user.id, data[1])
        if orders.__len__() < 1:
            bot.answer_callback_query(call.id, text="Замовлення не знайденні")
            return
        show_orders(orders, call.from_user.id, True)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
    elif 'mark_as_done' in call.data:
        data = call.data.split(' ')
        update_order_as_done(data[1])
        bot.answer_callback_query(call.id, text="Відмічено!")
    elif call.data == 'pre_check_order':
        keyboard = buttons.client_check_order_buttons()
        bot.send_message(call.from_user.id, 'Оберіть, що ви хочете переглянути:',
                         reply_markup=keyboard)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
    elif 'edit_profile' in call.data:
        data = call.data.split(' ')
        edit_profile(call.from_user.id, data[1])
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
    elif 'profile_edit' in call.data:
        data = call.data.split(' ')
        if data[1] == 'name':
            bot.send_message(call.from_user.id, "Введіть своє ім'я"
                                                "(можна латиницею) і натисніть Enter ↩")
            bot.register_next_step_handler(message=call.message, call_id=call.id, callback=edit_name, role=data[2])
        elif data[1] == 'phone':
            bot.send_message(call.from_user.id, "Тепер надішліть свій телефон ☎️",
                             reply_markup=buttons.send_contact())
            bot.register_next_step_handler(message=call.message, callback=edit_telephone, role=data[2])
        elif data[1] == 'tg_link':
            update_user_name(call.from_user.id, call.from_user.username, role=data[2])
            bot.answer_callback_query(call.id, text="Змінено")
        elif data[1] == 'card':
            bot.send_message(call.from_user.id,
                             'Напишіть номер картки, на яку '
                             'будуть надходити кошти.\n\n'
                             'Також рекомендую видалити його з чату 😉')
            bot.register_next_step_handler(message=call.message, call_id=call.id, callback=edit_card)
        elif data[1] == 'placement':
            user_instance = get_master(call.from_user.id)
            data = buttons.set_placement_buttons(user_instance[0].city_id, '')
            bot.send_message(call.from_user.id, data[0],
                             reply_markup=data[1])
            bot.answer_callback_query(call.id, text=" ", show_alert=False)
        elif data[1] == 'edit_city':
            keyboard = buttons.city_buttons(data[2], '1')
            bot.send_message(call.from_user.id, "Оберіть Ваше місто🌆:", reply_markup=keyboard)
            bot.answer_callback_query(call.id, text=" ", show_alert=False)
        elif data[1] == 'details':
            bot.send_message(call.from_user.id, 'Напишіть опис до аккаунту, '
                                                'що ви вмієте і тд.')
            bot.register_next_step_handler(message=call.message, call_id=call.id, callback=edit_details)
        elif data[1] == 'photo':
            bot.send_message(call.from_user.id, 'Відправте мені ваше фото')
            bot.register_next_step_handler(message=call.message, reg='', callback=set_acc_photo)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return
    elif 'edit_service' in call.data:
        data = call.data.split(' ')
        keyboard = buttons.edit_service(call.from_user.id, data[1])
        if keyboard is None:
            bot.answer_callback_query(call.id, text="Послуг не додано(")
            return
        bot.send_message(call.from_user.id, 'Оберіть послугу, що хочете змінити🛠',
                         reply_markup=keyboard)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return
    elif 'update_service' in call.data:
        data = call.data.split(' ')
        bot.delete_message(call.from_user.id, call.message.message_id)
        keyboard = buttons.edit_service_buttons(data[1], data[2], call.from_user.id)
        bot.send_message(call.from_user.id, 'Оберіть, що хочете змінити⚙',
                         reply_markup=keyboard)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return
    elif 'update_price' in call.data:
        data = call.data.split(' ')
        bot.send_message(call.from_user.id, 'Напишіть нову ціну послуги💸')
        bot.register_next_step_handler(call.message, set_money_cost, data[1], data[2])
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return
    elif 'update_time_cost' in call.data:
        data = call.data.split(' ')
        bot.send_message(call.from_user.id, 'Напишіть тривалість послуги⏳')
        bot.register_next_step_handler(message=call.message, callback=set_time_cost,
                                       service_id=data[1], segment=data[2])
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return
    elif 'delete_service' in call.data:
        data = call.data.split(' ')
        bot.delete_message(call.from_user.id, call.message.message_id)
        try:
            delete_service(data[1])
        except Exception as ex:
            print(ex)
            bot.answer_callback_query(call.id, text="Виникла помилка!")
            return
        keyboard = buttons.service_segments(call.from_user.id, False)
        bot.send_message(call.from_user.id, 'Оберіть сегмент послуг 🧚🏻‍',
                         reply_markup=keyboard)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return
    elif 'edit_sample_services' in call.data:
        data = call.data.split(' ')
        try:
            edit_sample_service(data[1], call.from_user.id)
        except Exception as ex:
            print(ex)
            bot.answer_callback_query(call.id, text="Виникла помилка!")
            return
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return
    elif 'edit_sample_serv_name' in call.data:
        data = call.data.split(' ')
        bot.send_message(call.from_user.id, 'Напишіть назву послуги')
        bot.register_next_step_handler(call.message, edit_sample_service_name, data[1])
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return
    elif 'edit_sample_serv_photo' in call.data:
        data = call.data.split(' ')
        bot.send_message(call.from_user.id, 'Відправте нову фотографію')
        bot.register_next_step_handler(call.message, edit_sample_service_photo, data[1])
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return
    elif 'del_sample_service' in call.data:
        data = call.data.split(' ')
        try:
            delete_service_image(data[1], call.from_user.id)
            delete_sample_service(data[1])
        except Exception as ex:
            print(ex)
            bot.answer_callback_query(call.id, text="Виникла помилка!")
            return
        services = get_sample_services(call.from_user.id)
        end_index = services.__len__() - 1
        if end_index == -1:
            to_menu(call)
            bot.answer_callback_query(call.id, text=" ", show_alert=False)
            return
        index = 0
        show_services(index, end_index, services, call.from_user.id)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return
    elif 'edit_certificate' in call.data:
        data = call.data.split(' ')
        try:
            edit_certificate(data[1], call.from_user.id)
        except Exception as ex:
            print(ex)
            bot.answer_callback_query(call.id, text="Виникла помилка!")
            return
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return
    elif 'edit_cer_description' in call.data:
        data = call.data.split(' ')
        bot.send_message(call.from_user.id, 'Напишіть новий опис')
        bot.register_next_step_handler(call.message, edit_certificate_description, data[1])
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return
    elif 'edit_cer_photo' in call.data:
        data = call.data.split(' ')
        bot.send_message(call.from_user.id, 'Відправте нову фотографію')
        bot.register_next_step_handler(call.message, edit_certificate_photo, data[1])
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return
    elif 'del_cer' in call.data:
        data = call.data.split(' ')
        try:
            delete_certificate_image(data[1], call.from_user.id)
            delete_certificate(data[1])
        except Exception as ex:
            print(ex)
            bot.answer_callback_query(call.id, text="Виникла помилка!")
            return
        certificates = get_certificates(call.from_user.id)
        end_index = certificates.__len__() - 1
        if end_index == -1:
            to_menu(call)
            bot.answer_callback_query(call.id, text=" ", show_alert=False)
            return
        index = 0
        show_certificates(index, end_index, certificates, call.from_user.id)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return


def delete_service_image(service_id, user_id):
    service_instance = get_sample_service_by_id(service_id)
    if service_instance[0].image is not None:
        try:
            os.remove(data_path + str(user_id) + '\\services\\' +
                      str(service_instance[0].image) + '.jpg')
        except Exception as ex:
            print(ex)


def delete_certificate_image(certificate_id, user_id):
    certificate_instance = get_certificate_by_id(certificate_id)
    if certificate_instance[0].image is not None:
        try:
            os.remove(data_path + str(user_id) + '\\certificates\\' +
                      str(certificate_instance[0].image) + '.jpg')
        except Exception as ex:
            print(ex)


def edit_certificate(certificate_id, user_id):
    keyboard = buttons.edit_certificate_buttons(certificate_id, user_id)
    bot.send_message(user_id, 'Оберіть, що хочете змінити⚙',
                     reply_markup=keyboard)


def edit_certificate_description(message, certificate_id):
    if message.text is None:
        bot.send_message(message.from_user.id, 'Неправильний формат вводу,'
                                               ' напишіть назву послуги')
        bot.register_next_step_handler(message, edit_certificate_description, certificate_id)
    try:
        update_certificate_description(certificate_id, message.text)
    except Exception as ex:
        print(ex)
        edit_certificate(certificate_id, message.from_user.id)
        return
    edit_certificate(certificate_id, message.from_user.id)
    return


def edit_certificate_photo(message, certificate_id):
    certificate_instance = get_certificate_by_id(certificate_id)
    if certificate_instance.__len__() < 1:
        return
    if certificate_instance[0].image is not None:
        ran = certificate_instance[0].image
    else:
        while True:
            ran = str(message.from_user.id) + '_' + str(random.randint(1000, 9999))
            if not os.path.exists(data_path + str(message.from_user.id) + '\\certificates\\' +
                                  str(ran) + '.jpg'):
                break
    update_certificate_photo(message, ran, False)
    edit_certificate(certificate_id, message.from_user.id)


def update_certificate_photo(message, ran, create):
    if not os.path.exists(data_path + str(message.from_user.id) + '\\certificates'):
        os.makedirs(data_path + str(message.from_user.id) + '\\certificates')
    try:
        photo = get_photo(message)
    except Exception as ex:
        print(ex)
        bot.send_message(message.from_user.id, "Відправте фотографію (можливо Ви її відправили у форматі файлу,"
                                               " потрібно у форматі фотографії!)")
        bot.register_next_step_handler(message, set_certificate_photo)
        return

    with open(data_path + str(message.from_user.id) + '\\certificates\\' +
              str(ran) + '.jpg', 'wb') as file:
        file.write(photo)
    image = str(ran)
    if create:
        create_certificate(message.from_user.id, image)
        return image
    else:
        return


def to_menu(call):
    if get_user_role(call.from_user.id):
        user_instance = get_master(call.from_user.id)
        if user_instance[0].cur_role:
            keyboard = buttons.master_menu_1(call.from_user.id)
        else:
            keyboard = buttons.client_menu('master')
    else:
        keyboard = buttons.client_menu('client')
    bot.send_message(call.from_user.id, 'Меню', reply_markup=keyboard)
    # bot.edit_message_text('Меню', call.from_user.id, call.message.message_id)
    # bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=keyboard)


def edit_sample_service(service_id, user_id):
    keyboard = buttons.edit_sample_service_buttons(service_id, user_id)
    bot.send_message(user_id, 'Оберіть, що хочете змінити⚙',
                     reply_markup=keyboard)


def edit_sample_service_photo(message, service_id):
    service_instance = get_sample_service_by_id(service_id)
    if service_instance.__len__() < 1:
        return
    if service_instance[0].image is not None:
        ran = service_instance[0].image
    else:
        while True:
            ran = str(message.from_user.id) + '_' + str(random.randint(1000, 9999))
            print(ran)
            if not os.path.exists(data_path + str(message.from_user.id) + '\\services\\' +
                                  str(ran) + '.jpg'):
                break
    update_samp_serv_photo(message, service_id, ran)
    edit_sample_service(service_id, message.from_user.id)


def update_samp_serv_photo(message, service_id, ran):
    if not os.path.exists(data_path + str(message.from_user.id) + '\\services'):
        os.makedirs(data_path + str(message.from_user.id) + '\\services')
    try:
        photo = get_photo(message)
    except Exception as ex:
        print(ex)
        bot.send_message(message.from_user.id, "Відправте фотографію (можливо Ви її відправили у форматі файлу,"
                                               " потрібно у форматі фотографії!)")
        bot.register_next_step_handler(message=message, service_id=service_id, callback=update_samp_serv_photo)
        return
    with open(data_path + str(message.from_user.id) + '\\services\\' +
              str(ran) + '.jpg', 'wb') as file:
        file.write(photo)
    image = str(ran)
    update_service_photo(message.from_user.id, service_id, image)


def edit_sample_service_name(message, service_id):
    if message.text is None:
        bot.send_message(message.from_user.id, 'Неправильний формат вводу,'
                                               ' напишіть назву послуги')
        bot.register_next_step_handler(message, edit_sample_service_name, service_id)
    try:
        update_sample_service_name(service_id, message.text)
    except Exception as ex:
        print(ex)
        edit_sample_service(service_id, message.from_user.id)
        return
    edit_sample_service(service_id, message.from_user.id)
    return


def edit_service(user_id, segment):
    keyboard = buttons.get_services(user_id, user_id, segment)
    bot.send_message(user_id, keyboard[0],
                     reply_markup=keyboard[1])


def master_reg_start(message, user_id):
    bot.send_message(user_id, 'Відправте мені ваше фото')
    bot.register_next_step_handler(message=message, reg='reg', callback=set_acc_photo)


def edit_name(message, call_id, role):
    update_name(message.from_user.id, message.text, role)
    edit_profile(message.from_user.id, role)
    bot.answer_callback_query(call_id, text="Змінено")


def edit_telephone(message, role):
    if message.contact is not None:
        update_telephone(message.from_user.id, message.contact.phone_number, role)
    else:
        update_telephone(message.from_user.id, message.text, role)
    bot.send_message(message.from_user.id, 'Змінено!', reply_markup=buttons.del_button())
    edit_profile(message.from_user.id, role)


def edit_card(message, call_id):
    update_card(message.from_user.id, base64.standard_b64encode(message.text.encode('UTF-8')))
    edit_profile(message.from_user.id, 'master')
    bot.answer_callback_query(call_id, text="Змінено")


def edit_profile(user_id, role):
    keyboard = buttons.edit_profile_buttons(role)
    bot.send_message(user_id, 'Оберіть, що хочете змінити🛠',
                     reply_markup=keyboard)


def edit_details(message, call_id):
    update_acc_details(message.from_user.id, message.text)
    edit_profile(message.from_user.id, 'master')
    bot.answer_callback_query(call_id, text="Змінено")


def set_money_cost(message, service_id, segment, reg='1'):
    if not message.text.isdigit():
        bot.send_message(message.chat.id, 'Це повинно бути число')
        bot.register_next_step_handler(message, set_money_cost, service_id, segment, reg)
        return
    update_service_cost(service_id, message.text)
    if reg == 'reg':
        bot.send_message(message.chat.id, 'Скільки процедура займає часу⏱? \n\n'
                                          '_Наприклад, 1-15 – це буде одна година, '
                                          '15 хвилин._',
                         parse_mode='markdown')
        bot.register_next_step_handler(message, set_time_cost, service_id, segment, reg)
    else:
        bot.send_message(message.from_user.id, 'Виконано!')
        edit_service(message.from_user.id, segment)


def set_time_cost(message, service_id, segment, reg='1'):
    if re.match(r'^([0-1]?[0-9]|2[0-3])-[0-5][0-9]$', message.text):
        data = message.text.split('-')
    else:
        bot.send_message(message.chat.id, 'Формат часу: 1-15 – це буде одна '
                                          'година, 15 хвилин.')
        bot.register_next_step_handler(message, set_time_cost, service_id, segment, reg)
        return
    update_service_time_cost(service_id, data[0] + ':' + data[1])
    if reg == 'reg':
        keyboard = buttons.to_menu_2()
        keyboard.add(buttons.add_more_button(segment))
        bot.send_message(message.chat.id, 'Процедуру додано 👍', reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, 'Виконано!')
        edit_service(message.from_user.id, segment)


def show_orders(orders, user_id, master_flag):
    for order in orders:
        keyboard = buttons.empty_template()
        service = get_service_by_id(order.service_id)
        time_slot = get_time_slot_by_id(order.time_slot_id)
        master = get_master(order.master_id)
        prepaid = 'Так' if order.prepaid else 'Ні'
        if not master_flag:
            if check_rating(order.master_id, order.client_id) and order.done:
                keyboard.add(buttons.rating_button(order.master_id, order.client_id))
            if check_feedback(order.master_id, order.client_id) and order.done:
                keyboard.add(buttons.feedback_button(order.master_id, order.client_id))
        elif master_flag and not order.done:
            keyboard.add(buttons.mark_as_done(order.id))
        bot.send_message(user_id, f'`Назва послуги:` {str(service[0].name)} \n'
                                  f"`Ім'я майстра:` {str(master[0].name)} \n"
                                  f"`Телефон майстра:` {str(master[0].telephone)} \n"
                                  f"`Дата:` {str(time_slot[0].date)} \n"
                                  f"`Початок о:` {str(time_slot[0].start_time)} \n"
                                  f"`Передплачено: ` {str(prepaid)} \n",
                         reply_markup=keyboard, parse_mode='markdown')
    bot.send_message(user_id, 'Повернутись у меню', reply_markup=buttons.to_menu())


def check_time_slot(data, call, service_id):
    keyboard = buttons.time_slots_buttons(data, call.from_user.id, service_id)
    if keyboard is None:
        bot.answer_callback_query(call.id, text="На жаль, "
                                                "вільних тайм слотів недодано :(")
        return
    bot.send_message(call.from_user.id, keyboard[0], reply_markup=keyboard[1])


def registration(message, role):
    bot.send_message(message.chat.id, "Введіть своє ім'я, за яким клієнт зможе вас знайти "
                                      "(можна латиницею) і натисніть Enter ↩️")
    bot.register_next_step_handler(message=message, role=role, callback=set_name)


def set_name(message, role):
    create_user(user_id=message.from_user.id, name=message.text, username=message.from_user.username, role=role)
    bot.send_message(message.chat.id, "Тепер надішліть свій телефон ☎️",
                     reply_markup=buttons.send_contact())
    bot.register_next_step_handler(message=message, role=role, callback=set_telephone)


def set_telephone(message, role):
    if message.contact is not None:
        update_telephone(message.from_user.id, message.contact.phone_number, role)
    else:
        update_telephone(message.from_user.id, message.text, role)
    keyboard = buttons.city_buttons(role, 'reg')
    bot.send_message(message.from_user.id, 'Слідуйте далі!', reply_markup=buttons.del_button())
    bot.send_message(message.chat.id, "А зараз оберіть Ваше місто:", reply_markup=keyboard)
    # bot.send_message(message.chat.id, "залишилось ще трошки", reply_markup=buttons.del_button())
    # bot.send_message(message.chat.id, "введіть Вашу email адресу")
    # bot.register_next_step_handler(message, set_email)


# def set_email(message):
#     if not re.match(r'^[a-z0-9A-Z]+[._]?[a-z0-9A-Z]+[@]\w+[.]\w{2,3}$', message.text):
#         bot.send_message(message.chat.id, "Невірний формат електронної адреси")
#         bot.send_message(message.chat.id, "Спробуйте ще раз!")
#         bot.register_next_step_handler(message, set_email)
#         return
#     else:
#         update_email(message.from_user.id, message.text)
#         keyboard = buttons.city_buttons()
#         bot.send_message(message.chat.id, "А зараз оберіть Ваше місто:", reply_markup=keyboard)
#         return


def set_acc_photo(message, reg):
    if not os.path.exists(data_path + str(message.from_user.id) + '\\profile'):
        os.makedirs(data_path + str(message.from_user.id) + '\\profile')
    try:
        photo = get_photo(message)
    except Exception as ex:
        print(ex)
        bot.send_message(message.from_user.id, "Відправте фотографію (можливо Ви її відправили у форматі файлу,"
                                               " потрібно у форматі фотографії!)")
        # bot.register_next_step_handler(message, set_acc_photo)
        return
    with open(data_path + str(message.from_user.id) + '\\profile\\profile.jpg', 'wb') as file:
        file.write(photo)
    update_acc_photo(message.from_user.id)
    if reg == 'reg':
        bot.send_message(message.from_user.id,
                         'Напишіть номер картки, на яку будуть '
                         'надходити кошти.'
                         'Також рекомендую видалити його з чату 😉')
        bot.register_next_step_handler(message, set_card)
    else:
        edit_profile(message.from_user.id, 'master')


def set_card(message):
    update_card(message.from_user.id, base64.standard_b64encode(message.text.encode('UTF-8')))
    bot.send_message(message.from_user.id,
                     'Напишіть опис до аккаунту, що ви вмієте і тд.')
    bot.register_next_step_handler(message, set_acc_details)


def set_acc_details(message):
    update_acc_details(message.from_user.id, message.text)
    user_instance = get_master(message.from_user.id)
    data = buttons.set_placement_buttons(user_instance[0].city_id, 'reg')
    bot.send_message(message.from_user.id, data[0],
                     reply_markup=data[1])


def show_profile(user_id, role):
    keyboard = buttons.to_menu()
    keyboard.add(buttons.edit_profile(role))
    if role == 'master':
        instance = get_master(user_id)
        try:
            img = open(data_path + str(user_id) + '\\profile\\profile.jpg', 'rb')
        except Exception as ex:
            print(ex)
            img = open(data_path + 'default.jpeg', 'rb')
        bot.send_photo(user_id, photo=img,
                       caption=f"`Ім'я:` {instance[0].name} \n\n"
                               f"`Телефон:` {instance[0].telephone} \n\n"
                       # f"`Пошта:` {instance[0].email} \n\n"
                               f"`Посилання в телеграмі:` @{instance[0].username} \n\n"
                               f"`Номер картки:` _*_"
                               f"{(base64.standard_b64decode(instance[0].card)).decode('UTF-8')[-4:]} \n\n"
                               f"`Назва салону:` {instance[2]} \n\n"
                               f"`Місто:` {instance[3]} \n\n"
                               f"`Опис аккаунту:` {instance[0].details} \n\n"
                               f"`Мій рейтинг:` {instance[1]} \n\n", parse_mode='markdown', reply_markup=keyboard)
        img.close()
    else:
        instance = get_client(user_id)
        bot.send_message(user_id,
                         f"`Ім'я:` {instance[0].name} \n\n"
                         f"`Телефон:` {instance[0].telephone} \n\n"
                         # f"`Пошта:` {instance[0].email} \n\n"
                         f"`Посилання в телеграмі:` @{instance[0].username} \n\n"
                         f"`Місто:` {instance[2]} \n\n",
                         parse_mode='markdown', reply_markup=keyboard)


def add_certificate(message):
    bot.send_message(message.chat.id, 'Відправте фото сертифікату')
    bot.register_next_step_handler(message, set_certificate_photo)


def set_certificate_photo(message):
    while True:
        ran = str(message.from_user.id) + '_' + str(random.randint(1000, 9999))
        if not os.path.exists(data_path + str(message.from_user.id) + '\\certificates\\' +
                              str(ran) + '.jpg'):
            break
    image = update_certificate_photo(message, ran, True)
    bot.send_message(message.chat.id, 'Напишіть опис до фото:')
    bot.register_next_step_handler(message=message, image=image, callback=set_certificate_details)


def set_certificate_details(message, image):
    update_certificate_details(message.from_user.id, image, message.text)
    keyboard = buttons.to_menu()
    bot.send_message(message.from_user.id, 'Додано!', reply_markup=keyboard)


def get_photo(message):
    photo_id = message.json['photo'][0]['file_id']
    return bot.download_file(bot.get_file(photo_id).file_path)


def add_sample_service(message):
    if message.text is None:
        bot.send_message(message.from_user.id, 'Неправильний формат вводу, напишіть, будь ласка, назву послуги')
        bot.register_next_step_handler(message, add_sample_service)
        return
    check = check_service(message.text, message.from_user.id)
    if check:
        service_id = create_sample_service(message.from_user.id, message.text)
    else:
        bot.send_message(message.from_user.id, 'Така послуга вже існує,'
                                               ' пропоную змініти назву!')
        bot.register_next_step_handler(message, add_sample_service)
        return
    bot.send_message(message.from_user.id, 'Відправте фото прикладу роботи')
    bot.register_next_step_handler(message=message, service_id=service_id, callback=set_service_photo)


def set_service_photo(message, service_id):
    while True:
        ran = str(message.from_user.id) + '_' + str(random.randint(1000, 9999))
        if not os.path.exists(data_path + str(message.from_user.id) + '\\services\\' +
                              str(ran) + '.jpg'):
            break
    update_samp_serv_photo(message, service_id, ran)
    keyboard = buttons.to_menu()
    bot.send_message(message.from_user.id, 'Додано!', reply_markup=keyboard)


def show_certificates(index, end_index, certificates, user_id):
    keyboard = buttons.moving_certificates_buttons(index, end_index, certificates[int(index)].id,
                                                   certificates[int(index)].user_id, user_id)
    try:
        img = open(data_path + str(certificates[int(index)].user_id) + '\\certificates\\' + certificates[
            int(index)].image + '.jpg', 'rb')
    except Exception as ex:
        print(ex)
        img = open(data_path + 'default.jpeg', 'rb')
    bot.send_photo(user_id, photo=img,
                   caption=f"`Опис:` {certificates[int(index)].description} \n\n", reply_markup=keyboard,
                   parse_mode='markdown')


def show_services(index, end_index, services, user_id):
    keyboard = buttons.moving_services_buttons(index, end_index, services[int(index)].id,
                                               services[int(index)].master_id, user_id)
    try:
        img = open(data_path + str(services[int(index)].master_id) + '\\services\\' + services[int(index)].image
                   + '.jpg', 'rb')
    except Exception as ex:
        print(ex)
        img = open(data_path + 'default.jpeg', 'rb')
    bot.send_photo(user_id, photo=img,
                   caption=f"`Назва:` {services[int(index)].name} \n\n",
                   reply_markup=keyboard,
                   parse_mode='markdown')


def show_masters(index, end_index, masters, user_id):
    keyboard = buttons.moving_masters_buttons(index, end_index,
                                              masters[int(index)].user_id, masters[int(index)].placement_id)
    try:
        img = open(data_path + masters[int(index)].user_id + '\\profile\\profile.jpg', 'rb')
    except Exception as ex:
        print(ex)
        img = open(data_path + 'default.jpeg', 'rb')
    bot.send_photo(user_id, photo=img,
                   caption=f"`Ім'я:` {masters[int(index)].name} \n\n"
                           f"`Опис: ` {masters[int(index)].details} \n\n"
                           f"`Рейтинг: `" + "⭐️" * int(get_point(masters[int(index)].user_id))
                           + "\n\n", reply_markup=keyboard,
                   parse_mode='markdown')


def set_start_time(message, date):
    if not re.match(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', message.text):
        bot.send_message(message.chat.id, 'Невірний формат часу, спробуйте ще раз. '
                                          '(Приклад: 9:00, 14:20)')
        bot.register_next_step_handler(message=message, date=date, callback=set_start_time)
        return
    bot.send_message(message.chat.id, 'Напишіть час кінця вільного тайм слоту. '
                                      '(Приклад: 9:00, 14:20): ')
    bot.register_next_step_handler(message=message, start_time=message.text,
                                   date=date, callback=set_end_time)
    return


def set_end_time(message, start_time, date):
    if not re.match(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', message.text):
        bot.send_message(message.chat.id, 'Невірний формат часу, спробуйте ще раз. '
                                          '(Приклад: 9:00, 14:20)')
        bot.register_next_step_handler(message=message, date=date, callback=set_end_time)
        return
    try:
        create_time_slot(user_id=message.from_user.id, start_time=start_time,
                         end_time=message.text, date=date)
    except Exception as ex:
        print(ex)
        return
    keyboard = buttons.to_menu()
    bot.send_message(message.from_user.id, 'Додано!', reply_markup=keyboard)
    return


bot.enable_save_next_step_handlers(delay=2)


# bot.load_next_step_handlers()


def check_start_ud_data():
    cities = get_cities()
    if cities.__len__() < 1:
        os.system('mysqlsh -uroot -fdata.sql')
    else:
        return


if __name__ == '__main__':
    # while True:
    #     try:
    check_start_ud_data()
    bot.polling(none_stop=True)
    # except Exception as e:
    #     print(e)
    #     time.sleep(10)
