import os
import urllib.request

BLACK_LIST = ['HTZ', 'BFET', 'TCB']

def download_ticker_cache(ticker):

    url = "https://query1.finance.yahoo.com/v7/finance/download/{0}?period1=0&period2=2000000000&interval=1d&events=history".format(ticker)

    file_path = os.path.dirname(os.path.realpath(__file__))
    file_path += "/caches/{0}.csv".format(ticker)

    print("Caching Stock Price Data For: ${0}".format(ticker))

    try:
        urllib.request.urlretrieve(url, file_path)

    except:
        return -1


def check_for_cache(ticker):

    file_path = os.path.dirname(os.path.realpath(__file__))
    file_path += "/caches/{0}.csv".format(ticker)

    return os.path.exists(file_path)


def ensure_cache_avail(ticker):

    if not check_for_cache(ticker):

        ret = download_ticker_cache(ticker)

        if ret == -1:
            return -1


def get_cont_from_cache(ticker):

    ret = ensure_cache_avail(ticker)
    if ret == -1:
        return -1

    file_path = os.path.dirname(os.path.realpath(__file__))
    file_path += "/caches/{0}.csv".format(ticker)

    cache = open(file_path, 'r')

    cont = cache.read()
    return cont


def month_by_month_performance(ticker, year, mon, day):
    global BLACK_LIST
    MONTHS = 24

    # Get contents from historical data for specific ticker
    cont = get_cont_from_cache(ticker)
    if cont == -1:
        print("ERROR: Ticker ${0} doesn't exist".format(ticker))
        return [None] * MONTHS, [None] * MONTHS
    cont_sp = cont.split('\n')

    # Get historical data for SPY for calculating alpha
    cont_a = get_cont_from_cache("SPY")
    cont_a_sp = cont_a.split('\n')

    # Create 24 month performance and alpha performance buffer
    perf = [None] * MONTHS
    perf_a = [None] * MONTHS

    # Get prices for ticker and SPY at time of purchase
    purchase_price, trash = find_price_by_date(cont_sp, year, mon, day)
    purchase_price_a, trash = find_price_by_date(cont_a_sp, year, mon, day)

    # If ticker is known to have corrupt data return empty list
    if ticker in BLACK_LIST:
        return perf, perf_a

    # For each of our 24 month bands that we are checking for
    for i in range(MONTHS):

        i2 = i+1
        # Get the prices for the ticker and SPY for the new month
        new_price, idx1 = find_price_by_date(cont_sp, year+int(i2/12), mon+(i2%12), day)
        cont_sp = cont_sp[idx1:]
        new_price_a, idx2 = find_price_by_date(cont_a_sp, year+int(i2/12), mon+(i2%12), day)
        cont_a_sp = cont_a_sp[idx2:]

        if new_price != None and new_price_a != None and purchase_price != 0 and purchase_price_a != 0 and purchase_price != None and purchase_price_a != None:

            # Calculate performance since asset purchase
            perf[i] = ((new_price / purchase_price) - 1) * 100

            # Calculate performance of asset relative to performance of SPY
            perf_a[i] = perf[i] - ((new_price_a / purchase_price_a) - 1) * 100

    return perf, perf_a


def find_price_by_date(cont_sp, year, mon, day):
   
    #print('{0}, {1}, {2}'.format(year, mon, day))

    for i in range(1,len(cont_sp)):

        ln_sp = cont_sp[i].split(',')

        if date_comp(ln_sp[0], year, mon, day):

            try:
                return float(ln_sp[1]), i 
            except:
                return None, i

    #print("ERROR: Date exceeded returning None <find_price_by_date()>")
    return None, 0


def date_comp(str_date, year, mon, day):
    '''
    returns: True if the string date is later than or equal to the specified year,mon,day
    returns: False otherwise
    
    str_date: in format "{year}-{mon}-{day}"
    '''

    try:
        date_sp = str_date.split('-')
        year_q = int(date_sp[0])
        mon_q = int(date_sp[1])
        day_q = int(date_sp[2])

    except:
        print("ERROR: Date is in some way malformed")

    res = (year_q * 1000 + mon_q * 50 + day_q) >= (year * 1000 + mon * 50 + day)
    return res
