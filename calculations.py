import time
import cmath
import re
from datetime import datetime
import calendar


def check_time(t):
    data = t.split('-')
    if int(data[0]) < int(data[2]) or (int(data[0]) == int(data[2]) and int(data[1]) < int(data[3])):
        return True
    else:
        return False


def regex_time(message):
    if not re.match(r'^([0-1]?[0-9]|2[0-3])-[0-5][0-9]-([0-1]?[0-9]|2[0-3])-[0-5][0-9]$', message.text):
        return False
    else:
        return True


def get_current_day():
    return datetime.date(datetime.now()).weekday()

if __name__ == '__main__':
    print(calendar.day_name[get_current_day()])