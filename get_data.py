from utilities import *
from progress import printProgressBar
from datetime import date
from datetime import timedelta

def get_links_by_location_file(driver_link, r_file, w_file):
    driver = prepare_driver(driver_link)
    line_count = 0
    with open(r_file, "r") as f:
        line_count = sum([1 for line in f])
        print("\nJOB STARTING, TOTAL OF " + str(line_count) + " QUERIES LOADED")
    f = open(r_file, "r")
    urls = set()
    current_line = 0
    for line in f:
        printProgressBar(current_line, line_count, prefix="Progress:", suffix=str(len(urls)) + " collected")
        urls |= get_link_by_search_query(line[:-1], driver)
        current_line += 1
    f.close()
    with open(w_file, "w") as f:
        for e in urls:
            f.write(e + "\n")
            

            
def get_availabilities_by_url_file(filename, date_in, date_out, driver_link, folder_out):
    """ Open filename, read the formated links, 
       and write the availablity of each listing to json files
    """
    
    driver = prepare_driver(driver_link)
    
    # read all the links that will be processed
    f = open(filename, "r")
    links = [l[:-1] for l in f]
    # initialize how the files will be splited
    files, index = 0, 0
    info = []
    
    print("\nJOB STARTING, TOTAL OF " + str(len(links)) + " LINKS LOADED")
    for address in links:
        index += 1
        printProgressBar(index, len(links), prefix="Progress:", suffix=str(index) +"/"+ str(len(links)))
        # when a certain number of links are scraped, store them as a file
        if index % 200 == 0:
            with open(folder_out+date_in+"_"+str(files)+".json", "w") as fw:
                json.dump(info, fw, indent=2)
            info.clear()
            files += 1
            
        availability = get_availabilities_by_url(address, date_in, date_out, driver)
        if availability:
            info.append(availability)
    f.close()
    with open(folder_out+date_in+"_"+str(files)+".json", "w") as fw:
        json.dump(info, fw, indent=2)
            
            
def get_listings_information_by_url_file(filename, folder_out):
    """ Open filename, read the formated links, 
       and write the information of each listing to json files
    """
    
    f = open(filename, "r")
    links = [l[:-1] for l in f]
    files, index = 0, 0
    info = []
    print("\nJOB STARTING, TOTAL OF " + str(len(links)) + " LINKS LOADED")
    for address in links:
        index += 1
        printProgressBar(index, len(links), prefix="Progress:", suffix=str(index) +"/"+ str(len(links)))
        # when a certain number of links are scraped, store them as a file
        if index % 200 == 0:
            with open(folder_out + "info"+str(files)+".json", "w") as fw:
                json.dump(info, fw, indent=2)
            info.clear()
            files += 1

        gotten = get_listing_information_by_url(address)
        if gotten:
            info.append(gotten)
    with open(folder_out + "info"+str(files)+".json", "w") as fw:
        json.dump(info, fw, indent=2)
