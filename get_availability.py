from selenium.common import exceptions

def get_availabilities_from_listings(filename, date_in, date_out, driver):
    """ Open filename, read the formated links, 
       and write the availablity of each listing to txt files"""
    f = open(filname, "r")
    links = [l[:-1] for l in f]

    files = 0
    index = 0

    fw = open("./avalibility/a"+str(files)+".txt", "w")

    for address in links:
        index += 1
        if index == 100:
            index = 0
            fw.close()
            files += 1
            fw = open("./avalibility/a"+str(files)+".txt", "w")
            print("---write to a"+str(files)+".txt---")

        fw.write("------" + address + "\n")
        try:
            driver.get("https://www.booking.com"+address+"?label=gen173nr-1FCAEoggI46AdIM1gEaCeIAQGYA"+\
                       "Qm4ARfIAQzYAQHoAQH4AQuIAgGoAgO4AtTm5-kFwAIB;sid=8020d5f8011367"+\
                       "d6f47868330f60750e;all_sr_blocks=206046901_117453847_4_0_0;checkin"+\
                       "="+date_in+";checkout="+date_out+";dest_id=20126394;dest_type=city;"+\
                       "dist=0;group_adults=2;hapos=1;highlighted_blocks=206046901_117453847_4_0_0;hpos"+\
                       "=1;room1=A%2CA;sb_price_type=total;sr_order=popularity;srepoch=1564078943;"+\
                       "srpvid=436e812f5cc300dd;type=total;ucfs=1&#hotelTmpl")
            table = driver.find_element_by_css_selector(".hprt-table.hprt-table-long-language ")
            tbody = table.find_element_by_css_selector("tbody")
            trs = tbody.find_elements_by_css_selector("tr")
            trd = [tr.find_elements_by_css_selector("td") for tr in trs]
            table_info = [[td.text for td in tds] for tds in trd]
            process_info(table_info, fw)
        except exceptions.NoSuchElementException:
            continue
    fw.close()