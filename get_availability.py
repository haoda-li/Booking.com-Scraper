from selenium.common import exceptions

def process_info(table, fw):
    for row in table:
        if len(row) >= 5:
            roomtype = row[0].split("\n")[0].replace("\n", "")
            price = row[2].split("\n")[0].replace("\n","")
            left = row[4].split("\n")[-4].replace("\n", "")
            fw.write(roomtype+"|"+price+"|"+left+"\n")
            
def get_availabilities_from_listings(filename, date_in, driver):
    """ Open filename, read the formated links, 
       and write the availablity of each listing to txt files"""
    f = open(filename, "r")
    links = [l[:-1] for l in f]

    files = 0
    index = 0

    fw = open("./avalibility/"+date_in+"_"+str(files)+".txt", "w")
    print("---write to a"+date_in+str(files)+".txt---")

    for address in links:
        index += 1
        if index == 100:
            index = 0
            fw.close()
            files += 1
            fw = open("./avalibility/"+date_in+"_"+str(files)+".txt", "w")
            print("---write to a"+date_in+str(files)+".txt---")

        fw.write("------" + address + "\n")
        try:
            driver.get("https://www.booking.com/hotel/"+address+".en-gb.html?checkout_year=2019&checkout_month=07&checkout_monthday=28&checkin_year=2019&checkin_month=07&checkin_monthday=27&selected_currency=USD&changed_currency=1&top_currency=1&lang=en-gb&group_adults=1&no_rooms=1")
            table = driver.find_element_by_css_selector(".hprt-table.hprt-table-long-language ")
            tbody = table.find_element_by_css_selector("tbody")
            trs = tbody.find_elements_by_css_selector("tr")
            trd = [tr.find_elements_by_css_selector("td") for tr in trs]
            table_info = [[td.text for td in tds] for tds in trd]
            process_info(table_info, fw)
        except exceptions.NoSuchElementException:
            continue
    fw.close()