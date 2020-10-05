import YahooFinanceCacher
import CSVWriter


def find_portfolio_performace(transaction_list, rep):

    perf_list = list()
    perf_a_list = list()

    for transaction in transaction_list:

        perf, perf_a = find_stock_performance(transaction)
        print(perf)
        print(perf_a)
        print(' ')
        perf_list.append(perf)
        perf_a_list.append(perf_a)

    avg_sell_perf, avg_buy_perf, avg_sell_perf_a, avg_buy_perf_a = find_avg_performance(transaction_list, perf_list, perf_a_list)

    CSVWriter.write_csv(rep, transaction_list, perf_list, perf_a_list)

    print("Average Stock Performance After Sale: {0}\n".format(avg_sell_perf))
    print("Average Stock Performance After Sale (Alpha): {0}\n".format(avg_sell_perf_a))
    print("Average Stock Performance After Buy: {0}\n".format(avg_buy_perf))
    print("Average Stock Performance After Buy (Alpha): {0}\n".format(avg_buy_perf_a))

    return avg_sell_perf, avg_buy_perf, avg_sell_perf_a, avg_buy_perf_a


def find_avg_performance(transaction_list, performance_list, performance_list_a):

    avg_sell_perf = [None] * 24
    avg_buy_perf = [None] * 24

    avg_sell_perf_a = [None] * 24
    avg_buy_perf_a = [None] * 24

    sell_signal = ['S', 's']
    buy_signal = ['P', 'p']

    #increment through months
    for month in range(24):
        sell_sum = 0
        sell_sum_a = 0
        sell_n = 0

        buy_sum = 0
        buy_sum_a = 0
        buy_n = 0

        #increment through transactions
        for i in range(len(transaction_list)):
            
            #check for signal
            if transaction_list[i][1] in sell_signal:
                if performance_list[i][month] != None:
                    sell_sum += performance_list[i][month]
                    sell_sum_a += performance_list_a[i][month]
                    sell_n += 1

            else:
                if performance_list[i][month] != None:
                    buy_sum += performance_list[i][month]
                    buy_sum_a += performance_list_a[i][month]
                    buy_n += 1

        if sell_n > 0:
            avg_sell_perf[month] = sell_sum / sell_n
            avg_sell_perf_a[month] = sell_sum_a / sell_n

        if buy_n > 0:
            avg_buy_perf[month] = buy_sum / buy_n
            avg_buy_perf_a[month] = buy_sum_a / buy_n

    return avg_sell_perf, avg_buy_perf, avg_sell_perf_a, avg_buy_perf_a

def find_stock_performance(transaction):

    ticker = transaction[0]
    year = int(transaction[2][0])
    month = int(transaction[2][1])
    day = int(transaction[2][2])

    print("${0} {1}-{2}-{3}".format(ticker, year, month, day))

    perf, perf_a = YahooFinanceCacher.month_by_month_performance(ticker, year, month, day)

    return perf, perf_a




















example_list = [['AAPL', 'P', ['2016', '05', '17']], ['SQ', 'P', ['2016', '05', '17']], ['AAPL', 'P', ['2017', '06', '15']], ['BFET', 's', ['2017', '06', '20']], ['AMZN', 'P', ['2018', '07', '27']], ['FB', 'P', ['2018', '07', '27']], ['DBX', 'P', ['2018', '03', '27']], ['AMZN', 'P', ['2020', '01', '16']], ['AMZN', 's', ['2020', '01', '16']], ['AMZN', 's', ['2020', '01', '16']], ['FB', 'P', ['2020', '01', '16']], ['FB', 'P', ['2020', '01', '16']], ['V', 'S', ['2019', '08', '07']], ['V', 'S', ['2019', '08', '07']], ['CRM', 'P', ['2019', '06', '14']], ['CRM', 'P', ['2019', '06', '18']], ['HTZ', 'P', ['2014', '11', '5']], ['HTZ', 'P', ['2014', '11', '25']], ['HTZ', 'P', ['2014', '11', '6']], ['HTZ', 'P', ['2014', '11', '28']], ['DIS', 'P', ['2014', '12', '10']], ['DIS', 'P', ['2014', '11', '28']], ['AAPL', 's', ['2017', '12', '21']], ['AAPL', 's', ['2017', '12', '28']], ['AAPL', 's', ['2017', '12', '29']], ['V', 's', ['2017', '12', '28']], ['V', 's', ['2017', '12', '21']], ['AAPL', 'P', ['2018', '02', '2']], ['AAPL', 'P', ['2018', '02', '2']], ['BFET', 's', ['2019', '02', '07']], ['CRM', 'S', ['2015', '12', '30']], ['V', 'S', ['2015', '12', '30']], ['V', 'S', ['2015', '12', '29']], ['AMZN', 'P', ['2018', '10', '12']], ['T', 'P', ['2018', '10', '24']], ['FB', 'P', ['2018', '10', '09']], ['AAPL', 'P', ['2017', '01', '19']], ['AAPL', 's', ['2017', '01', '20']], ['SQ', 'P', ['2017', '01', '20']], ['AAPL', 'S', ['2020', '05', '08']], ['AAPL', 'S', ['2020', '05', '08']], ['AAPL', 'S', ['2020', '05', '08']], ['FB', 'S', ['2020', '05', '08']], ['IBKR', 'S', ['2020', '05', '08']], ['MORN', 'S', ['2020', '05', '08']], ['V', 'S', ['2020', '05', '08']], ['V', 'S', ['2020', '05', '08']], ['HTZ', 'P', ['2015', '07', '15']], ['HTZ', 'P', ['2015', '07', '16']], ['V', 'S', ['2019', '08', '07']], ['V', 's', ['2014', '12', '29']], ['V', 's', ['2014', '12', '30']], ['DIS', 'P', ['2014', '12', '10']], ['AMZN', 'S', ['2020', '01', '16']], ['AMZN', 'S', ['2020', '01', '16']], ['AXP', 'P', ['2020', '06', '24']], ['AAPL', 'S', ['2020', '06', '18']], ['NFLX', 'P', ['2020', '06', '18']], ['PYPL', 'P', ['2020', '06', '12']], ['PYPL', 'P', ['2020', '06', '12']], ['PYPL', 'P', ['2020', '06', '24']], ['CRM', 'P', ['2020', '06', '18']], ['GOOGL', 'P', ['2020', '02', '27']], ['MSFT', 'P', ['2020', '02', '28']], ['MSFT', 'P', ['2020', '02', '20']], ['MSFT', 'P', ['2020', '02', '21']], ['WORK', 'P', ['2020', '02', '20']], ['AMZN', 'P', ['2019', '07', '22']], ['NFLX', 'P', ['2019', '07', '22']], ['NFLX', 'P', ['2019', '07', '05']], ['AAPL', 'P', ['2018', '09', '11']], ['AAPL', 'P', ['2018', '09', '20']], ['AAPL', 'P', ['2018', '09', '20']], ['MGRC', 'S', ['2016', '07', '21']], ['V', 'S', ['2016', '07', '21']], ['AAPL', 'P', ['2016', '01', '13']], ['DIS', 'P', ['2016', '01', '15']]]
#find_portfolio_performace(example_list, 'Hon. Katherine M. Clark')
