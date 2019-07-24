from collect_hotel_urls import *

if __name__ == "__main__":
    
    driver = prepare_driver("./chromedriver.exe")
    f = open("TX_CITIES.txt", "r")
    urls = set()
    for line in f:
        print("==== JOB ON " + line[:-1] + " ====")
        urls |= get_links(line[:-1], driver)
        print("==== COLLECTED " + str(len(urls)) + " URLS ====")
    driver.quit()
    
    with open("links.txt", "w") as f:
        for e in urls:
            f.write(e + "\n")