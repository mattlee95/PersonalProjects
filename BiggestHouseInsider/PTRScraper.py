import urllib.request
import os 


START_YEAR = 2015
DISCLOSURE_URL_FORMAT = "https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{0}/{1}.pdf"


def download_and_save_pdfs(pdf_years):
    global START_YEAR
    global DISCLOSURE_URL_FORMAT

    year = START_YEAR

    for i in range(len(pdf_years)):

        for pdf_num in pdf_years[i]:

            if not (check_for_pdf(pdf_num)):

                url = DISCLOSURE_URL_FORMAT.format(year+i,pdf_num)

                try:
                    download_url(url, pdf_num)
                except:
                    print("Downloading {0} failed".format(DISCLOSURE_URL_FORMAT.format(year+i,pdf_num)))

            else:
                print("{0}.pdf already exists".format(pdf_num))


def download_url(url, pdf_num):

    file_path = os.path.dirname(os.path.realpath(__file__))
    file_path += "/pdfs/{0}.pdf".format(pdf_num)

    urllib.request.urlretrieve(url, file_path)
    print("Downloading: {0}...".format(url))


def check_for_pdf(pdf_num):

    if (str(pdf_num)[0] != '2'):
        return True

    file_path = os.path.dirname(os.path.realpath(__file__))
    file_path += "/pdfs/{0}.pdf".format(pdf_num)

    return os.path.exists(file_path)


def read_pdf_maps():
    global START_YEAR

    pdf_years = list()
    year = START_YEAR

    while (1):

        pdfs = list()
        pwd = os.path.dirname(os.path.realpath(__file__))
        try:
            pdf_map = open(pwd + "/pdf_map/{0}FD.txt".format(year), "r")
        except:
            return pdf_years

        cont = pdf_map.read()
        cont_lines = cont.split('\n')
        for line in cont_lines:
            line_sp = line.split('\t')
            try:
                if "P" in line_sp:
                    pdfs.append(int(line_sp[len(line_sp)-1]))
            except:
                pass
        
        pdf_years.append(pdfs)
        year += 1


l = read_pdf_maps()
download_and_save_pdfs(l)
