from tika import parser
import os

'''
[[ticker, S/P, date[year, mon, day], amount(eventually)],...]
'''

TICKER_IDX = 0
SP_IDX = 1
DATE_IDX = 2
#AMOUNT_IDX = 3

YEAR_IDX = 0
MON_IDX = 1
DAY_IDX = 2


def get_all_pdf_nums():

    file_path = os.path.dirname(os.path.realpath(__file__))
    file_path += "/pdfs/"

    dir_cont = os.listdir(file_path)
    return dir_cont


def parse_pdf_for_trades(pdf_name):

    name = "0"

    trades = list()

    try:
        file_path = os.path.dirname(os.path.realpath(__file__))
        file_path += "/pdfs/{0}".format(pdf_name)

        print(file_path)

        raw = parser.from_file(file_path)

        cont = raw['content']
        cont = cont.replace('(partial)','')
        cont_sp = cont.split('\n')

    except:
        return None, None

    for line in cont_sp:

        if 'Name' in line or "name" in line:
            if "Hon" in line:
                name = line[6:]
        '''
        if '(' in line and '$' in line:

            line_sp = line.split('(')
            other_sp = line_sp[1].split(' ')
            #print(other_sp)

            try:
                trade = list()
                
                if other_sp[1] in ['S', 's', 'P', 'p']:
                    tran_idx = 1
                else:
                    tran_idx = 2

                ticker = other_sp[0].replace(')','')
                ticker = ticker.upper()
                trade.append(ticker)

                trade.append(other_sp[tran_idx])

                date_arr = other_sp[tran_idx+1].split('/')
                date = [date_arr[2], date_arr[0], date_arr[1]]
                trade.append(date)

                trades.append(trade)

            except:
                pass
        '''

    try:
        cont = raw['content']
        cont = cont.replace('(partial)','')
        cont = cont.replace('\n', ' ')
        cont = cont.replace('  ', ' ')
        cont_sp = cont.split('(')

    except:
        pass

    for line in cont_sp:

        try:
            other_sp = line.split(' ')

            if other_sp[1] in ['S', 's', 'P', 'p'] or other_sp[2] in ['S', 's', 'P', 'p']:

                    trade = list()
                    
                    if other_sp[1] in ['S', 's', 'P', 'p']:
                        tran_idx = 1
                    else:
                        tran_idx = 2

                    ticker = other_sp[0].replace(')','')
                    ticker = ticker.upper()
                    trade.append(ticker)

                    trade.append(other_sp[tran_idx])

                    date_arr = other_sp[tran_idx+1].split('/')
                    date = [date_arr[2], date_arr[0], date_arr[1]]
                    trade.append(date)

                    trades.append(trade)

        except:
            pass

    return name, trades


def get_all_trades():

    trades_per_rep = dict()
    trade_num = 0
    dir_list = get_all_pdf_nums()

    for pdf_name in dir_list:

        name, trades = parse_pdf_for_trades(pdf_name)
        print(trades)
        print(name)
        print('')
        try:
            trade_num += len(test)
        except:
            pass

        if trades != None and name != None:
            if name in trades_per_rep.keys():
                trades_per_rep[name] += trades
            else:
                trades_per_rep[name] = trades

    print('Trades: {0}'.format(trade_num))
    return trades_per_rep


trade_dict = get_all_trades()
print(trade_dict)
print(trade_dict.keys())
#name, test = parse_pdf_for_trades('20010637.pdf')
#print(test)
#print(name)
#print('')
