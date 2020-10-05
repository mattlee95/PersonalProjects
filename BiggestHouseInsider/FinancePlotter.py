import datetime
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import numpy as np


class matplot_graph:

    def __init__(self, title_i, perf, perf_a, x_label_i, y_label_i, x_range_i, y_range_i):
        self.title = title_i

        self.performance = list(perf)
        self.performance_a = list(perf_a)

        self.x = list(range(1,25))

        self.x_label = x_label_i
        self.y_label = y_label_i
        self.x_range = x_range_i
        self.y_range = y_range_i


class matplot_bar:

    def __init__(self, title_i, sales_i, buys_i, x_label_i, y_label_i, x_range_i, y_range_i):
        self.title = title_i

        self.x = list(range(84))

        self.sales = list(sales_i)
        self.buys = list(buys_i)

        self.x_label = x_label_i
        self.y_label = y_label_i
        self.x_range = x_range_i
        self.y_range = y_range_i


def add_plot_to_pdf(graph_list, pdf_name, pdf_title):

    with PdfPages(pdf_name + '.pdf') as pdf:

        for graph in graph_list:

            if graph.performance[0] != None:

                plt.figure(figsize=(8,5))

                plt.title(graph.title)
                plt.xlabel(graph.x_label)
                plt.ylabel(graph.y_label)

                plt.xlim(1, graph.x_range)
                plt.ylim(-100, graph.y_range)

                plt.plot(graph.x, graph.performance, 'g-', label="True Performance")
                plt.plot(graph.x, graph.performance_a, 'b-', label="Performance Relative to SPY")

                plt.legend(loc='upper left')
                plt.grid()

                pdf.savefig()
                plt.close()

        d = pdf.infodict()
        d['Title'] = pdf_title
        d['Author'] = "Matthew Lee"


def add_bar_to_pdf(graph_list, pdf_name, pdf_title):

    with PdfPages(pdf_name + '.pdf') as pdf:

        for graph in graph_list:

            if sum(graph.sales) != 0 and sum(graph.buys) != 0:

                plt.figure(figsize=(8,5))

                plt.title(graph.title)
                plt.xlabel(graph.x_label)
                plt.ylabel(graph.y_label)

                plt.xlim(0, 83)
                plt.ylim(0, 25)

                plt.plot(graph.x, graph.buys, 'g-', label="Purchases")
                plt.plot(graph.x, graph.sales, 'r-', label="Sales")

                plt.legend(loc='upper left')
                plt.grid()

                pdf.savefig()
                plt.close()

        d = pdf.infodict()
        d['Title'] = pdf_title
        d['Author'] = "Matthew Lee"


def get_bar_from_transactions(tran_list, rep):

    #categories = [elem * 2 for elem in c]

    sales = [0] * 84
    buys = [0] * 84

    for t in tran_list:
        
        idx = (int(t[2][0]) - 2014) * 12
        idx += (int(t[2][1]))
        idx -= 1

        if t[1] in ['S', 's']:
            sales[idx] = sales[idx] + 1

        else:
            buys[idx] = buys[idx] + 1

    ret = matplot_bar("{0} Transaction Timing".format(rep), sales, buys, "Months Since 2014 Jan", "Number of Transactions", 0, 0) 
    return ret


'''
test_list_a = [-2.436409769017922, 1.3922383610301736, 3.186085846644482, 1.9277163013502685, -3.721550400083007, -6.104412642806567, -11.99464321256456, -11.99464321256456, -11.99464321256456, -11.99464321256456, -11.99464321256456, -0.7496600133686693, 4.337357661973651, 0.5890281439907996, 3.025440590385031, 2.838024248354709, 8.862120956472342, 11.593044797485664, 15.207500144979914, 15.207500144979914, 15.207500144979914, 15.207500144979914, 15.207500144979914, 19.919687813637886]
test_list_b = [-1.38933646392837, -1.7308401246158622, -2.0347891311795596, -3.3949576265613457, -2.772637070190409, -2.785025113874917, -1.4256582031923823, -1.4256582031923823, -1.4256582031923823, -1.4256582031923823, -1.4256582031923823, -3.3964512577296935, -3.802985903502166, -4.151931161195566, -4.878584840803146, -3.858944958566335, -2.9684587271013854, -1.9245064194225883, -2.4220301642524653, -2.4220301642524653, -2.4220301642524653, -2.4220301642524653, -2.4220301642524653, 4.584285217655946]

x = matplot_graph("Nancy Pelosi Transaction Performance (Sell)", test_list_a, test_list_b, "Time (Months)", "Performance (%)", 24, 200)

print(x.title)

add_plot_to_pdf([x], "pdf_name", "title")
'''
