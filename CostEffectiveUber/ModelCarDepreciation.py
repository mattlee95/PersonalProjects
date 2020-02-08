import CLScraper
from MattPlotLib import *
import os

MODELS = ['prius', 'camry', 'civic', 'accord', 'rav4', 'altima', 'escape', 'pilot', 'fusion', 'egde', 'rdx', 'mdx', 'corolla']
LOCALITIES = ['sfbay', 'sacramento', 'losangeles', 'sandiego', 'orangecounty', 'lasvegas']
#LOCALITIES = ['sfbay']

def remove_salvage(raw_data):

    ret_list = list()

    for elem in raw_data:

        if 'clean' in elem:

            ret_list.append(elem)

    return ret_list


def get_data_mod_loc(model, locality):

    raw_data = CLScraper.scrape_for_model(model, locality)

    raw_data = remove_salvage(raw_data)

    return raw_data


def car_dep_model(model):
    global LOCALITIES

    car_data = []

    for loc in LOCALITIES:

        car_data = car_data + get_data_mod_loc(model, loc)

    return car_data


def plot_car_dep(model):

    raw_data = car_dep_model(model)

    graph_list = list()

    for i in range(2000, 2021):

        graph = matplot_graph("Car: {0}, Year: {1} Depreciation".format(model, i), "Mileage", "Price", 300000, 40000)

        for elem in raw_data:

            if elem[0] == i:

                graph.add_point(elem[1], elem[3])

        if (len(graph.x) > 0):
            graph_list.append(graph)

    if (len(graph_list) > 0):

        add_plot_to_pdf(graph_list, "{0}Depreceation".format(model), "Car: {0} Depreciation As Mileage Increases".format(model))



for model in MODELS:
    plot_car_dep(model)

#get_data_mod_loc(MODELS[0], LOCALITIES[0])
