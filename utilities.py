import selenium
import time
import json

from bs4 import BeautifulSoup
from requests import get

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions 



def prepare_driver(path, headless=True):
    """ Initiate the Chrome driver installed in path
    """
    
    options = Options()
    # make the Chrome driver runs in the background
    if headless:
        options.add_argument('-headless')
    options.add_argument("--lang=en-US")
    options.add_argument('--disable-gpu')
    
    driver = webdriver.Chrome(path, options=options)
    return driver


def get_link_by_search_query(location, driver):
    """ Using a Chrome driver to search for the location
        return the urls of the search results
        
        NOTE: Booking.com only shows a max of 1000 results
    """
    
    # make the search query
    driver.get('https://www.booking.com/index.html?label=gen173nr-' + \
               '1FCAEoggI46AdIM1gEaCeIAQGYASu4ARnIAQzYAQHoAQH4AQuIAgGoAgO4Aqe03ukFwAIB' +\
               '&sid=189ec2c0f7b6489fda1f0d8b2eae9761&lang=en-us&selected_currency=USD')
    driver.find_element_by_css_selector("#ss").send_keys(location)
    driver.find_element_by_css_selector(".sb-searchbox__button").submit()
    driver.get(driver.current_url + "&rows=50")
    
    # collect all urls
    urls = set()
    while True:
        # since selenium is based on automation, 
        # setting a time interval allows data transmission 
        # and will reduce error rate
        time.sleep(2)
        
        try: 
            WebDriverWait(driver, timeout=10).\
              until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sr-hotel__name')))
            links = driver.find_elements_by_class_name('hotel_name_link')
            links = [e.get_attribute("href") for e in links]
            # collect the urls
            for e in links:
                start = e.find("/hotel")
                end = e.find(".html")
                wanted = e[start: end + 5]
                urls.add(wanted)
            
            WebDriverWait(driver, timeout=10).\
              until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'bui-pagination__next-arrow')))
            arrow = driver.find_element_by_class_name('bui-pagination__next-arrow')
            
            # when the end of pages reached
            if "bui-pagination__next-arrow bui-pagination__item--disabled" in arrow.get_attribute("class"):
                break
            
            # move to the next page
            webdriver.ActionChains(driver).move_to_element(arrow).click(arrow).perform()
        
        # if the HTML DOM haven't been updated
        except exceptions.StaleElementReferenceException as se:
            WebDriverWait(driver, timeout=10).\
              until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'bui-pagination__next-arrow')))
            arrow = driver.find_element_by_class_name('bui-pagination__next-arrow')
            webdriver.ActionChains(driver).move_to_element(arrow).click(arrow).perform()
        
        # if the number of results is fitted in one page
        except exceptions.TimeoutException as te:
            break
    return urls


def process_info(table):
    """ Helper of get_availabilities_by_url
        Parser information and 
        returns the room type, price, and number of rooms left.
    """
    rooms = []
    for row in table:
        if len(row) >= 5:
            rooms.append({
                'type': row[0].split("\n")[0].replace("\n", ""),
                'price': row[2].split("\n")[0].replace("\n","").replace("US$", ""),
                'left': row[4].split("\n")[-4].replace("\n", "")
            })
            
    return rooms

def get_availabilities_by_url(url, date_in, date_out, driver):
    """ Given the hotel url, and check in check out dates, 
        return the availabilitiy information as an json object.
    """
    
    year_in, month_in, day_in = date_in.split("-")
    year_out, month_out, day_out = date_out.split("-")
    
    try:
        driver.get("https://www.booking.com/hotel/"+url+".en-gb.html?"+\
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
        return {
            'link': url, 
            'rooms': process_info(table_info)
        }
    except exceptions.NoSuchElementException:
        return None

def get_listing_information_by_url(url):
    """ Given the hotel url, 
        return a json object representation of the hotel information 
    """
    
    r = get("https://www.booking.com/hotel/" + url+ ".en-gb.html")
    b = BeautifulSoup(r.content, "lxml")
    try:
        details = {
            'url': url, 
            'type': b.select("#hp_hotel_name")[0].get_text().split("\n")[1],
            'name': b.select("#hp_hotel_name")[0].get_text().split("\n")[2],
            'address': b.select(".hp_address_subtitle.js-hp_address_subtitle.jq_tooltip")[0].get_text().replace("\n", ""),
            'rating': -1,
            'number_reviews': -1,
            'last_reviewed': "",
            'room_types': [a.get_text().replace("\n", "") for a in b.select(".jqrt.togglelink")]
        }
        ratings_div = b.select(".bui-review-score__badge")
        if ratings_div:
            details['rating'] =  float(ratings_div[0].get_text())

        n_reviews_div = b.select(".bui-review-score__text")
        if n_reviews_div:
            details['number_reviews'] = int(n_reviews_div[0].get_text().replace(" reviews", "").replace(",",""))

        last_reviewed_div = b.select(".review_item_date")
        if last_reviewed_div:
            details['last_reviewed'] = last_reviewed_div[0].get_text().replace("\n", "").replace("Reviewed: ", "")
        coordinate =b.select("#hotel_header")[0].attrs['data-atlas-latlng']
        details['lat'], details['lng'] = [float(x) for x in coordinate.split(",")]
        return details
    except:
        return None