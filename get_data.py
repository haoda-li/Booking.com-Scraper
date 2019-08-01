from utilities import *

def get_links_by_location_file(driver_link, r_file, w_file):
    driver = prepare_driver(driver_link)
    f = open(r_file, "r")
    urls = set()
    for line in f:
        print("==== JOB ON " + line[:-1] + " ====")
        urls |= get_link_by_search_query(line[:-1], driver)
        print("==== COLLECTED " + str(len(urls)) + " URLS ====")
    
    with open(w_file, "w") as f:
        for e in urls:
            f.write(e + "\n")
            

            
def get_availabilities_by_url_file(filename, date_in, date_out, driver_link, page=0):
    """ Open filename, read the formated links, 
       and write the availablity of each listing to json files
    """
    
    driver = prepare_driver(driver_link)
    
    # read all the links that will be processed
    f = open(filename, "r")
    links = [l[:-1] for l in f]
    links = links[page*200:]
    # initialize how the files will be splited
    files = page
    info = []
    index = 0
    
    
    for address in links:
        index += 1
        
        # when a certain number of links are scraped, store them as a file
        if index == 200:
            with open("./avalibility/"+date_in+"_"+str(files)+".json", "w") as fw:
                json.dump(info, fw, indent=2)
            print("---write to: "+date_in+"_"+str(files)+".json---")
            
            info.clear()
            index = 0
            files += 1
            
        availability = get_availabilities_by_url(address, date_in, date_out, driver)
        if availability:
            info.append(availability)
    with open("./avalibility/"+date_in+"_"+str(files)+".json", "w") as fw:
        json.dump(info, fw, indent=2)
    print("---write to: "+date_in+"_"+str(files)+".json---")
            
            
def get_listings_information_by_url_file(filename, page=0):
    """ Open filename, read the formated links, 
       and write the information of each listing to json files
    """
    
    f = open(filename, "r")
    links = [l[:-1] for l in f]
    links = links[(page+1) * 200:]
    
    files = page
    info = []
    index = 0
    
    for address in links:
        index += 1
        
        # when a certain number of links are scraped, store them as a file
        if index == 200:
            with open("./information/i"+str(files)+".json", "w") as fw:
                json.dump(info, fw, indent=2)
            print("---write to: i"+str(files)+".json---")
            
            info.clear()
            index = 0
            files += 1
        gotten = get_listing_information_by_url(address)
        if gotten:
            info.append(gotten)
    with open("./information/i"+str(files)+".json", "w") as fw:
        json.dump(info, fw, indent=2)
    print("---write to: i"+str(files)+".json---")