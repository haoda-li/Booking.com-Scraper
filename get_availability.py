from selenium.common import exceptions
import json

def process_info(table):
    rooms = []
    for row in table:
        if len(row) >= 5:
            rooms.append({
                'type': row[0].split("\n")[0].replace("\n", ""),
                'price': row[2].split("\n")[0].replace("\n","").replace("US$", ""),
                'left': row[4].split("\n")[-4].replace("\n", "")
            })
            
    return rooms

            
def get_availabilities_from_listings(filename, date_in, date_out, driver):
    """ Open filename, read the formated links, 
       and write the availablity of each listing to txt files"""
    
    # format check-in check-out information
    year_in, month_in, day_in = date_in.split("-")
    year_out, month_out, day_out = date_out.split("-")
    
    # read all the links that will be processed
    f = open(filename, "r")
    links = [l[:-1] for l in f]

    # initialize how the files will be splited
    files = 0
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
            
        # main scraping process
        try:
            driver.get("https://www.booking.com/hotel/"+address+".en-gb.html?"+\
                       "checkout_year=" +year_out+\
                       "&checkout_month="+month_out+\
                       "&checkout_monthday="+day_out+\
                       "&checkin_year="+year_in+\
                       "&checkin_month="+month_in+\
                       "&checkin_monthday="+day_in+\
                       "&selected_currency=USD"+\
                       "&changed_currency=1"+\
                       "&top_currency=1&lang=en-gb"+\
                       "&group_adults=1&no_rooms=1")
            table = driver.find_element_by_css_selector(".hprt-table.hprt-table-long-language ")
            tbody = table.find_element_by_css_selector("tbody")
            trs = tbody.find_elements_by_css_selector("tr")
            trd = [tr.find_elements_by_css_selector("td") for tr in trs]
            table_info = [[td.text for td in tds] for tds in trd]
            info.append({
                'link': address, 
                'rooms': process_info(table_info)
            })
        except exceptions.NoSuchElementException:
            continue