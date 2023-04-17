"""obtain data from Inciweb for creating Fire instances"""

# using RSS feed to get xml data at https://inciweb.nwcg.gov/incidents/rss.xml

#import Python modules
import requests
from bs4 import BeautifulSoup
import re

#import local modules
import helper


def get_soup_from_inciweb(inciweb_url = 'https://inciweb.nwcg.gov/incidents/rss.xml'):
    """get xml from a website parsed by BeautifulSoup"""
    response = requests.get(inciweb_url)
    return BeautifulSoup(response.text, 'xml')

def get_soup_from_file(text = 'seed_data/incidents.xml'):
    """get xml from a file parsed by BeautifulSoup"""
    with open(text) as file:
        return BeautifulSoup(file, 'xml')

# def get_fires():
    
soup = get_soup_from_file()

fires = []
items = soup.find_all('item')

for item in items[:1]:

    # get last update; if none
    last_update = re.search(r'\d{4}-\d{2}-\d{2}', item.find('description').string)
    if last_update:
        last_update = last_update.group(0)
    else:
        last_update = 'unknown'
    
    # get lat/long
    latlong_groups = re.findall(r"(?P<neg>-)?(?P<degrees>\d*)\°(?P<minutes>\d{2})\'(?P<seconds>\d*\.?\d*)", "Latitude: 39°57'0''  Longitude: -105°22'5'' " )
    if latlong_groups[0] and latlong_groups[1]:
        latitude = helper.create_decimal_latlong(latlong_groups[0])
        longitude = helper.create_decimal_latlong(latlong_groups[1])
    else:
        print('no latlong group')
        continue

    # append attribute dict to fires list
    fires.append({'fire_url':item.find('link').string, 
                 'fire_name':item.find('title').string,
                 'latitude': latitude,
                 'longitude': longitude, 
                 'incident_type': '', 
                 'last_updated': last_update, 
                 'size': '', 
                 'contained': ''
                 })


print(fires[0])
# return fires[0]

     








