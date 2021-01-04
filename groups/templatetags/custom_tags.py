from django import template
from datetime import datetime, date

register = template.Library()


def get_str(user):
    return str(user)

register.filter('get_str',get_str)


def get_size(size):
    return len(size)

register.filter('get_size',get_size)


def set_nr(nr):
    global x
    x = nr
    return x

register.filter('set_nr',set_nr)


def get_nr(nr):
    global x
    return x

register.filter('get_nr',get_nr)


def get_date_size(y):

    date_for_weekday = y.replace("-"," ")
    numbers = [int(word) for word in date_for_weekday.split() if word.isdigit()]
    date_for_weekday = date(numbers[0], numbers[1], numbers[2])

    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    dt = now.strptime(dt_string,"%Y-%m-%d %H:%M:%S")

    ExpectedDate1 = str(y)
    if date_for_weekday.weekday() == 2:
        ExpectedTime2 = "22:00"
    if date_for_weekday.weekday() == 6:
        ExpectedTime2 = "12:00"
    space = " "
    ExpectedDate = ExpectedDate1 + space + ExpectedTime2
    ExpectedDate = datetime.strptime(ExpectedDate, "%Y-%m-%d %H:%M")

    if dt > ExpectedDate:
        return 0
    else:
        return 1

register.filter('get_date_size',get_date_size)


def replace_(name):
    name = name.replace(" ", "_")
    return name

register.filter('replace_', replace_)

