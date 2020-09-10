import requests
import re

import DateConverter

YEAR_IDX = 0
MONTH_IDX = 1
DAY_IDX = 2


def construct_url(ticker, date, period):

    url_format = "https://finance.yahoo.com/quote/{0}/history?period1={1}&period2={2}&interval=1d&filter=history&frequency=1d"

    start_date = DateConverter.date_to_int(date[YEAR_IDX], date[MONTH_IDX], date[DAY_IDX])
    end_date = DateConverter.add_time_to_time(period[YEAR_IDX], period[MONTH_IDX], period[DAY_IDX], start_date)
    
    url = url_format.format(ticker, start_date, end_date)

    return url


def get_contents_from_url(url):

    try:
        res = requests.get(url)
    except:
        print("ERROR: For some reason a request has failed")
        return ""

    return res.content


def get_data_from_contents(contents, period):

    cont = str(contents)
    all_values = list()
    cont_sp = cont.split('<span data-reactid=')

    for block in cont_sp:

        try:
            val = block[block.find('>')+1:block.find('</span>')]

            if '.' in val:
                val = float(val)
                all_values.append(val)

        except:
            pass

    return min(all_values), max(all_values), sum(all_values)/len(all_values)

'''
url = construct_url("AAPL", [2020,8,28], [0,0,0])
cont = get_contents_from_url(url)
stuff1, stuff2, stuff3 = get_data_from_contents(cont, [0,0,0])
print(stuff1)
print(stuff2)
print(stuff3)

url = construct_url("AAPL", [2019,8,23], [1,0,0])
cont = get_contents_from_url(url)
stuff1, stuff2, stuff3 = get_data_from_contents(cont, [0,0,5])
print(stuff1)
print(stuff2)
print(stuff3)
'''
