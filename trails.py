"""scraper file for getting basic trail information from hikingproject.com"""

# import Python modules
from bs4 import BeautifulSoup
import requests

# import local modules
from seed import seed_trail


# currently designing this to be run interactively
def get_soup(website):
    """get html from website parsed by BeautifulSoup"""
    response = requests.get(website)
    return BeautifulSoup(response.text, 'html.parser')

# option to get website from command line input - will need python3 trails.py <url for website>
# import sys
# url = sys.argv[1]
# soup = get_soup(url)

def get_trails(soup):
    """create trail list for seeding"""

    # create empty trails list
    trails = []
    
    # currently planning on running this by subarea to state, area same for all trails
    area = soup.h1.get_text()
    table_data = soup.find_all(class_='trail-row')
    # list I need:
    {'trail_name': 'Cochise Stronghold Trail #279', 
        'hp_id': '7030929', 
        'state': 'AZ',
        'area': 'Southern Arizona and Tucson',
        'city': 'Saint David'},
