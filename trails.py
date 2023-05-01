"""scraper file for getting basic trail information from hikingproject.com"""

# import Python modules
from bs4 import BeautifulSoup
import re
import requests
import sys


#  temp for test file
# with open('./testcode/testscrape.html') as file:
#    soup = BeautifulSoup(file, 'html.parser')

# currently designing this to be run interactively
def get_soup(website):
    """get html from website parsed by BeautifulSoup"""
    response = requests.get(website)
    return BeautifulSoup(response.text, 'html.parser')

# option to get website from command line input - will need python3 trails.py <url for website>
# if sys.argv[1]:
#     url = sys.argv[1]
#     soup = get_soup(url)

def get_trails(soup):
    """create trail list for seeding"""

    # create empty trails list
    trails = []
    
    # currently planning on running this by subarea to state, area same for all trails
    area = soup.h1.get_text()
    data_by_row = soup.select('.trail-row')
    for row in data_by_row:
        trail_name = row.strong.get_text() # gets string of trail name
        hp_id = re.search(r'\d{7}', str(row.a)).group(0) # gets string of hiking project id number
        city, state = row.find_all('td')[-3].get_text()[1:-1].split(', ') # gets string in 'City, State' format
        trails.append({
            'trail_name': trail_name, 
            'hp_id': hp_id, 
            'state': state,
            'area': area,
            'city': city
        })
    return trails

# trails = get_trails(soup)

