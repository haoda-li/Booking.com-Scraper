import selenium
import time

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


def get_links(location, driver):
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