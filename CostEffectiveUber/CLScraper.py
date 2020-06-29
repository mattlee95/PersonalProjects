import requests
import re


MODEL = None
LOCALITY = None


def scrape_search_for_listings(search_url):
    '''
    Function takes in a string url which is a page of listings on CL
    Function returns list of strings of urls which are presumed to be listings
    '''
    global LOCALITY

    res = requests.get(search_url)

    listing_links = re.findall('sfbay*.html', res.content)

    listing_links = list()
    cont_lines = res.content.split('\n')

    # Scraping through the raw html contents of the webpage for all links
    # With the idea of grabbing all listings on that page of listings
    for line in cont_lines:

        # To make sure the link is a listing making sure the link matches the following criteria
        if line.find('https://{0}.craigslist.org'.format(LOCALITY)) >= 0 and line.find('html') >= 0:

            # Grabbing just the link part from the line
            new_listing = line[line.find('https://{0}.craigslist.org'.format(LOCALITY)) : line.find('html') + 4]
            if ('/d/' in new_listing) and (new_listing not in listing_links):

                listing_links.append(new_listing)

    print search_url
    print listing_links
    return listing_links


def scrape_listing_for_details(listing_url):
    '''
    Function takes in a string url for an actual CL listing
    Function returns a tuple of the pertinent details for the listed car:
        (model_year, miles, title, price)
    '''
    global MODEL

    if (MODEL.lower() not in listing_url.lower()):
        return (0, 0, 0, 0)

    res = requests.get(listing_url)

    model_year = 0
    miles = 0
    title = None
    price = 0

    # Get model year from URL (generally has it)
    for i in range(2000,2021):

        strI = '-' + str(i)
        strI2 = str(i) + '-'
        if strI in listing_url:

            model_year = i

    cont_lines = res.content.split('\n')

    for line in cont_lines:

        # Get car price
        if "price" in line:

            try:
                line_sp = line.split('$')[1]
                price = int(line_sp[0 : line_sp.find('</span>')])
            except:
                pass

        # Get car milage, look for odometer section in listing, see if filled
        if "<span>odometer:" in line:

            try:
                miles = int(line[line.find('<b>') + 3 : line.find('</b>')])
                if miles < 500:
                    miles = miles * 1000
            except:
                pass

        # Get car title status, look for title section in listing see if filled
        if "<span>title status:" in line:

            title = line[line.find('<b>') + 3 : line.find('</b>')]

    print "Model Year: {0}, Miles: {1}, Title: {2}, Price: {3}\n{4}".format(model_year, miles, title, price, listing_url)

    return (model_year, miles, title, price)


def scrape_for_model(model, locality):
    global MODEL
    global LOCALITY

    LOCALITY = locality
    MODEL = model

    # Specific URL formatting for page 1
    page1p1 = 'https://{0}.craigslist.org/search/cta?query='.format(LOCALITY) #Car model
    page1p2 = '&sort=rel'

    # URL formatting for pages after 1
    pageNp1 = 'https://{0}.craigslist.org/search/cta?s='.format(LOCALITY) #Page Number - 1 * 120
    pageNp2 = '&query=' #Car model
    pageNp3 = '&sort=rel'

    all_data = list()

    listing_list = list()
    last_listing_num = 0

    print "SCRAPING P1"

    # Using page 1 specific format for scrape listing page 1 for listing urls
    listing_list = scrape_search_for_listings(page1p1 + model + page1p2)
    last_listing_num = len(listing_list)

    # Go through collected listing URLS and scrape them for data
    for l in listing_list:

        listing_data = scrape_listing_for_details(l)

        if (listing_data[0] > 0) and (listing_data[1] > 0) and (listing_data[3] > 500):

            all_data.append(listing_data)

    p = 120

    # Continue for all pages after page 1, once we see a page with less than
    # 10 possible listings gathered, we know we are at the end
    while (last_listing_num > 10):

        print "SCRAPING P{0}".format((p + 120) / 120)

        listing_list = scrape_search_for_listings(pageNp1 + str(p) + pageNp2 + model + pageNp3)
        last_listing_num = len(listing_list)

        for l in listing_list:

            listing_data = scrape_listing_for_details(l)

            if (listing_data[0] > 0) and (listing_data[1] > 0) and (listing_data[3] > 500):

                all_data.append(listing_data)

        p += 120

    print all_data
    return all_data


#scrape_for_model('prius', 'sfbay')
