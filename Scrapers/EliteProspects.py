
# Import required packages/modules
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
from time import time
from time import sleep
import pandas as pd
import numpy as np
import re
import pickle
from itertools import islice, chain, repeat
import pymongo

# Create connection to MongoDB
conn = 'mongodb://localhost:27018'
client = pymongo.MongoClient(conn)

# Create Eliteprospects DB
db = client.eliteprospects
meta_collection = db.meta_data
player_collection = db.player_data

# Setup iteratble list for player profile href links
with open('listfile.data', 'rb') as filehandle:
    urls = pickle.load(filehandle)

# def chunk_pad(it, size, padval=None):
#     it = chain(iter(it), repeat(padval))
#     return iter(lambda: tuple(islice(it, size)), (padval,) * size)

# player_url_list = list(chunk_pad(urls, 120))

# cohort = player_url_list[0]

players_urls = [str(i) for i in urls] # change urls / cohort if using chunked list

# Create empty list for meta table variables
meta_items_list = []

# User-agent header for www.eliteprospects.com/robots.txt web logs
headers = {
    "user-Agent": "Personal web-scraping script.  I can be contacted at thomascallegari@yahoo.com"
}

# Create a variable for output printing
players_added = 0

# Initialize empty DataFrames
meta_stats = pd.DataFrame()
player_stats = pd.DataFrame()

# for loop for each player profile
for player in players_urls:

    # Pull html soup from profile
    response = get(player, headers=headers) # Add headers=headers to add user-agent header for each request
    soup = BeautifulSoup(response.text, 'html.parser')

    # Pull Eliteprospects ID from urls
    ep_id_regex = re.search(r'(\d+)', player)
    ep_id = ep_id_regex.group(0)

    # Meta data section
    meta_section = soup.find('section', class_='plyr_details')

    # Player name
    full_name = meta_section.find('h1', class_='plytitle').text.strip()
    
    # Meta data
    meta_table = soup.find('div', class_='table-view')    
    for item in meta_table.find_all('div', class_='col-xs-8 fac-lbl-dark'):
            items = item.text.strip()
            meta_items_list.append(items)

    # Scouting text
    try:
        scout_text = meta_section.find('div', class_='dtl-txt').text.strip()
    except:
        scout_text = '-'

    # Meta data dictionary
    meta_data_dict = {
        'ep_id': ep_id,
        'full_name': full_name,
        'date_of_birth': meta_items_list[0],
        'hometown': meta_items_list[2],
        'country': meta_items_list[3],
        'youth_team': meta_items_list[4],
        'position': meta_items_list[5],
        'height': meta_items_list[6],
        'weight': meta_items_list[7],
        'shoots': meta_items_list[8],
        'status': meta_items_list[9],
        'scout_text': scout_text
    }

    # Print output for each player meta data
    for i in meta_data_dict.items():
        print(i)

    meta_collection.insert_one(meta_data_dict)

    # Re-initialise the meta_data_dict to be empty for the next interation
    meta_data_dict = {} 

    # Reset meta_items_list for next iteration
    meta_items_list = []

    # Career statistics table
    stat_table = soup.find('div', {'id': 'league-stats'})
    table_rows = stat_table.find_all('tr', {'class': 'team-continent-NA'})
    for tr in table_rows:
                        
        # Player stats dictionary
        player_stats_dict = {
            'ep_id': ep_id,
            'season': tr.find('td', {'class': 'season sorted'}).text.strip(),
            'team': tr.find('td', {'class': 'team'}).text.strip(),
            'league': tr.find('td', {'class': 'league'}).text.strip(),
            'games_played': tr.find('td', {'class': 'regular gp'}).text.strip(),
            'goals': tr.find('td', {'class': 'regular g'}).text.strip(),
            'assists': tr.find('td', {'class': 'regular a'}).text.strip(),
            'penalty_min': tr.find('td', {'class': 'regular pim'}).text.strip(),
            'plus_minus': tr.find('td', {'class': 'regular pm'}).text.strip()
        }

        # Insert player_stats table into database
        player_collection.insert_one(player_stats_dict)

        # Re-initialise the player_stats_dict to be empty for the next interation
        player_stats_dict = {}
    
    # Print current number of players added
    players_added += 1
    print('')
    print('Players added: ', players_added)
    print('# --------------------------------------------------------------------------- #')
    print('')
