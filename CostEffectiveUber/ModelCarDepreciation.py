import CLScraper
from MattPlotLib import *
import os

MODELS = ['prius', 'camry', 'civic', 'accord', 'rav4', 'altima', 'escape', 'pilot', 'fusion', 'egde', 'rdx', 'mdx', 'corolla']
LOCALITIES = ['sfbay', 'sacramento', 'losangeles', 'sandiego', 'orangecounty', 'lasvegas']
#LOCALITIES = ['sacramento']
#MODELS = ['rav4']

def remove_salvage(raw_data):
    '''
    Function returns new list of data with salvage data-points removed
    Trying to isolate the regression model to a single variable (miles)
    '''

    ret_list = list()

    for elem in raw_data:

        if 'clean' in elem:

            ret_list.append(elem)

    return ret_list


def get_data_mod_loc(model, locality):
    '''
    Function returns list of data of all listings for a specific car model
    and locatlity in which it is being sold
    '''

    raw_data = CLScraper.scrape_for_model(model, locality)

    raw_data = remove_salvage(raw_data)

    return raw_data


def car_dep_model(model):
    '''
    Function collects data for a car model for various localities on CL
    Returns the data
    '''
    global LOCALITIES

    car_data = []

    for loc in LOCALITIES:

        car_data = car_data + get_data_mod_loc(model, loc)

    return car_data


def plot_car_dep(model):

    raw_data = car_dep_model(model)

    # Going to use this list to track depreciation per model
    # Format [[model, year, samples, depreciation],...]
    deprec_list = list()
    graph_list = list()

    for i in range(2000, 2021):

        graph = matplot_graph("Car: {0}, Year: {1} Depreciation".format(model, i), "Mileage", "Price", 300000, 40000)

        for elem in raw_data:

            if elem[0] == i:

                graph.add_point(elem[1], elem[3])

        if (len(graph.x) > 0):
            graph_list.append(graph)
            deprec_list.append([model, i, len(graph.x), 0])

    if (len(graph_list) > 0):

        slope_list = add_plot_to_pdf(graph_list, "{0}Depreceation".format(model), "Car: {0} Depreciation As Mileage Increases".format(model))

    for i in range(len(deprec_list)):
        deprec_list[i][3] = slope_list[i]

    return deprec_list


def rank_depreciation(dep_list):

    dep_list.sort(key=lambda x: x[3], reverse=True)

    print "CAR DEPRECIATION RANKING"

    for i in range(len(dep_list)):

        print "Rank {0}: {1} {2}, Depreciation Per Mile (in Dollars): {3} with {4} samples".format(i+1, dep_list[i][1], dep_list[i][0], dep_list[i][3], dep_list[i][2])


def main():

    deprec_list = []

    for model in MODELS:

        model_dep = plot_car_dep(model)
        deprec_list += model_dep

    rank_depreciation(deprec_list)

main()
