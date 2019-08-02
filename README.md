# Booking.com Scraper

Scrape <a href="https://www.booking.com">Booking.com</a> hotels listings, information, and availabilities. 

The scraper is designated for reseach project on Texas hotel tax evasions. The research project is conducted and supervised by Yao Luo, under Department of Economics, University of Toronto. 

## Installations
Python ver. 3.6+

`pip install -r requirements.txt`

## Data Format
__Listings information (Delivered as csv and json)__
 - __url__ the compressed url. You can see the website details by `http://booking.com/hotel/`__url__`.en-gb.html`
 - __type__ whether the accommodation is a hotel, apartment, or other type
 - __name__ name of the accommodation
 - __address__ the general address provided publically, note that this might not be the exact address
 - __lat, lng__ the latitude and longitude, note that this might not be the exact address
 - __rating__ note that rating only applies to hotels, not apartment. `-1` indicates not applicable
 - __number_reviewed__ note that reviews only applies to hotels, not apartment. `-1` indicates not applicable
 - __last_reviewed__ when was the last review posted, because Booking.com 's mechanism, this might not be the exact "last review". Also, note that reviews only applies to hotels, not apartment.  empty indicates not applicable
 
 __Listings Avalibility (Delivered as json for each query date interval)__
 - __url__ the url is the ID of each accommodation
 - __rooms__ A list of rooms avaliable for booking, each element will be an object having 
     - _room\_type_ 
     - _price_ in USD
     - _left_ how many rooms are left for booking on Booking.com. Note that hotels showing 9 or 10 meaning they are more than 9 or 10 rooms left. 
