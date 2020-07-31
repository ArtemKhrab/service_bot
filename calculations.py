import re
from datetime import datetime
from datetime import timedelta
from config import utc


def check_time(t):
    data = t.split('-')
    if int(data[0]) < int(data[2]) or (int(data[0]) == int(data[2]) and int(data[1]) < int(data[3])):
        return True
    else:
        return False


def regex_time(message):
    if not re.match(r"^([0-1]?[0-9]|2[0-3])-[0-5][0-9]-([0-1]?[0-9]|2[0-3])-[0-5][0-9]$", message.text):
        return False
    else:
        return True


def get_current_day():
    return datetime.date(datetime.now()).weekday()


def get_current_year():
    return datetime.date(datetime.now()).year


def get_date_by_day_number(day_num, next_week):
    today = get_current_day()
    day_diff = day_num - today
    if next_week == '1':
        return datetime.today() + timedelta(days=day_diff+7)
    else:
        return datetime.today() + timedelta(days=day_diff)


def check_available_time(day_det, service_det, req=None, set_custom_time=False, take_brake=False):
    today = datetime.now().weekday()
    now = datetime.utcnow() + timedelta(hours=utc)
    try:
        working_hours = day_det[0].working_hours.split('-')
    except Exception as ex:
        print(ex)
        return [None, 'На жаль, майстер не вказав робочі години на даний період. '
                      'Будь ласка, зверніться до адміністратора: номер телефону.']
    orders = day_det[1]
    time_item = datetime.now()
    if not take_brake:
        service_time = service_det[0].time_cost.split('-')
    else:
        data = service_det.split('-')
        temp_end = time_item.replace(hour=int(data[2]), minute=int(data[3]))
        req = f'{data[0]}-{data[1]}'
        temp = temp_end - timedelta(hours=int(data[0]), minutes=int(data[1]))
        service_time = [str(temp.strftime('%H')), str(temp.strftime('%M'))]
        del temp, temp_end
    master_start_time = now + timedelta(minutes=20) if day_det[0].day_num == today else \
        time_item.replace(hour=int(working_hours[0]), minute=int(working_hours[1]))
    master_end_time = time_item.replace(hour=int(working_hours[2]), minute=int(working_hours[3]))
    time_slots = []
    if set_custom_time:
        user_time = req.split('-')
        user_time_start = time_item.replace(hour=int(user_time[0]), minute=int(user_time[1]))
        if day_det[0].day_num == today:
            if user_time_start < now:
                return [None, 'Ви не можете записатись на час, який вже пройшов']
        user_time_end = user_time_start + timedelta(hours=int(service_time[0]), minutes=int(service_time[1]))

        if master_start_time <= user_time_start and master_end_time >= user_time_end:

            if not orders:
                return [req, f"Вас записано на {req}"]
            else:

                for order in orders:
                    order_time = order.time.split('-')
                    order_start = time_item.replace(hour=int(order_time[0]), minute=int(order_time[1]))
                    order_end = time_item.replace(hour=int(order_time[2]), minute=int(order_time[3]))
                    if (order_start <= user_time_start < order_end) or (order_start < user_time_end <= order_end):
                        return [None, "Даний час вже зайнято. Будь ласка, оберіть інший"]

                else:
                    return [req, f"Вас записно на {req}"]

        else:
            return [None,
                    'Майстер не працює в заданий час, або він не встигне виконати роботу, оберіть інший час']
    else:

        if not orders:
            afternoon = time_item.replace(hour=12, minute=00)
            if (master_start_time + timedelta(hours=int(service_time[0]), minutes=int(service_time[1]))) \
                    <= master_end_time:
                time_slots.append(str(master_start_time.strftime("%H-%M")))

            if master_start_time <= afternoon and (afternoon + timedelta(hours=int(service_time[0]),
                                                                         minutes=int(service_time[1]))) \
                    <= master_end_time and (day_det[0].day_num != today or
                                            (day_det[0].day_num == today and now < afternoon)):
                time_slots.append(str(afternoon.strftime("%H-%M")))

            if (master_end_time - timedelta(hours=int(service_time[0]), minutes=int(service_time[1]))) \
                    >= master_start_time:
                time_slots.append(str((master_end_time - timedelta(hours=int(service_time[0]),
                                                                   minutes=int(service_time[1]))).strftime(
                    "%H-%M")))
            return [time_slots, "Оберіть час із запропонованого, або задайте свій"]
        else:
            quantity = orders.__len__()-1
            counter = 0
            service_time_cost = time_item.replace(hour=int(service_time[0]), minute=int(service_time[1]))
            for order in orders:
                if counter == 0:
                    order_time = order.time.split('-')
                    order_start = time_item.replace(hour=int(order_time[0]), minute=int(order_time[1]))
                    if (order_start - timedelta(hours=int(working_hours[0]),
                                                minutes=int(working_hours[1]))) >= service_time_cost:
                        time_slots.append(str(master_start_time.strftime("%H-%M")))

                if counter == quantity:
                    order_time = order.time.split('-')
                    order_end = time_item.replace(hour=int(order_time[2]), minute=int(order_time[3]))
                    if (master_end_time - timedelta(hours=int(order_time[2]),
                                                    minutes=int(order_time[3]))) >= service_time_cost:
                        time_slots.append(str(order_end.strftime("%H-%M")))
                else:
                    order_time = orders[counter].time.split('-')
                    next_order_time = orders[counter + 1].time.split('-')
                    next_order_start = time_item.replace(hour=int(next_order_time[0]), minute=int(next_order_time[1]))
                    order_end = time_item.replace(hour=int(order_time[2]), minute=int(order_time[3]))
                    if (next_order_start - timedelta(hours=int(order_time[2]), minutes=int(order_time[3]))) >= \
                            service_time_cost:
                        time_slots.append(str(order_end.strftime("%H-%M")))
                counter += 1
            return [time_slots, "Оберіть час із запропонованого, або задайте свій"]
