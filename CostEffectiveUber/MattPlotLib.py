import datetime
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import polyfit
from numpy.polynomial import Polynomial

class matplot_graph:

    def __init__(self, title_i, x_label_i, y_label_i, x_range_i, y_range_i):
        self.title = title_i
        self.x = list()
        self.y = list()
        self.x_label = x_label_i
        self.y_label = y_label_i
        self.x_range = x_range_i
        self.y_range = y_range_i


    def add_point(self, x_in, y_in):
        self.x.append(x_in)
        self.y.append(y_in)


def add_plot_to_pdf(graph_list, pdf_name, pdf_title):

    # Using this to bubble up the slopes to the caller
    slope_list = list()

    with PdfPages(pdf_name + '.pdf') as pdf:

        for graph in graph_list:

            plt.figure(figsize=(8,5))

            x_numpy = np.array(graph.x)

            b, m = polyfit(graph.x, graph.y, 1)
            slope_list.append(m)

            plt.title(graph.title + " Depreciation/Mile Driven: {0}".format(m))
            plt.xlabel(graph.x_label)
            plt.ylabel(graph.y_label)
            plt.xlim(0, graph.x_range)
            plt.ylim(0, graph.y_range)

            plt.plot(graph.x, graph.y, '.')

            plt.plot(graph.x, b + m * x_numpy, '-')

            pdf.savefig()
            plt.close()

        d = pdf.infodict()
        d['Title'] = pdf_title
        d['Author'] = "Matthew Lee"

        return slope_list
