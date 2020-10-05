'''
<MemberName.csv>

Ticker, Date, Purchase/Sale, 1 Month, 1 Month Alpha, ...

'''
import os


def write_csv(rep, transaction_list, perf, perf_a):

    csv = open_csv(rep)

    write_header(csv)

    for i in range(len(transaction_list)):

        write_line(csv, transaction_list[i], perf[i], perf_a[i])

    csv.close()


def open_csv(rep):

    f_name = rep.replace(' ', '')
    f_name = f_name.replace('.', '')

    file_path = os.path.dirname(os.path.realpath(__file__))
    file_path += "/csv/{0}.csv".format(f_name)

    csv = open(file_path, 'w')
    return csv


def write_header(csv):

    MONTHS = 24
    header = "Ticker, Date, Purchase/Sale"

    for i in range(1, MONTHS+1):
        header += ", {0} Month(s), {0} Month(s) Alpha".format(i)
    
    header += '\n'
    csv.write(header)


def write_line(csv, transaction, perf, perf_a):

    MONTHS = 24
    ticker = transaction[0]
    year = int(transaction[2][0])
    month = int(transaction[2][1])
    day = int(transaction[2][2])
    t_type = transaction[1]

    line = "${0}, {1}-{2}-{3}, {4}".format(ticker, month, day, year, t_type)

    for i in range(MONTHS):
        line += ", {0}, {1}".format(perf[i], perf_a[i])

    line += '\n'
    csv.write(line)
