import random
import re
from methods import *
import os
import telebot
import time
import logging
import calculations
import schedule
from config import token
from multiprocessing import Process


bot = telebot.TeleBot(token=token)
data_path = os.curdir + '\\data\\'
# try:
#     schedule.every().day.at('01:59').do(daily_update)
# except Exception as exc:
#     print(exc)
#     time.sleep(5)


schedule.every().day.at('11:30').do(daily_update)
# try:
#     schedule.every().monday.at('02:09').do(weekly_update)
# except Exception as exc:
#     print(exc)
#     time.sleep(5)

schedule.every().monday.at('01:10').do(weekly_update)

@bot.message_handler(commands=['send_to_everyone'])
def mailing(message):
    if not is_super_admin(message.from_user.id):
        return

    bot.send_message(message.from_user.id, f"Что рассылать:")
    users = get_all_users()
    bot.register_next_step_handler(message, send_to_everyone, users)


@bot.message_handler(commands=['send_to_masters'])
def mailing(message):
    if not is_super_admin(message.from_user.id):
        return

    bot.send_message(message.from_user.id, f"Что рассылать:")
    users = get_all_masters()
    bot.register_next_step_handler(message, send_to_everyone, users)


@bot.message_handler(commands=['send_to_clients'])
def mailing(message):
    if not is_super_admin(message.from_user.id):
        return

    bot.send_message(message.from_user.id, f"Что рассылать:")
    users = get_all_clients()
    bot.register_next_step_handler(message, send_to_everyone, users)


@bot.message_handler(commands=['send_to_admins'])
def mailing(message):
    if not is_super_admin(message.from_user.id):
        return

    bot.send_message(message.from_user.id, f"Что рассылать:")
    users = get_all_admins()
    bot.register_next_step_handler(message, send_to_everyone, users)


@bot.message_handler(commands=['daily_update'])
def d_update(message):
    if not is_super_admin(message.from_user.id):
        return
    try:
        daily_update()
    except Exception as e:
        print(e)
        bot.send_message(message.from_user.id, 'Не проапдейтилось...')
        return

    with open(data_path + 'done.jpg', 'rb') as done_pic:
        bot.send_photo(message.from_user.id, photo=done_pic)

    return


@bot.message_handler(commands=['weekly_update'])
def w_update(message):
    if not is_super_admin(message.from_user.id):
        return

    try:
        weekly_update()
    except Exception as ex:
        print(ex)
        bot.send_message(message.from_user.id, 'Не проапдейтилось...')
        return

    with open(data_path + 'done.jpg', 'rb') as done_pic:
        bot.send_photo(message.from_user.id, photo=done_pic)

    return


@bot.message_handler(commands=['get_last_update'])
def get_update(message):
    if not is_super_admin(message.from_user.id):
        return
    instance = get_last_update()
    if instance.__len__() < 1:
        bot.send_message(message.from_user.id, "Не вдалося виконати запит...")
        return
    else:
        bot.send_message(message.from_user.id, f"Дата: {instance[0].date} \n"
                                               f"Тип апдейту: {'daily' if instance[0].daily else 'weekly'} \n"
                                               f"Виконано: {'Так' if instance[0].done else 'Ні'}")
        return


@bot.message_handler(commands=['help'])
def bot_help(message):
    if is_super_admin(message.from_user.id):
        bot.send_message(message.from_user.id,
                         "У Вас є права адміна.\n "
                         "Що Ви можете: \n"
                         "/get_last_update - отримати інформацію про останній апдейт\n"
                         "/send_to_everyone - розсилка повідомлень всім, підтримуються лише текстові повідомленя та фотографії\n"
                         "/send_to_clients - розсилка повідомлень клієнтам, підтримуються лише текстові повідомленя та фотографії\n"
                         "/send_to_masters - розсилка повідомлень майстрам, підтримуються лише текстові повідомленя та фотографії\n"
                         "/send_to_admins - розсилка повідомлень адмінам, підтримуються лише текстові повідомленя та фотографії\n"
                         "/daily_update - апдейт бази даних (всі заяки, які не були виконані, стануть неактивними)\n"
                         "/weekly_update - апдейт бази даних (зміщення тиждня на 1 вперед)\n\n"
                         "* ці апдейти виконуються системою автоматично, але якщо трипились якісь негаразди - їх "
                         "потрібно виконати вручну\n\n"
                         "Всі питання та пропозиції сюди - @fjskdb (Артём)"
                         )
    else:
        bot.send_message(message.from_user.id,
                         "Якщо Ви не зареєстровані:\n"
                         "▫️ натисніть /start \n"
                         "▫️ з'явиться кнопка реєстрації, натисніть на її\n"
                         "▫️ оберіть роль (якщо Ви працюєте майстром, то оберіть 'майстер', якщо хочете отримати послугу"
                         " - оберіть 'клієнт'\n"
                         "▫️ слідкуйте за інструкціями, які Вам надасть бот\n\n"
                         "Якщо ви вже зареєстровані:\n"
                         "▫️ натисніть на кнопку Головне меню, яка є на вашій клавіатурі, щоб перейти до меню\n"
                         "Якщо її немає:\n"
                         "▫️ натисніть /start\n"
                         "▫️ з'явиться кнопка меню, натисніть на її\n\n"
                         "Як замовити послугу:\n"
                         "▫️ переходите до меню\n"
                         "▫️ натискаєте 'Записатись на процедуру'\n"
                         "▫️ обираєте салон\n"
                         "▫️ обираєте майстра\n"
                         "▫️ на вікні майстра натискаєте кнопку 'Обрати послугу'\n"
                         "▫️ обираєте сегмент послуг, який хочете отримати\n"
                         "▫️ обираєте послугу\n"
                         "▫️ виводится деталі про послугу, якщо Ви з всім згодні, то натискайте 'Далі', якщо ні - 'Повернутися'\n"
                         "▫️ обираєте тиждень, доступні лише поточний та наступний тиждні\n"
                         "▫️ обираєте день\n"
                         "▫️ обирайте час, можна обрати з запропонованого, або ж спробувати задати свій, якщо майстер"
                         "вільний у цей час - Вас запише.\n"
                         "▫️ слідкуйте на інструкціями\n"
                         "▫️ після створеня заявки, Ви можете переглянути, у google календарі буде відмітка з Вашою послугою"
                         " (якщо ви вказали пошту gmail)\n\n"
                         "Всі питання та пропозиції сюди - @fjskdb (Артём)"
                         )


def send_to_everyone(message, users):
    if message.content_type == 'text':

        for user_id in users:

            if user_id != str(message.from_user.id):
                try:
                    bot.send_message(user_id, message.text)
                except Exception as ex:
                    print(ex)

    elif message.content_type == 'photo':

        for user_id in users:

            if user_id != str(message.from_user.id):
                try:
                    bot.send_photo(user_id, get_photo(message), caption=message.caption)
                except Exception as ex:
                    print(ex)

    else:
        bot.send_message(message.from_user.id, "Тип данных не поддерживается. "
                                               "Можно рассылать только тект либо картинки")
        return

    with open(data_path + 'done.jpg', 'rb') as done_pic:
        bot.send_photo(message.from_user.id, photo=done_pic)
    return


@bot.message_handler(commands=['admin'])
def show_admin_contacts(message):
    bot.send_message(message.from_user.id, 'писатель энтого бота - @fjskdb')


@bot.message_handler(commands=['start'])
def start(message):
    bot.clear_step_handler_by_chat_id(message.from_user.id)

    try:
        flag = check_user(message.from_user.id)
    except Exception as ex:
        session.rollback()
        logging.error(f'Could not check user. Cause: {ex}. Time: {time.asctime()}')
        return

    # keyboard = buttons.choose_language_buttons()
    # bot.send_message(message.from_user.id, 'Обери мову/Choose a language', reply_markup=keyboard)

    greetings = ('Привіт, мене звуть Лола! 💁‍♀️\n\n'
                 '🤖 Я робот і буду виконувати роль твого'
                 ' персонального менеджера. \n\n')

    if flag:
        keyboard = buttons.choose_role_button_menu()
    else:
        keyboard = buttons.choose_role_button_reg()
        greetings += 'Але перед початком треба  зареєструватись👇🏻'

    bot.send_message(message.from_user.id, greetings,
                     reply_markup=keyboard)


@bot.message_handler(regexp='^(Головне меню)')
def menu(message):
    bot.clear_step_handler_by_chat_id(message.from_user.id)
    try:
        flag = check_user(message.from_user.id)
    except Exception as ex:
        session.rollback()
        logging.error(f'Could not check user. Cause: {ex}. Time: {time.asctime()}')
        return
    if not flag:
        return
    else:
        to_menu(message.from_user.id)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    bot.clear_step_handler_by_chat_id(call.from_user.id)

    try:
        flag = check_user(call.from_user.id)
    except Exception as ex:
        session.rollback()
        logging.error(f'Could not check user. Cause: {ex}. Time: {time.asctime()}')
        return

    if 'registration' in call.data:
        bot.delete_message(call.from_user.id, call.message.message_id)
        data = call.data.split(' ')
        if flag:
            bot.send_message(call.from_user.id, 'Ви вже зареєстровані!')
            to_menu(call.from_user.id)
            bot.answer_callback_query(call.id, text=" ", show_alert=False)
            return
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
        bot.delete_message(call.from_user.id, call.message.message_id)
        data = call.data.split(' ')
        try:
            user_instance = get_user_role(call.from_user.id)
        except Exception as ex:
            logging.error(f'Could not get current role. Cause: {ex}. Time: {time.asctime()}')
            return

        if data[1] == '1':
            if user_instance:
                try:
                    set_current_role(call.from_user.id, 1)
                except Exception as ex:
                    logging.error(f'Could not set current role. Cause: {ex}. Time: {time.asctime()}')
                    session.rollback()
                    return
                to_menu(call.from_user.id)
                bot.answer_callback_query(call.id, text=" ", show_alert=False)
                return
            else:
                keyboard = buttons.reg_as_master()
                bot.send_message(call.from_user.id, 'Ви не зареєстровані як майстер. Бажаєте зареєструватися?',
                                 reply_markup=keyboard)
            return
        else:
            try:
                set_current_role(call.from_user.id, 0)
            except Exception as ex:
                logging.error(f'Could not set current role. Cause: {ex}. Time: {time.asctime()}')
                session.rollback()
                return
            to_menu(call.from_user.id)
            bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return

    elif 'set_placement' in call.data:
        bot.delete_message(call.from_user.id, call.message.message_id)
        data = call.data.split(' ')
        try:
            update_placement(call.from_user.id, data[1])
        except Exception as ex:
            logging.error(f'Could not update placement. Cause: {ex}. Time: {time.asctime()}')
            session.rollback()
            return
        bot.send_message(call.from_user.id, 'Місце роботи додано', reply_markup=buttons.keyboard_menu_button())
        if data[2] == 'reg':
            set_current_role(call.from_user.id, True)
            # keyboard = buttons.to_menu()
            add_new_service(call, True)
            # bot.send_message(call.from_user.id, "Супер! Тепер ви зареєстровані і до вас вже можна записуватись 🥳",
            #                  reply_markup=keyboard)
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
        to_menu(call.from_user.id)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)

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
        try:
            update_city(call.from_user.id, data[1], data[2])
        except Exception as ex:
            logging.error(f'Could not set city. Cause: {ex}. Time: {time.asctime()}')
            session.rollback()
            return
        try:
            city = get_city_by_id(data[1])
        except Exception as ex:
            logging.error(f'Could not get city. Cause: {ex}. Time: {time.asctime()}')
            return
        bot.send_message(call.from_user.id, f'Ви обрали місто: {city}🌆')

        if data[3] == 'reg':
            if data[2] == 'master':
                update_to_master(call.from_user.id)
                master_reg_start(call.message, call.from_user.id)
                bot.answer_callback_query(call.id, text=" ", show_alert=False)
                return
            else:
                # keyboard = buttons.to_menu()
                bot.send_message(call.from_user.id, "Супер! Тепер ви зареєстровані 🥳",
                                 reply_markup=buttons.keyboard_menu_button())
                bot.answer_callback_query(call.id, text=" ", show_alert=False)
                return
        else:
            edit_profile(call.from_user.id, data[2])
            bot.answer_callback_query(call.id, text=" ", show_alert=False)
            return

    elif call.data == 'check_profile':
        try:
            if get_user_role(call.from_user.id):
                show_profile(call.from_user.id, 'master')
            else:
                show_profile(call.from_user.id, 'client')
            bot.answer_callback_query(call.id, text=" ", show_alert=False)
        except Exception as ex:
            logging.error(f'Could not show profile. Cause: {ex}. Time: {time.asctime()}')
            return
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
            bot.answer_callback_query(call.id, text="На жаль, сертифікати не завантажені  :(!")
            return

        index = 0
        try:
            show_certificates(index, end_index, certificates, call.from_user.id)
        except Exception as ex:
            logging.error(f'Could not show certificates. Cause: {ex}. Time: {time.asctime()}')
            return
        bot.answer_callback_query(call.id, text=" ", show_alert=False)

    elif 'move_certificate' in call.data:
        indexes = call.data.split(' ')
        bot.delete_message(call.from_user.id, call.message.message_id)
        certificates = get_certificates(indexes[3])
        try:
            show_certificates(indexes[1], indexes[2], certificates, call.from_user.id)
        except Exception as ex:
            logging.error(f'Could not show certificates. Cause: {ex}. Time: {time.asctime()}')
            return
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return

    elif 'check_sample_services' in call.data:
        data = call.data.split(' ')
        services = get_sample_services(data[1])
        end_index = services.__len__() - 1

        if end_index == -1:
            bot.answer_callback_query(call.id, text="На жаль, роботи не завантажені  :(!")
            return

        index = 0
        try:
            show_services(index, end_index, services, call.from_user.id)
        except Exception as ex:
            logging.error(f'Could not show services. Cause: {ex}. Time: {time.asctime()}')
            return
        bot.answer_callback_query(call.id, text=" ", show_alert=False)

    elif 'move_services' in call.data:
        indexes = call.data.split(' ')
        bot.delete_message(call.from_user.id, call.message.message_id)
        services = get_sample_services(indexes[3])
        try:
            show_services(indexes[1], indexes[2], services, call.from_user.id)
        except Exception as ex:
            logging.error(f'Could not show services. Cause: {ex}. Time: {time.asctime()}')
            return
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return

    elif call.data == 'reg_as_master':
        move_user(call.from_user.id)
        master_reg_start(call.message, call.from_user.id)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return

    elif 'order_1' in call.data:
        data = call.data.split(' ')
        try:

            if data[1] == 'client':
                user_instance = get_client(call.from_user.id)
            else:
                user_instance = get_master(call.from_user.id)

        except Exception as ex:
            logging.error(f'Could not get user instance. Cause: {ex}. Time: {time.asctime()}')
            return
        keyboard = buttons.order_placement_buttons(user_instance[0].city_id)
        bot.send_message(call.from_user.id, keyboard[0],
                         reply_markup=keyboard[1])
        bot.answer_callback_query(call.id, text=' ', show_alert=False)

    elif 'order_placement' in call.data:
        data = call.data.split(' ')
        try:
            masters = get_masters(data[1])
        except Exception as ex:
            logging.error(f'Could not get masters. Cause: {ex}. Time: {time.asctime()}')
            return
        end_index = masters.__len__() - 1

        if end_index == -1:
            bot.answer_callback_query(call.id, text="На жаль, у даному салоні майстри ще не зареєестровані :(")
            return

        bot.send_message(call.from_user.id, '<<<<<< А зараз оберіть майстра >>>>>>', reply_markup=buttons.keyboard_menu_button())
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        index = 0
        try:
            show_masters(index, end_index, masters, call.from_user.id)
        except Exception as ex:
            logging.error(f'Could not show masters. Cause: {ex}. Time: {time.asctime()}')
            return

    elif 'move_masters' in call.data:
        bot.delete_message(call.from_user.id, call.message.message_id)
        indexes = call.data.split(' ')
        masters = get_masters(indexes[3])
        try:
            show_masters(indexes[1], indexes[2], masters, call.from_user.id)
        except Exception as ex:
            logging.error(f'Could not show masters. Cause: {ex}. Time: {time.asctime()}')
            return
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return

    elif 'del_message' in call.data:
        bot.delete_message(call.from_user.id, call.message.message_id)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)

    elif 'add_to_favorite' in call.data:
        data = call.data.split(' ')

        if str(data[1]) != str(call.from_user.id):
            try:
                flag = check_saved_masters(master_id=data[1], user_id=call.from_user.id)
            except Exception as ex:
                logging.error(f'Could not check saved masters. Cause: {ex}. Time: {time.asctime()}')
                return
            if flag:
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
        try:
            reservation = data[3]
        except Exception as ex:
            print(ex)
            reservation = None
        keyboard = buttons.service_segments(data[1], False, call.from_user.id, reservation, check=data[2])
        bot.send_message(call.from_user.id, 'Оберіть сегмент послуг 🧚🏻‍',
                         reply_markup=keyboard)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)

    elif 'order_service' in call.data:
        data = call.data.split(' ')

        if data[1] == '4':
            bot.send_message(call.from_user.id, "Напишіть час перерви. "
                                                "(Наприклад 10-00-11-00)")
            bot.register_next_step_handler(call.message, take_brake, call)
            bot.answer_callback_query(call.id, text=" ", show_alert=False)
            return
        keyboard = buttons.get_services(data[2], call.from_user.id, data[1], data[3], check=data[4])

        if keyboard is None:
            bot.answer_callback_query(call.id, text="Майстер не надає цей тип послуг")
            bot.answer_callback_query(call.id, text=" ", show_alert=False)
            return

        if (str(call.from_user.id) is str(data[2])) and (data[3] != 'reservation') and (data[4] == 'check'):
            segment_text = 'Уточніть процедуру 🗂' if keyboard[1] is not None else \
                'Послуги для цієї категорії не визначені. ' \
                'Зверніться до адміністратора для того, щоб додати список послуг'
            bot.send_message(call.from_user.id, segment_text,
                             reply_markup=keyboard[1])
        else:
            bot.send_message(call.from_user.id, keyboard[0],
                             reply_markup=keyboard[1])

        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return

    elif 'add_service' in call.data:
        # data = call.data.split(' ')
        add_new_service(call)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)

    elif 'service_segment' in call.data:
        data = call.data.split(' ')
        try:
            services_name = get_service_names(call.from_user.id, data[1])
        except Exception as ex:
            logging.error(f'Could not get service names. Cause: {ex}. Time: {time.asctime()}')
            return
        keyboard = buttons.service_buttons(data[1], services_name)
        segment_text = 'Уточніть процедуру 🗂' if keyboard[1] else \
            'Послуги для цієї категорії не визначені. ' \
            'Зверніться до адміністратора для того, щоб додати список послуг'
        bot.send_message(call.from_user.id, segment_text,
                         reply_markup=keyboard[0])
        bot.answer_callback_query(call.id, text=" ", show_alert=False)

    elif 'add_instance' in call.data:
        data = call.data.split(' ')
        service = data[1]
        segment = data[2]

        if data.__len__() == 4:
            service = data[1] + ' ' + data[2]
            segment = data[3]

        try:
            service_id = create_service(call.from_user.id, str(service), str(segment))
        except Exception as ex:
            logging.error(f'Could not create service. Cause: {ex}. Time: {time.asctime()}')
            session.rollback()
            return
        bot.delete_message(call.from_user.id, call.message.message_id)
        bot.send_message(call.from_user.id, service + ':')
        bot.send_message(call.from_user.id, '💵 Яка вартість процедури?')
        bot.register_next_step_handler(message=call.message, service_id=service_id, segment=segment,
                                       callback=set_money_cost, reg='reg')
        bot.answer_callback_query(call.id, text=" ", show_alert=False)

    elif 'sav_masters' in call.data:
        data = call.data.split(' ')
        try:
            masters = get_master_by_id(data[1])
        except Exception as ex:
            logging.error(f'Could not get masters. Cause: {ex}. Time: {time.asctime()}')
            session.rollback()
            return
        show_masters(0, 0, masters, call.from_user.id, True, call.message.message_id + 1)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)

    elif 'choose_service ' in call.data:
        data = call.data.split(' ')
        if data[3] == 'not_confirmed':
            user_confirmation(call, data[1], data[2], data[4])
        elif data[3] == 'confirmed':
            bot.delete_message(call.from_user.id, call.message.message_id)
            keyboard = buttons.choose_week(data[1], data[2], data[4])
            bot.send_message(call.from_user.id, "Оберіть тиждень, на який хочете записатися🗓:", reply_markup=keyboard)

        bot.answer_callback_query(call.id, text=" ", show_alert=False)

    elif 'choose_week' in call.data:
        data = call.data.split(' ')
        show_working_days(call, data[1], data[2], data[3], data[4])
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return

    elif 'set_working_days' in call.data:
        data = call.data.split(' ')
        set_working_days(call, False, data[1])
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return
    elif 'add_working_day' in call.data:
        data = call.data.split(' ')
        create_working_day(call.from_user.id, data[1])
        set_working_days(call, True, data[2])
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return
    elif call.data == 'pre_check_order':
        keyboard = buttons.client_check_order_buttons()
        bot.send_message(call.from_user.id, 'Оберіть опцію', reply_markup=keyboard)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)

    elif 'check_order_client' in call.data:
        data = call.data.split(' ')
        try:
            orders = get_orders_for_client(call.from_user.id, data[1])
        except Exception as ex:
            logging.error(f'Could not get orders for client. Cause: {ex}. Time: {time.asctime()}')
            return
        if orders.__len__() < 1:
            bot.answer_callback_query(call.id, text="Замовлення не знайдені")
            return
        try:
            show_orders(orders, call.from_user.id, False, call)
        except Exception as ex:
            logging.error(f'Could not show orders. Cause: {ex}')
            return
        bot.answer_callback_query(call.id, text=" ", show_alert=False)

    elif 'check_order_master' in call.data:
        data = call.data.split(' ')
        try:
            orders = get_orders_for_master(call.from_user.id, data[1])
        except Exception as ex:
            logging.error(f'Could not get orders for master. Cause: {ex}. Time: {time.asctime()}')
            return
        if orders.__len__() < 1:
            bot.answer_callback_query(call.id, text="Замовлення не знайдені")
            return
        try:
            show_orders(orders, call.from_user.id, True, call)
        except Exception as ex:
            logging.error(f'Could not show orders. Cause: {ex}. Time: {time.asctime()}')
            return
        bot.answer_callback_query(call.id, text=" ", show_alert=False)

    elif 'mark_as_done' in call.data:
        data = call.data.split(' ')
        try:
            bot.delete_message(call.from_user.id, int(data[2]))
        except Exception as ex:
            print(ex)
        try:
            order = update_order_as_done(data[1])
        except Exception as ex:
            logging.error(f'Could not update order as completed. Cause: {ex}. Time: {time.asctime()}')
            session.rollback()
            return
        if str(call.from_user.id) != order.client_id_master_acc and str(call.from_user.id) != order.client_id:
            service = get_service_by_id(order.service_id)
            bot.send_message(int(order.client_id) if order.client_id is not None else int(order.client_id_master_acc),
                             f'Ваше замовленя №{order.id} - {service[0].name}, було відмічено майстром як виконане. Ви '
                             'можете оцінити якість роботи майстра у розділі Мої записи -> Виконані замовлення.\n\nЯкщо'
                             ' ви не отримали цю послугу, напишіть, будь ласка, адміністрітору. Щоб отримати контактні '
                             'дані адміністратора, скористуйтеся /admin')
        bot.answer_callback_query(call.id, text="Відмічено!")

    elif 'mark_as_canceled_by_master' in call.data:
        data = call.data.split(' ')
        try:
            bot.delete_message(call.from_user.id, data[2])
        except Exception as ex:
            print(ex)
        try:
            order = update_order_as_canceled_by_master(data[1])
        except Exception as ex:
            logging.error(f'Could not update order as canceled by master. Cause: {ex}. Time: {time.asctime()}')
            session.rollback()
            return
        try:
            master = get_master(order.master_id)
            service = get_service_by_id(order.service_id)
        except Exception as ex:
            print(ex)
            logging.error(f'Could not get order, master, service data. Cause: {ex}. Time: {time.asctime()}')
            return
        start_time = order.time.split('-')
        prepaid = 'Так' if order.prepaid else 'Ні'
        if order.client_id is None:
            if order.client_id_master_acc == str(call.from_user.id):
                pass
            else:
                bot.send_message(order.client_id_master_acc, f'Ваше бронювання було відмінено майстром '
                                                             f'{time.localtime().tm_hour}:{time.localtime().tm_min} '
                                                             f'{time.localtime().tm_mon}.{time.localtime().tm_mday} \n'
                                                             f"Ім`я майстра: {master[0].name} \n"
                                                             f"Телеграм майстра: {master[0].username} \n"
                                                             f"Назва процедури: {service[0].name} \n"
                                                             f"Час початку: {start_time[0]}-{start_time[1]} \n"
                                                             f"Передплачено: {prepaid} \n\n\n"
                                                             f"***Якщо процедура передплачена, зверніться ---, щоб "
                                                             f"вам повернули кошти")
        else:
            if order.client_id == str(call.from_user.id):
                pass
            else:
                bot.send_message(order.client_id, f'Ваше бронювання була відмінена майстром '
                                                  f'{time.localtime().tm_hour}:{time.localtime().tm_min} '
                                                  f'{time.localtime().tm_mon}.{time.localtime().tm_mday} \n'
                                                  f"Ім'я майстра: {master[0].name} \n"
                                                  f"Телеграм майстра: {master[0].username} \n"
                                                  f"Назва процедури: {service.name} \n"
                                                  f"Час початку: {start_time[0]}-{start_time[1]} \n"
                                                  f"Передплачено: {prepaid} \n\n\n"
                                                  f"***Якщо процедура передплачена, зверніться ---, щоб "
                                                  f"вам повернули кошти")
        bot.answer_callback_query(call.id, text="Відхилено!")

    elif 'mark_as_canceled_by_client' in call.data:
        data = call.data.split(' ')
        try:
            bot.delete_message(call.from_user.id, data[2])
        except Exception as ex:
            print(ex)

        try:
            order = update_order_as_canceled_by_client(data[1])
        except Exception as ex:
            logging.error(f'Could not update order as canceled by master. Cause: {ex}. Time: {time.asctime()}')
            session.rollback()
            return

        prepaid = 'Так' if order.prepaid else 'Ні'

        if order.master_id == str(call.from_user.id):
            pass
        else:
            bot.send_message(order.master_id, f'Замовлення №{order.id} було відмінене клієнтом \n'
                                              f'Передплачено: {prepaid}')
            if order.prepaid:
                if order.client_id is None:
                    bot.send_message(order.client_id_master_acc, 'У Вас була здійснена передплата.'
                                                                 'Зверніться, будь ласка, до адміністратора, '
                                                                 f'щоб повернути гроші. Номер замовлення № {order.id}')
                else:
                    bot.send_message(order.client_id, 'У Вас була здійснена передплата.'
                                                      'Зверніться, будь ласка, до адміністратора, '
                                                      f'щоб повернути гроші. Номер замовлення № {order.id}')
        bot.answer_callback_query(call.id, text="Відхилено!")

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
            bot.register_next_step_handler(message=call.message, callback=edit_name, role=data[2])

        elif data[1] == 'phone':
            bot.send_message(call.from_user.id, "Тепер надішліть свій телефон ☎️",
                             reply_markup=buttons.send_contact())
            bot.register_next_step_handler(message=call.message, callback=edit_telephone, role=data[2])

        elif data[1] == 'tg_link':
            try:
                update_user_name(call.from_user.id, call.from_user.username, role=data[2])
            except Exception as ex:
                logging.error(f'Could not update username. Cause: {ex}. Time: {time.asctime()}')
                session.rollback()
                return

        elif data[1] == 'placement':
            user_instance = get_master(call.from_user.id)
            data = buttons.set_placement_buttons(user_instance[0].city_id, '')
            bot.send_message(call.from_user.id, data[0],
                             reply_markup=data[1])

        elif data[1] == 'edit_city':
            keyboard = buttons.city_buttons(data[2], '1')
            bot.send_message(call.from_user.id, "Оберіть Ваше місто🌆:", reply_markup=keyboard)

        elif data[1] == 'details':
            bot.send_message(call.from_user.id, 'Напишіть опис до аккаунту, '
                                                'що ви вмієте і тд.')
            bot.register_next_step_handler(message=call.message, callback=edit_details)

        elif data[1] == 'photo':
            bot.send_message(call.from_user.id, 'Відправте мені ваше фото')
            bot.register_next_step_handler(message=call.message, reg='', callback=set_acc_photo)

        elif data[1] == 'edit_email':
            bot.send_message(call.from_user.id, 'Вкажіть діючу пошту✉')
            bot.register_next_step_handler(call.message, set_email, data[2], None)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return

    elif 'remove_saved' in call.data:
        data = call.data.split(' ')
        try:
            delete_from_favorites(data[1], call.from_user.id)
        except Exception as ex:
            logging.error(f'Could not delete master from favorites. Cause {ex}')
            session.rollback()
            return
        try:
            bot.delete_message(call.from_user.id, int(data[2]))
            keyboard = buttons.saved_masters(call.from_user.id)
            if keyboard is None:
                bot.delete_message(call.from_user.id, int(data[2]) - 1)
            else:
                bot.edit_message_reply_markup(call.from_user.id, int(data[2]) - 1, reply_markup=keyboard)
        except Exception as ex:
            logging.error(f'Callback handler: remove_saved. Cause: {ex}')
            bot.answer_callback_query(call.id, text=" ", show_alert=False)
            return
        bot.answer_callback_query(call.id, text="Видалено(")
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
            logging.error(f'Could not delete service. Cause: {ex}. Time: {time.asctime()}')
            session.rollback()
            bot.answer_callback_query(call.id, text="Виникла помилка!")
            return
        keyboard = buttons.service_segments(call.from_user.id, False, call.from_user.id, check='check')
        bot.send_message(call.from_user.id, 'Оберіть сегмент послуг 🧚🏻‍',
                         reply_markup=keyboard)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return

    elif 'edit_sample_services' in call.data:
        data = call.data.split(' ')
        try:
            edit_sample_service(data[1], call.from_user.id)
        except Exception as ex:
            logging.error(f'Could not edit sample service. Cause: {ex}. Time: {time.asctime()}')
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
            logging.error(f'Could not delete sample service. Cause: {ex}. Time: {time.asctime()}')
            session.rollback()
            bot.answer_callback_query(call.id, text="Виникла помилка!")
            return
        services = get_sample_services(call.from_user.id)
        end_index = services.__len__() - 1

        if end_index == -1:
            to_menu(call.from_user.id)
            bot.answer_callback_query(call.id, text=" ", show_alert=False)
            return

        index = 0
        try:
            show_services(index, end_index, services, call.from_user.id)
        except Exception as ex:
            logging.error(f'Could not show services. Cause: {ex}. Time: {time.asctime()}')
            return
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return

    elif 'edit_certificate' in call.data:
        data = call.data.split(' ')
        try:
            edit_certificate(data[1], call.from_user.id)
        except Exception as ex:
            logging.error(f'Could not edit certificate. Cause: {ex}. Time: {time.asctime()}')
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
            logging.error(f'Could not delete certificate. Cause: {ex}. Time: {time.asctime()}')
            session.rollback()
            bot.answer_callback_query(call.id, text="Виникла помилка!")
            return
        certificates = get_certificates(call.from_user.id)
        end_index = certificates.__len__() - 1

        if end_index == -1:
            to_menu(call.from_user.id)
            bot.answer_callback_query(call.id, text=" ", show_alert=False)
            return

        index = 0
        try:
            show_certificates(index, end_index, certificates, call.from_user.id)
        except Exception as ex:
            logging.error(f'Could not show certificates. Cause: {ex}. Time: {time.asctime()}')
            return
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return

    elif 'send_rating' in call.data:
        data = call.data.split(' ')
        keyboard = buttons.set_rating_buttons(data[1])
        bot.send_message(call.from_user.id, 'Оцініть роботу майстра 🤩', reply_markup=keyboard)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return

    elif 'set_rating' in call.data:
        keyboard = buttons.to_completed_services()
        bot.delete_message(call.from_user.id, call.message.message_id)
        data = call.data.split(' ')
        response = create_rating(master_id=data[2], client_id=call.from_user.id, point=int(data[1]))

        if response is None:
            bot.send_message(call.from_user.id, 'Ви вже оцінювали цього майстра!', reply_markup=keyboard)
        else:
            bot.send_message(call.from_user.id, 'Дякую за вігук ☺', reply_markup=keyboard)

        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return

    elif 'send_feedback' in call.data:
        data = call.data.split(' ')
        try:
            flag = check_feedback(call.from_user.id, data[1])
        except Exception as ex:
            logging.error(f'Could not check feedback. Cause: {ex}. Time: {time.asctime()}')
            return

        if flag:
            bot.send_message(call.from_user.id, 'Напишіть відгук про майстра *повідомлення не повинно містити'
                                                ' емодзі')
            bot.register_next_step_handler(call.message, set_feedback, call.from_user.id, data[1], call)
        else:
            bot.answer_callback_query(call.id, text="Ви вже написали відгук про цього майстра")
            return

        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return

    elif call.data == 'del_than_menu':
        bot.delete_message(call.from_user.id, call.message.message_id)
        to_menu(call.from_user.id)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)

    elif call.data == 'set_working_time':
        bot.send_message(call.from_user.id,
                         'Напишіть години, коли Ви працюєте. Наприклад,'
                         ' 9-00-18-00, де \n 9-00 - початок робочого дня, 18-00'
                         ' закінчення. Ці години будуть застосовані для'
                         ' всіх робочих днів. В меню "Налаштувати робочий час"'
                         ' Ви завжди можете змінити час для кожного дня'
                         ' окремо.')
        bot.register_next_step_handler(call.message, set_working_time, call)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)

    elif 'edit_working_day' in call.data:
        data = call.data.split(' ')

        if data[1] == 'start':
            keyboard = buttons.edit_working_day(data[2])
            bot.send_message(call.from_user.id, 'Оберіть, що хочете змінити⚙',
                             reply_markup=keyboard)
            bot.answer_callback_query(call.id, text=" ", show_alert=False)
            return

        elif data[1] == 'update_time':
            bot.send_message(call.from_user.id,
                             'Напишіть години, коли Ви працюєте. Наприклад,'
                             ' 9-00-18-00, де \n 9-00 - початок робочого дня, 18-00'
                             ' закінчення.')
            bot.register_next_step_handler(call.message, update_time, data[2], call)
            bot.answer_callback_query(call.id, text=" ", show_alert=False)
            return

        elif data[1] == 'set_non_active':
            try:
                days_next_week = get_day_details(data[2], '1')
                days_cur_week = get_day_details(data[2])
                if days_next_week[1].__len__() > 1 or days_cur_week[1].__len__() > 1:
                    bot.send_message(call.from_user.id, 'На цей день є записи, ви не можете зробити його неактивник.'
                                                        ' Спершу відмініть всі записи!')
                else:
                    response = edit_day(data[2], non_active=True)
                    if response is None:
                        logging.error('edit_day method: unknown option')
                        return
            except Exception as ex:
                logging.error(f'Could not update working hours. Cause: {ex}. Time: {time.asctime()}')
                return

            set_working_days(call, False, 'show')
            bot.answer_callback_query(call.id, text=" ", show_alert=False)
            return

        elif data[1] == 'set_active':
            try:
                response = edit_day(data[2], active=True)
            except Exception as ex:
                logging.error(f'Could not update working hours. Cause: {ex}. Time: {time.asctime()}')
                return

            if response is None:
                logging.error('edit_day method: unknown option')

            set_working_days(call, False, 'show')
            bot.answer_callback_query(call.id, text=" ", show_alert=False)
            return

    elif 'show_certificates_settings' in call.data:
        data = call.data.split(' ')
        keyboard = buttons.show_certificates(data[1])
        bot.send_message(call.from_user.id, '<<<<<< Меню сертифікатів: >>>>>>', reply_markup=keyboard)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return

    elif 'show_sample_services_settings' in call.data:
        data = call.data.split(' ')
        keyboard = buttons.show_sample_services(data[1])
        bot.send_message(call.from_user.id, '<<<<<< Меню прикладів робіт: >>>>>>', reply_markup=keyboard)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return

    elif 'show_services_settings' in call.data:
        data = call.data.split(' ')
        keyboard = buttons.show_service(data[1])
        bot.send_message(call.from_user.id, '<<<<<< Меню послуг: >>>>>>', reply_markup=keyboard)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return

    elif call.data == 'show_orders_master':
        keyboard = buttons.check_order_menu()
        bot.send_message(call.from_user.id, '<<<<<< Меню записів: >>>>>>', reply_markup=keyboard)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return

    elif 'reserve_day' in call.data:
        data = call.data.split(' ')
        try:
            day_det = get_day_details(data[1], data[5])
            service_det = get_service_by_id(data[3])
        except Exception as ex:
            logging.error(f'Could not get day details or service by id. Cause: {ex}. Time {time.asctime()}')
            return

        if data[4] == 'True':
            bot.delete_message(call.from_user.id, call.message.message_id)
            bot.send_message(call.from_user.id,
                             'Напишіть час, на який '
                             'хочете записатися (формат: 13-00)')
            print(data)
            bot.register_next_step_handler(call.message, get_time_slots, day_det, service_det, data[1], data[2],
                                           data[3], data[5], data[6], call)
            bot.answer_callback_query(call.id, text=" ", show_alert=False)
            return

        response = calculations.check_available_time(day_det, service_det)
        if response[0] is None:
            bot.send_message(call.from_user.id, response[1])
            return
        keyboard = buttons.set_hours(data[2], data[3], data[1], data[5], response[0], data[6])
        bot.send_message(call.from_user.id, response[1], reply_markup=keyboard)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return

    elif 'create_order' in call.data:
        bot.delete_message(call.from_user.id, call.message.message_id)
        data = call.data.split(' ')
        order_creation(data[1], data[2], data[3], data[4], data[5], data[6], call)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)

    elif call.data == 'settings_client':
        keyboard = buttons.client_settings()
        bot.send_message(call.from_user.id, "Налаштування", reply_markup=keyboard)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return

    elif call.data == 'settings_master':
        keyboard = buttons.master_menu_1(call.from_user.id)
        bot.send_message(call.from_user.id, "Налаштування", reply_markup=keyboard)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return

    elif 'check_more_details' in call.data:
        data = call.data.split(' ')
        keyboard = buttons.master_more_details(data[1])
        bot.send_message(call.from_user.id, 'Деталі🗂:', reply_markup=keyboard)
        bot.answer_callback_query(call.id, text=" ", show_alert=False)
        return


def take_brake(message, call):
    if not calculations.regex_time(message):
        bot.send_message(message.chat.id, 'Формат часу: 1-15 – це буде одна '
                                          'година, 15 хвилин.')
        bot.register_next_step_handler(message, take_brake, call)
        return

    cur_day = calculations.get_current_day()
    day_det = get_cur_day(call.from_user.id, cur_day)
    response = calculations.check_available_time(day_det, message.text, set_custom_time=True, take_brake=True)
    bot.send_message(call.from_user.id, response[1])
    if response[0] is not None:
        try:
            create_order(call.from_user.id, call.from_user.id, day_det[0].id, message.text, None, '0', True)
        except Exception as ex:
            logging.error(f'Could not create free time slot. Cause: {ex}. Time: {time.asctime()}')
            session.rollback()
            return
        bot.send_message(call.from_user.id, 'Вільний таймслот створено!')
        to_menu(call.from_user.id)
        return


def order_creation(master_id, service_id, day_id, time_slot, next_week, reservation, call):
    if reservation == 'reservation':
        bot.send_message(call.from_user.id, 'Напишіть опис до замовлення. '
                                            'Наприклад ім`я та телефон замовника...')
        bot.register_next_step_handler(call.message, create_self_reservation, master_id, service_id,
                                       day_id, time_slot, next_week, call)
        return
    # bot.send_message(call.from_user.id, 'Предоплата и тд...')
    instance = create_order(master_id, call.from_user.id, day_id, time_slot, service_id, next_week)
    day = get_day_details(instance.day_id, instance.next_week)
    if instance is not None:
        bot.send_message(call.from_user.id, f"Заявку створено! \n\n"
                                            f"Номер заявки: {instance.id} \n"
                                            f"Час: {instance.time}\n"
                                            f"Дата: {calculations.get_date_by_day_number(day[0].day_num, instance.next_week).strftime('%Y-%m-%d')}\n"
                                            f"Детальну інформацію Ви можете переглянути в розділі 'Мої записи' -> \n"
                                            f"'У процесі виконання'")
    else:
        bot.send_message(call.from_user.id, "Щос пішло не так, відправте скріншот цієї переписки сюди - @fjskdb ")
    to_menu(call.from_user.id)


def create_self_reservation(message, master_id, service_id, day_id, time_slot, next_week, call):
    create_order(master_id, call.from_user.id, day_id, time_slot, service_id, next_week, self_res=True,
                 description=message.text)
    bot.send_message(call.from_user.id, f"Заявка створена!")
    to_menu(call.from_user.id)


def get_time_slots(message, day_det, service_det, day_id, master_id, service_id, next_week, reservation, call):
    if not re.match(r'^([0-1]?[0-9]|2[0-3])-[0-5][0-9]$', message.text):
        bot.send_message(message.chat.id, 'Формат часу: 1-15 – це буде одна '
                                          'година, 15 хвилин.')
        bot.register_next_step_handler(message, get_time_slots, service_det, day_id, master_id, service_id, next_week,
                                       reservation, call)
        return

    response = calculations.check_available_time(day_det, service_det, req=message.text, set_custom_time=True)
    bot.send_message(call.from_user.id, response[1])
    if response[0] is not None:
        order_creation(master_id, service_id, day_id, response[0], next_week, reservation, call)
    else:
        show_working_days(call, master_id, service_id, next_week, reservation)


def user_confirmation(call, master_id, service_id, reservation):
    keyboard = buttons.user_confirmation_buttons(master_id, service_id, reservation)
    service = get_service_by_id(service_id)
    master = get_master_by_id(master_id)
    bot.send_message(call.from_user.id, f"Ім'я майстра: {master[0].name} \n"
                                        f"Назва процедури: {service[0].name} \n"
                                        f"Ціна процедури: {service[0].money_cost}₴ \n"
                                        f"Тривалість процедури: годин - {service[0].time_cost.split('-')[0]}"
                                        f", хвилин - {service[0].time_cost.split('-')[1]}",
                     reply_markup=keyboard)


def show_working_days(call, master_id, service_id, next_week, reservation):
    try:
        days = get_available_days(master_id, calculations.get_current_day(), next_week)
    except Exception as ex:
        logging.error(f'Could not get available days. Cause: {ex}. Time: {time.asctime()}')
        return
    keyboard = buttons.reserve_day(days, master_id, service_id, next_week, reservation)

    if keyboard is None:
        keyboard = buttons.empty_template()
        keyboard.add(buttons.back_and_delete())
        bot.send_message(call.from_user.id, 'На жаль, доступних днів немає',
                         reply_markup=keyboard)
        return

    bot.send_message(call.from_user.id, 'Оберіть день:', reply_markup=keyboard)


def update_time(message, day_id, call):
    if not calculations.regex_time(message):
        bot.send_message(message.chat.id, 'Невірний формат часу, спробуйте ще раз. '
                                          '(Приклад: 9-00-18-00)')
        bot.register_next_step_handler(message, update_time, day_id, call)
        return

    if not calculations.check_time(message.text):
        bot.send_message(message.chat.id, 'Час початку не може буду більшим за час кінця робочого дня, '
                                          'спробуйте ще раз.')
        bot.register_next_step_handler(message, update_time, day_id, call)
        return

    try:
        response = edit_day(day_id, set_time=True, time=message.text)
    except Exception as ex:
        logging.error(f'Could not update working hours. Cause: {ex}. Time: {time.asctime()}')
        return

    if response is None:
        logging.error('edit_day method: unknown option')

    set_working_days(call, False, 'show')


def set_working_time(message, call):
    if not calculations.regex_time(message):
        bot.send_message(message.chat.id, 'Невірний формат часу, спробуйте ще раз. '
                                          '(Приклад: 9-00-18-00)')
        bot.register_next_step_handler(message, set_working_time, call)
        return
    if not calculations.check_time(message.text):
        bot.send_message(message.chat.id, 'Час початку не може буду більшим за час кінця робочого дня, '
                                          'спробуйте ще раз.')
        bot.register_next_step_handler(message, set_working_time, call)
        return
    try:
        update_working_time(message.from_user.id, message.text)
    except Exception as ex:
        logging.error(f'Could not set working time. Cause: {ex}, Time: {time.asctime()}')
        session.rollback()
        return
    bot.send_message(call.from_user.id, 'Час виставлено!⏱')
    to_menu(call.from_user.id)


def set_working_days(call, again, option):
    try:
        days = get_days(call.from_user.id)
    except Exception as ex:
        logging.error(f'Could not get master working days from db. Cause: {ex}. Time: {time.asctime()}')
        return

    if option == 'show':
        keyboard = buttons.working_days_buttons(days, option)
        bot.send_message(call.from_user.id, keyboard[0], reply_markup=keyboard[1])
        return

    elif option == 'add':
        keyboard = buttons.working_days_buttons(days, option)

        if again:
            bot.edit_message_reply_markup(call.from_user.id, call.message.message_id,
                                          reply_markup=keyboard)
        else:
            bot.send_message(call.from_user.id, "Оберіть дні, по яким Ви працюєте👩‍⚕",
                             reply_markup=keyboard)
        return

    elif option == 'edit':
        keyboard = buttons.working_days_buttons(days, option)

        if keyboard is None:
            bot.send_message(call.from_user.id, 'Робочі дні не знайдені!')
            set_working_days(call, False, 'show')
            return
        bot.send_message(call.from_user.id, 'Оберіть день, який хочете редагувати',
                         reply_markup=keyboard)
        return


def add_new_service(call, reg=False):
    keyboard = buttons.service_segments(call.from_user.id, True, call.from_user.id, reg=reg)
    bot.send_message(call.from_user.id,
                     'Оберіть сегмент послуг, що надаєте 🧚🏻‍♀',
                     reply_markup=keyboard)


def set_feedback(message, user_id, master_id, call):
    keyboard = buttons.to_completed_services()

    if message.text is None:
        bot.send_message(user_id, 'Неправильний формат тексту(')
        to_menu(call.from_user.id)
        return
    else:
        try:
            create_feedback(master_id, user_id, message.text)
        except Exception as ex:
            logging.error(f'Could not create feedback. Cause: {ex}. Time: {time.asctime()}')
            session.rollback()
            return

    bot.send_message(call.from_user.id, 'Дякую за вігук ☺', reply_markup=keyboard)
    return


def delete_service_image(service_id, user_id):
    service_instance = get_sample_service_by_id(service_id)

    if service_instance[0].image is not None:
        try:
            os.remove(data_path + str(user_id) + '\\services\\' +
                      str(service_instance[0].image) + '.jpg')
        except Exception as ex:
            logging.error(f'Could not delete service image. Cause: {ex}. Time: {time.asctime()}')


def delete_certificate_image(certificate_id, user_id):
    certificate_instance = get_certificate_by_id(certificate_id)

    if certificate_instance[0].image is not None:
        try:
            os.remove(data_path + str(user_id) + '\\certificates\\' +
                      str(certificate_instance[0].image) + '.jpg')
        except Exception as ex:
            logging.error(f'Could not delete certificate image. Cause: {ex}. Time: {time.asctime()}')


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
        logging.error(f'Could not update certificate description. Cause: {ex}. Time: {time.asctime()}')
        session.rollback()
        edit_certificate(certificate_id, message.from_user.id)
        return
    edit_certificate(certificate_id, message.from_user.id)
    return


def edit_certificate_photo(message, certificate_id):
    certificate_instance = get_certificate_by_id(certificate_id)
    try:
        photo = get_photo(message)
    except Exception as ex:
        logging.error(f'Could not get certificate photo. Cause: {ex}. Input: {message.text}. Time: {time.asctime()}')
        bot.send_message(message.from_user.id, "Відправте фотографію (можливо Ви її відправили у форматі файлу,"
                                               " потрібно у форматі фотографії!)")
        bot.register_next_step_handler(message, edit_certificate_photo)
        return

    if certificate_instance.__len__() < 1:
        return

    if certificate_instance[0].image is not None:
        ran = certificate_instance[0].image
    else:
        ran = gen_path(message, 'certificates')

    try:
        update_certificate_photo(message, ran, False, photo)
    except Exception as ex:
        session.rollback()
        logging.error(f'Could not update certificate photo. Cause: {ex}. Time: {time.asctime()}')
        return
    edit_certificate(certificate_id, message.from_user.id)


def update_certificate_photo(message, ran, create, photo):
    if not os.path.exists(data_path + str(message.from_user.id) + '\\certificates'):
        os.makedirs(data_path + str(message.from_user.id) + '\\certificates')

    with open(data_path + str(message.from_user.id) + '\\certificates\\' +
              str(ran) + '.jpg', 'wb') as file:
        file.write(photo)
    image = str(ran)

    if create:
        try:
            create_certificate(message.from_user.id, image)
        except Exception as ex:
            logging.error(f'Could not create certificate. Cause: {ex}. Time: {time.asctime()}')
            session.rollback()
            return
        return image
    else:
        return


def to_menu(user_id):
    try:
        if get_user_role(user_id):
            user_instance = get_master(user_id)

            if user_instance[0].cur_role:
                keyboard = buttons.main_menu_master(user_id)
            else:
                keyboard = buttons.client_menu('master')

        else:
            keyboard = buttons.client_menu('client')
    except Exception as ex:
        logging.error(f'Could not get user data. Func: to_menu . Cause: {ex}. Time: {time.asctime()}')
        return
    bot.send_message(user_id, '<<<<<< Головне меню 🏠 >>>>>>', reply_markup=keyboard)


def edit_sample_service(service_id, user_id):
    keyboard = buttons.edit_sample_service_buttons(service_id, user_id)
    bot.send_message(user_id, 'Оберіть, що хочете змінити⚙',
                     reply_markup=keyboard)


def edit_sample_service_photo(message, service_id):
    try:
        service_instance = get_sample_service_by_id(service_id)
    except Exception as ex:
        logging.error(f'Could not get sample service data. Cause: {ex}. Time: {time.asctime()}')
        return
    try:
        photo = get_photo(message)
    except Exception as ex:
        logging.error(f'Could not get sample service photo. Cause: {ex}. Input: {message.text}. Time: {time.asctime()}')
        bot.send_message(message.from_user.id, "Відправте фотографію (можливо Ви її відправили у форматі файлу,"
                                               " потрібно у форматі фотографії!)")
        bot.register_next_step_handler(message, edit_sample_service_photo, service_id)
        return

    if service_instance.__len__() < 1:
        return

    if service_instance[0].image is not None:
        ran = service_instance[0].image
    else:
        ran = gen_path(message, 'services')

    try:
        update_samp_serv_photo(message, service_id, ran, photo)
    except Exception as ex:
        logging.error(f'Could not update sample service photo. Cause: {ex}. Time: {time.asctime()}')
        session.rollback()
        return
    edit_sample_service(service_id, message.from_user.id)


def update_samp_serv_photo(message, service_id, ran, photo):
    if not os.path.exists(data_path + str(message.from_user.id) + '\\services'):
        os.makedirs(data_path + str(message.from_user.id) + '\\services')

    with open(data_path + str(message.from_user.id) + '\\services\\' +
              str(ran) + '.jpg', 'wb') as file:
        file.write(photo)
    image = str(ran)
    try:
        update_service_photo(message.from_user.id, service_id, image)
    except Exception as ex:
        logging.error(f'Could not update service photo. Cause: {ex}. Time: {time.asctime()}')
        session.rollback()
        return


def edit_sample_service_name(message, service_id):
    if message.text is None:
        bot.send_message(message.from_user.id, 'Неправильний формат вводу,'
                                               ' напишіть назву послуги')
        bot.register_next_step_handler(message, edit_sample_service_name, service_id)

    try:
        update_sample_service_name(service_id, message.text)
    except Exception as ex:
        logging.error(f'Could not update sample service name. Cause: {ex}. Time: {time.asctime()}')
        session.rollback()
        edit_sample_service(service_id, message.from_user.id)
        return
    edit_sample_service(service_id, message.from_user.id)
    return


def edit_service(user_id, segment):
    keyboard = buttons.get_services(user_id, user_id, segment, None, True)
    bot.send_message(user_id, keyboard[0],
                     reply_markup=keyboard[1])


def master_reg_start(message, user_id):
    bot.send_message(user_id, 'Відправте мені ваше фото')
    bot.register_next_step_handler(message=message, reg='reg', callback=set_acc_photo)


def edit_name(message, role):
    try:
        update_name(message.from_user.id, message.text, role)
    except Exception as ex:
        logging.error(f'Could not update name. Cause: {ex}. Time: {time.asctime()}')
        session.rollback()
        return
    edit_profile(message.from_user.id, role)


def edit_telephone(message, role):
    try:
        if message.contact is not None:
            update_telephone(message.from_user.id, message.contact.phone_number, role)
        else:
            update_telephone(message.from_user.id, message.text, role)

    except Exception as ex:
        logging.error(f'Could not update telephone. Cause: {ex}. Input: {message.text}. Time: {time.asctime()}')
        session.rollback()
        return
    bot.send_message(message.from_user.id, 'Змінено!', reply_markup=buttons.del_button())
    bot.send_message(message.from_user.id, "Повертаю вашу кнопочку 'меню'", reply_markup=buttons.keyboard_menu_button())
    edit_profile(message.from_user.id, role)


def edit_profile(user_id, role):
    keyboard = buttons.edit_profile_buttons(role)
    bot.send_message(user_id, 'Оберіть, що хочете змінити🛠',
                     reply_markup=keyboard)


def edit_details(message):
    try:
        update_acc_details(message.from_user.id, message.text)
    except Exception as ex:
        logging.error(f'Could not update account details. Cause: {ex}. Input: {message.text}. Time: {time.asctime()}')
        session.rollback()
        return
    edit_profile(message.from_user.id, 'master')


def set_money_cost(message, service_id, segment, reg='1'):
    if not message.text.isdigit():
        bot.send_message(message.chat.id, 'Це повинно бути число')
        bot.register_next_step_handler(message, set_money_cost, service_id, segment, reg)
        return

    try:
        update_service_cost(service_id, message.text)
    except Exception as ex:
        logging.error(f'Could not update service cost. Cause: {ex}. Input: {message.text}. Time: {time.asctime()}')
        session.rollback()
        return

    if reg == 'reg':
        bot.send_message(message.chat.id, 'Скільки процедура займає часу⏱? \n\n'
                                          '_Наприклад, 1-15 – це буде одна година, '
                                          '15 хвилин._',
                         parse_mode='markdown')
        bot.register_next_step_handler(message, set_time_cost, service_id, segment, reg)
    else:
        bot.send_message(message.from_user.id, 'Виконано!')
        edit_service(message.from_user.id, segment)


def set_email(message, role, reg):
    if not re.match(r'^[a-z0-9A-Z._]+[@]\w+[.]\w{2,3}$', message.text):
        bot.send_message(message.chat.id, "Невірний формат електронної адреси")
        bot.send_message(message.chat.id, "Спробуйте ще раз!")
        bot.register_next_step_handler(message, set_email, role, reg)
        return
    else:
        try:
            update_email(message.from_user.id, message.text, role)
        except Exception as ex:
            logging.error(f'Could not set mail. Cause: {ex}. Time: {time.asctime()}')
            session.rollback()
            return
        if reg == 'reg':
            keyboard = buttons.city_buttons(role, reg)
            bot.send_message(message.chat.id, "А зараз оберіть Ваше місто:", reply_markup=keyboard)
        else:
            edit_profile(message.from_user.id, role)


def set_time_cost(message, service_id, segment, reg='1'):
    if not re.match(r'^([0-1]?[0-9]|2[0-3])-[0-5][0-9]$', message.text):
        bot.send_message(message.chat.id, 'Формат часу: 1-15 – це буде одна '
                                          'година, 15 хвилин.')
        bot.register_next_step_handler(message, set_time_cost, service_id, segment, reg)
        return

    try:
        update_service_time_cost(service_id, message.text)
    except Exception as ex:
        logging.error(f'Could not update service time cost. Cause: {ex}. Input: {message.text}. Time: {time.asctime()}')
        session.rollback()
        return

    if reg == 'reg':
        keyboard = buttons.to_menu()
        keyboard.add(buttons.add_more_button())
        bot.send_message(message.chat.id, 'Процедуру додано 👍', reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, 'Виконано!')
        edit_service(message.from_user.id, segment)


def show_orders(orders, user_id, master_flag, call):
    counter = 1
    for order in orders:
        keyboard = buttons.empty_template()
        try:
            service = get_service_by_id(order.service_id)
            master = get_master(order.master_id)
            day = get_day_details(order.day_id)
            if order.client_id is None:
                client = get_master(order.client_id_master_acc)
            else:
                client = get_client(order.client_id)

        except Exception as ex:
            logging.error(f'Could not get data. Func: show_orders. Cause: {ex}. Time: {time.asctime()}')
            session.rollback()
            return
        prepaid = 'Так' if order.prepaid else 'Ні'
        if not master_flag:
            try:

                if check_rating(user_id, order.master_id) and order.done:
                    keyboard.add(buttons.rating_button(order.master_id))

                # if check_feedback(user_id, order.master_id) and order.done:
                #     keyboard.add(buttons.feedback_button(order.master_id))

            except Exception as ex:
                logging.error(f'Could not check rating or feedback. Cause: {ex}. Time: {time.asctime()}')
                return

        elif master_flag and not order.done:
            keyboard.add(buttons.mark_as_done(order.id, call.message.message_id + counter))
        start_time = order.time.split('-')

        if service.__len__() < 1:
            bot.send_message(user_id, f'Перерва \n'
                                      f'Час: {order.time}  \n'
                                      f'День тижня: {day[0].day_name} \n',
                             reply_markup=keyboard)
        else:
            date = calculations.get_date_by_day_number(day[0].day_num, order.next_week).strftime("%Y-%m-%d")
            if not order.done and not order.canceled_by_system \
                    and not order.canceled_by_master and not order.canceled_by_client and master_flag:
                keyboard.add(buttons.mark_as_canceled_by_master(order.id, call.message.message_id + counter))
            if not order.done and not order.canceled_by_system \
                    and not order.canceled_by_master and not order.canceled_by_client and not master_flag:
                keyboard.add(buttons.mark_as_canceled_by_client(order.id, call.message.message_id + counter))
            canceled = ''

            if order.canceled_by_system:
                canceled = '\n\nВідхилено системою. \n'
            elif order.canceled_by_master:
                canceled = '\n\nВідхилено майстром. \n'
            elif order.canceled_by_client:
                canceled = '\n\nВідхилено клієнтом. \n'

            if order.self_res:
                bot.send_message(user_id,
                                 f'*Саморезервація* \n\n'
                                 f'Назва послуги: {str(service[0].name)} \n'
                                 f'Початок о: {start_time[0]}-{start_time[1]}  \n'
                                 f'День тижня: {day[0].day_name} \n'
                                 f'Дата: {order.order_date} \n'
                                 f"Ім'я майстра:  {str(master[0].name)} \n"
                                 f"Телефон майстра: {str(master[0].telephone)} \n"
                                 f"Опис: {order.description} {canceled}",
                                 reply_markup=keyboard)
            else:
                bot.send_message(user_id,
                                 f'Назва послуги: {str(service[0].name)} \n'
                                 f'Початок о: {start_time[0]}-{start_time[1]}  \n'
                                 f'День тижня: {day[0].day_name} \n'
                                 f'Дата: {date} \n'
                                 f"Ім'я майстра:  {str(master[0].name)} \n"
                                 f"Телефон майстра: {str(master[0].telephone)} \n"
                                 f"Ім'я клієнта: {str(client[0].name)} \n"
                                 f"Телефон клієнта: {str(client[0].telephone)} \n"
                                 f"Передплачено: {str(prepaid)}{canceled}",
                                 reply_markup=keyboard)

        counter += 1
    bot.send_message(user_id, 'Повернутись у меню', reply_markup=buttons.to_menu())


def registration(message, role):
    bot.send_message(message.chat.id, "Введіть своє ім'я, за яким клієнт зможе вас знайти "
                                      "(можна латиницею) і натисніть Enter ↩️")
    bot.register_next_step_handler(message=message, role=role, callback=set_name)


def set_name(message, role):
    try:
        create_user(user_id=message.from_user.id, name=message.text, username=message.from_user.username, role=role)
    except Exception as ex:
        logging.error(f'Could not set name. Cause: {ex}. Time: {time.asctime()}')
        return
    try:
        create_user_role(message.from_user.id)

        if role == 'master':
            update_master_flag(message.from_user.id)

    except Exception as ex:
        logging.error(f'Could not create user role, or update user to master. Cause: {ex}. Time: {time.asctime()}')
        return
    bot.send_message(message.chat.id, "Тепер надішліть свій телефон ☎️",
                     reply_markup=buttons.send_contact())
    bot.register_next_step_handler(message=message, role=role, callback=set_telephone)


def set_telephone(message, role):
    try:

        if message.contact is not None:
            update_telephone(message.from_user.id, message.contact.phone_number, role)
        else:
            update_telephone(message.from_user.id, message.text, role)

    except Exception as ex:
        logging.error(f'Could not set telephone. Cause: {ex}. Time: {time.asctime()}')
        session.rollback()
        return
    bot.send_message(message.from_user.id, 'Вкажіть діючу пошту✉',
                     reply_markup=buttons.del_button())
    bot.register_next_step_handler(message, set_email, role, 'reg')


def set_acc_photo(message, reg):
    if not os.path.exists(data_path + str(message.from_user.id) + '\\profile'):
        os.makedirs(data_path + str(message.from_user.id) + '\\profile')
    try:
        photo = get_photo(message)
    except Exception as ex:
        logging.error(f'Could not load account photo. Cause: {ex}. Input: {message}. Time: {time.asctime()}')
        bot.send_message(message.from_user.id, "Відправте фотографію (можливо Ви її відправили у форматі файлу,"
                                               " потрібно у форматі фотографії!)")
        bot.register_next_step_handler(message, set_acc_photo, reg)
        return
    with open(data_path + str(message.from_user.id) + '\\profile\\profile.jpg', 'wb') as file:
        file.write(photo)
    try:
        update_acc_photo(message.from_user.id)
    except Exception as ex:
        logging.error(f'Could not set acc photo (Line: 1067). Cause: {ex}. Time: {time.asctime()}')
        session.rollback()
        return

    if reg == 'reg':
        # bot.send_message(message.from_user.id,
        #                  'Напишіть номер картки, на яку будуть '
        #                  'надходити кошти.')
        # bot.register_next_step_handler(message, set_card)
        bot.send_message(message.from_user.id,
                         'Напишіть опис до аккаунту, що ви вмієте і тд.')
        bot.register_next_step_handler(message, set_acc_details)
    else:
        edit_profile(message.from_user.id, 'master')


# def set_card(message):
#     try:
#         update_card(message.from_user.id, base64.standard_b64encode(message.text.encode('UTF-8')))
#     except Exception as ex:
#         logging.error(f'Could not set credit card. Cause: {ex}. Time: {time.asctime()}')
#         session.rollback()
#         return
#     bot.send_message(message.from_user.id,
#                      'Напишіть опис до аккаунту, що ви вмієте і тд.')
#     bot.register_next_step_handler(message, set_acc_details)


def set_acc_details(message):
    try:
        update_acc_details(message.from_user.id, message.text)
    except Exception as ex:
        logging.error(f'Could not update account details. Cause: {ex}. Input: {message.text}. Time: {time.asctime()}')
        session.rollback()
        return
    user_instance = get_master(message.from_user.id)
    data = buttons.set_placement_buttons(user_instance[0].city_id, 'reg')
    bot.send_message(message.from_user.id, data[0],
                     reply_markup=data[1])


def show_profile(user_id, role):
    keyboard = buttons.empty_template()
    keyboard.add(buttons.back_and_delete())
    keyboard.add(buttons.edit_profile(role))

    if role == 'master':
        try:
            instance = get_master(user_id)
        except Exception as ex:
            logging.error(f'Could not get master data. Cause: {ex}. Time: {time.asctime()}')
            return
        try:
            img = open(data_path + str(user_id) + '\\profile\\profile.jpg', 'rb')
        except Exception as ex:
            logging.error(f'Could not load profile photo. Cause: {ex}. Time: {time.asctime()}')
            img = open(data_path + 'default.jpeg', 'rb')
        bot.send_photo(user_id, photo=img,
                       caption=f"Ім'я: "
                               f"{'Н/Д' if instance[0].name is None else instance[0].name} \n\n"
                               f"Телефон: "
                               f"{'Н/Д' if instance[0].telephone is None else instance[0].telephone} \n\n"
                               f"Пошта: "
                               f"{'Н/Д' if instance[0].email is None else instance[0].email} \n\n"
                               f"Посилання в телеграмі: @{instance[0].username} \n\n"
                       # f"Номер картки: *"
                       # f"{'Н/Д' if instance[0].card is None else (base64.standard_b64decode(instance[0].card)).decode('UTF-8')[-4:]} \n\n "
                               f"Назва салону: {instance[2]} \n\n"
                               f"Місто: "
                               f"{'Н/Д' if instance[3] is None else instance[3]} \n\n"
                               f"Опис аккаунту: {instance[0].details} \n\n"
                               f"Мій рейтинг: {instance[1]} \n\n",
                       reply_markup=keyboard)
        img.close()
    else:
        try:
            instance = get_client(user_id)
        except Exception as ex:
            logging.error(f'Could not get client data. Cause: {ex}. Time: {time.asctime()}')
            return
        bot.send_message(user_id,
                         f"Ім'я: {instance[0].name} \n\n"
                         f"Телефон: {instance[0].telephone} \n\n"
                         f"Пошта: {instance[0].email} \n\n"
                         f"Посилання в телеграмі: @{instance[0].username} \n\n"
                         f"Місто: {instance[1]} \n\n",
                         reply_markup=keyboard)


def add_certificate(message):
    bot.send_message(message.chat.id, 'Відправте фото сертифікату')
    bot.register_next_step_handler(message, set_certificate_photo)


def set_certificate_photo(message):
    try:
        photo = get_photo(message)
    except Exception as ex:
        logging.error(f'Wrong input. func: set_certificate_photo. Cause: {ex}. Time: {time.asctime()}')
        bot.send_message(message.from_user.id, "Відправте фотографію (можливо Ви її відправили у форматі файлу,"
                                               " потрібно у форматі фотографії!)")
        bot.register_next_step_handler(message, set_certificate_photo)
        return
    ran = gen_path(message, 'certificates')
    try:
        image = update_certificate_photo(message, ran, True, photo)
    except Exception as ex:
        logging.error(f'Could not update certificate photo. Cause: {ex}. Time: {time.asctime()}')
        session.rollback()
        return
    bot.send_message(message.chat.id, 'Напишіть опис до фото:')
    bot.register_next_step_handler(message=message, image=image, callback=set_certificate_details)


def set_certificate_details(message, image):
    try:
        update_certificate_details(message.from_user.id, image, message.text)
    except Exception as ex:
        logging.error(f'Could not set certificate. Cause: {ex}. Time: {time.asctime()}')
        session.rollback()
        return
    keyboard = buttons.to_menu()
    bot.send_message(message.from_user.id, 'Додано!', reply_markup=keyboard)


def get_photo(message):
    quantity = message.photo.__len__()
    raw = message.photo[quantity - 1].file_id
    file_info = bot.get_file(raw)
    return bot.download_file(file_info.file_path)


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


def gen_path(message, path):
    while True:
        ran = str(message.from_user.id) + '_' + str(random.randint(1000, 9999))

        if not os.path.exists(data_path + str(message.from_user.id) + '\\' + str(path) + '\\' +
                              str(ran) + '.jpg'):
            break

    return ran


def set_service_photo(message, service_id):
    try:
        photo = get_photo(message)
    except Exception as ex:
        logging.error(f'Could not get service photo. Cause: {ex}. Time: {time.asctime()}')
        bot.send_message(message.from_user.id, "Відправте фотографію (можливо Ви її відправили у форматі файлу,"
                                               " потрібно у форматі фотографії!)")
        bot.register_next_step_handler(message, set_service_photo, service_id)
        return
    ran = gen_path(message, 'services')
    try:
        update_samp_serv_photo(message, service_id, ran, photo)
    except Exception as ex:
        logging.error(f'Could not update service photo. Cause: {ex}. Time: {time.asctime()}')
        session.rollback()
        return

    keyboard = buttons.to_menu()
    bot.send_message(message.from_user.id, 'Додано!', reply_markup=keyboard)


def show_certificates(index, end_index, certificates, user_id):
    keyboard = buttons.moving_certificates_buttons(index, end_index, certificates[int(index)].id,
                                                   certificates[int(index)].user_id, user_id)
    try:
        img = open(data_path + str(certificates[int(index)].user_id) + '\\certificates\\' + certificates[
            int(index)].image + '.jpg', 'rb')
    except Exception as ex:
        logging.error(f'Could not load certificate image. Cause: {ex}')
        img = open(data_path + 'default.jpeg', 'rb')
    bot.send_photo(user_id, photo=img,
                   caption=f"Опис: {certificates[int(index)].description} \n\n", reply_markup=keyboard)


def show_services(index, end_index, services, user_id):
    keyboard = buttons.moving_services_buttons(index, end_index, services[int(index)].id,
                                               services[int(index)].master_id, user_id)
    try:
        img = open(data_path + str(services[int(index)].master_id) + '\\services\\' + services[int(index)].image
                   + '.jpg', 'rb')
    except Exception as ex:
        logging.error(f'Could not load service image. Cause: {ex}. Time: {time.asctime()}')
        img = open(data_path + 'default.jpeg', 'rb')
    bot.send_photo(user_id, photo=img,
                   caption=f"Назва: {services[int(index)].name} \n\n",
                   reply_markup=keyboard)


def show_masters(index, end_index, masters, user_id, is_saved=False, message_id=False):
    keyboard = buttons.moving_masters_buttons(index, end_index,
                                              masters[int(index)].user_id,
                                              masters[int(index)].placement_id, is_saved, message_id)
    try:
        img = open(data_path + masters[int(index)].user_id + '\\profile\\profile.jpg', 'rb')
    except Exception as ex:
        logging.error(f'Could not load master image. Cause: {ex}. Time: {time.asctime()}')
        img = open(data_path + 'default.jpeg', 'rb')
    try:
        segments = get_segments_for_master(masters[int(index)].user_id)
    except Exception as ex:
        logging.error(f'Could not get master segments. Cause: {ex}. Time: {time.asctime()}')
        return
    segments_text = ''
    for segment in segments:
        segments_text += '🔸 ' + segment + '\n'
    if int(get_point(masters[int(index)].user_id)) > 0:
        rating = f"\nРейтинг: " + "⭐️" * int(get_point(masters[int(index)].user_id)) + "\n\n"
    else:
        rating = ''
    bot.send_photo(user_id, photo=img,
                   caption=f"Ім'я: {masters[int(index)].name} \n\n"
                           f"Опис: {masters[int(index)].details} \n\n"
                           f'Категорії робіт, які виконує майстер:\n{segments_text} \n {rating}',
                   reply_markup=keyboard)


bot.enable_save_next_step_handlers(delay=2)


bot.load_next_step_handlers()


def check_start_up_data():
    cities = get_cities()

    if cities.__len__() < 1:
        os.system('mysqlsh -uroot -fdata.sql')
    else:
        return


def start_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


def start_bot():
    logging.basicConfig(filename='.log',
                        format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s')
    try:
        check_start_up_data()
        bot.polling()
    except Exception as e:
        logging.error(f'Could not start a bot. Cause: {e}. Time: {time.asctime()}')


if __name__ == '__main__':
    bot_process = Process(target=start_bot)
    bot_process.start()
    schedule_process = Process(target=start_schedule)
    schedule_process.start()

    while True:
        time.sleep(1)
        if not bot_process.is_alive():
            schedule_process.terminate()
            break

    # schedule_process.join()
    # bot_process.join()
