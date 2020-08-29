import requests
import appleRetailGlobal


def get_retail_traffic(store_str):

    url = "http://www.google.com/search?q=Apple+store+{0}".format(store_str.replace(" ","+"))

    res = requests.get(url)
    cont = res.content

    cont = cont.split('<div class="Hk2yDb KsR1A"')[1]

    reviews = cont[cont.find('(')+1:cont.find(')')]
    reviews = reviews.replace(',', '')

    print reviews
    return int(reviews)


def get_all_traffic():

    for i in range(len(appleRetailGlobal.storeIDs)):

        traffic = get_retail_traffic(appleRetailGlobal.storeIDs[i][0])
        appleRetailGlobal.storeIDs[i].append(traffic)

    print appleRetailGlobal.storeIDs


get_all_traffic()
