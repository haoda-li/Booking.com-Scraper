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
            driver.get("https://www.booking.com/hotel/"+address+"?label=gen173nr-1FCAEoggI46AdIM1gEaCeIAQGYAQm4ARnIAQzYAQHoAQH4AQuIAgGoAgO4ArOF6ukFwAIB;sid=586f4aac96691ec9be6e32c8ed90589b;all_sr_blocks=7591018_189982941_4_42_0;checkin=2019-07-26;checkout=2019-07-27;dest_id=20126394;dest_type=city;dist=0;group_adults=2;hapos=1;highlighted_blocks=7591018_189982941_4_42_0;hpos=1;room1=A%2CA;sb_price_type=total;sr_order=popularity;srepoch=1564115654;srpvid=6d6b2022cbc302c7;type=total;ucfs=1&#hotelTmpl")
            table = driver.find_element_by_css_selector(".hprt-table.hprt-table-long-language ")
            tbody = table.find_element_by_css_selector("tbody")
            trs = tbody.find_elements_by_css_selector("tr")
            trd = [tr.find_elements_by_css_selector("td") for tr in trs]
            table_info = [[td.text for td in tds] for tds in trd]
            process_info(table_info, fw)
        except exceptions.NoSuchElementException:
            continue
    fw.close()