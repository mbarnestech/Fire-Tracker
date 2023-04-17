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

def get_fires():
    
    soup = get_soup_from_file()

    fires = []
    items = soup.find_all('item')

    for item in items:

        # get last update; if none
        last_update = re.search(r'\d{4}-\d{2}-\d{2}', item.find('description').string)
        if last_update:
            last_update = last_update.group(0)
        else:
            last_update = 'unknown'
        
        # get lat/long
        latlong_groups = re.findall(r"(?P<neg>-)?(?P<degrees>\d{2,3} ?)\°(?P<minutes>\d{1,2} ?)\'(?P<seconds>\d*\.?\d*)", item.find('description').string )
        if len(latlong_groups) > 1:
            latitude = helper.create_decimal_latlong(latlong_groups[0])
            longitude = helper.create_decimal_latlong(latlong_groups[1])
        else:
            latlong_groups = re.findall(r"(?P<neg>-)?(?P<latlong>[\d*\.]*)(?P<trailing>°)", item.find('description').string )
            if len(latlong_groups) > 1:
                latitude = helper.get_latlong_float(latlong_groups[0])
                longitude = helper.get_latlong_float(latlong_groups[1])
            else:
                print(f"{item.find('title').string}: LATITUDE / LONGITUDE ERROR")
                continue

        # get incident type

        incident_type = re.search(r"(incident is )(.*)( and involves)", item.find('description').string)
        if incident_type:
            incident_type = incident_type.group(2)

        # append attribute dict to fires list
        fires.append({'fire_url':item.find('link').string, 
                    'fire_name':item.find('title').string.strip(),
                    'latitude': latitude,
                    'longitude': longitude, 
                    'incident_type': incident_type, 
                    'last_updated': last_update, 
                    'size': None, # size and contained require second scrape; will not be in MVP
                    'contained': None
                    })

    return fires


     








