import PDFReader
import StockPerformanceAnalyzer
from FinancePlotter import *


def get_all_rep_performance(tranaction_map):

    performance_dict = dict()
    timing_graph_list = list()

    for rep in tranaction_map.keys():

        print("Gathering info for: {0}".format(rep))

        perf = get_performance_rep(tranaction_map[rep], rep)

        performance_dict[rep] = perf

        bar_graph = get_bar_from_transactions(tranaction_map[rep], rep)
        timing_graph_list.append(bar_graph)

    plot_performance(performance_dict, timing_graph_list)
    


def plot_performance(perf, bar_graph_list):

    ##### Performance Graph #####

    title = "House Member's Stock Performance Graphs"
    plot_title = "{0} Transaction Performance ({1})"
    x_label_i = "Time (Months)"
    y_label_i = "Performance (%)"
    x_range_i = 24
    y_range_i = 200

    graph_list = list()

    for rep in perf.keys():

        rep_perf = perf[rep]
        
        graph_b = matplot_graph("{0} Transaction Performance ({1})".format(rep, "Buy"), rep_perf[1], rep_perf[3], x_label_i, y_label_i, x_range_i, y_range_i)
        graph_s = matplot_graph("{0} Transaction Performance ({1})".format(rep, "Sell"), rep_perf[0], rep_perf[2], x_label_i, y_label_i, x_range_i, y_range_i)

        graph_list.append(graph_b)
        graph_list.append(graph_s)

    add_plot_to_pdf(graph_list, "MemberPerformance", title)

    ##### Timing Bar Graphs #####

    add_bar_to_pdf(bar_graph_list, "MemberActivity", "House Member's Transaction Timing Graphs")



def get_performance_rep(transaction_list, rep):

    avg_sell_perf, avg_buy_perf, avg_sell_perf_a, avg_buy_perf_a = StockPerformanceAnalyzer.find_portfolio_performace(transaction_list, rep)

    return [avg_sell_perf, avg_buy_perf, avg_sell_perf_a, avg_buy_perf_a]


def get_transaction_map():

    transaction_map = PDFReader.get_all_trades()
    return transaction_map


def main():

    tranaction_map = get_transaction_map()
    get_all_rep_performance(tranaction_map)


main()
