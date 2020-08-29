from datetime import date

# starting at 2010
new_year_time = [1262390400,
                 1293926400,
                 1325462400,
                 1357084800,
                 1388620800,
                 1420156800,
                 1451692800,
                 1483315200,
                 1514851200,
                 1546387200,
                 1577923200]

days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# leap year makes feb +1 day
leap_years = [2012, 2016, 2020]

DAY_LEN = 86400


def date_to_int(year, month, day):

    if (year > 2020 or year < 2010):
        return -1

    return_time = new_year_time[year-2010]
    return_time += sum(days_per_month[:month-1]) * DAY_LEN
    return_time += (day-1) * DAY_LEN

    if ((year in leap_years) and (month > 2)):
        return_time += DAY_LEN
        
    return return_time


def get_today_time():

    today = date.today()
    today_time = date_to_int(today.year, today.month, today.day)
    return today_time


def add_time_to_time(years, months, days, time):

    return_time = time
    return_time += years * DAY_LEN * 365
    return_time += months * DAY_LEN * 30
    return_time += days * DAY_LEN

    today_time = get_today_time()

    if today_time < return_time:
        return -1

    return return_time

'''
l = date_to_int(2019, 10, 15)
print (l)
l = get_today_time()
print (l)
l = add_time_to_time(1, 0, 0, date_to_int(2019, 10, 15))
print (l)
'''
