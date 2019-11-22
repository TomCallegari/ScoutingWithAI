
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
conn = 'mongodb://localhost:27017'
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

players_url = [str(i) for i in urls] # change urls / cohort if using chunked list

# Create empty list for meta table variables
meta_items_list = []

# User-agent header for www.eliteprospects.com/robots.txt web logs
headers = {
    "user-Agent": "Student project for Uoft - School of Continuing Studies - Data Analytics.  I can be contacted at thomascallegari@yahoo.com"
}

# Create a variable for output printing
players_added = 0

# Initialize empty DataFrames
meta_stats = pd.DataFrame()
player_stats = pd.DataFrame()

# for loop for each player profile
for player in players_url:

    # Pull html soup from profile
    response = get(player) # Add headers=headers to add user-agent header for each request
    soup = BeautifulSoup(response.text, 'html.parser')

    # Pull Eliteprospects ID from urls
    ep_id_regex = re.search(r'(\d+)', player)
    ep_id = ep_id_regex.group(0)

    # Meta data section
    meta_section = soup.find('section', class_='plyr_details')

    # Player name
    raw_full_name = meta_section.find('h1', class_='plytitle').text.strip()
    
    # Meta data
    meta_table = soup.find('div', class_='table-view')
    for item in meta_table.find_all('div', class_='col-xs-8 fac-lbl-dark'):
        items = item.text.strip()
        meta_items_list.append(items)
    
    # Append empty meta variable lists
    raw_birth_date = meta_items_list[0]
    raw_hometown = meta_items_list[2]
    raw_country = meta_items_list[3]
    youth_team = meta_items_list[4]
    position = meta_items_list[5]
    raw_height = meta_items_list[6]
    raw_weight = meta_items_list[7]
    shoots = meta_items_list[8]

    # Scouting text
    try:        
        scout_text = meta_section.find('div', class_='dtl-txt').text.strip()        
    except:        
        scout_text = np.nan

    # Modify date_of_birth format to fit MySQL 8.0.16 accepted date type
    date_of_birth = raw_birth_date

    # Extract full_name with no tailing whitespace
    full_name_regex = re.search(r'(\w+\s\w+)', raw_full_name)
    if re.search(r'(\w+\s\w+)', raw_full_name) is None:
        full_name = np.nan
    else:
        full_name = full_name_regex.group(0)

    # Extract hometown city name
    hometown_regex = re.search(r'(\w{4,})', raw_hometown)
    if re.search(r'(\w{4,})', raw_hometown) is None:
        hometown = np.nan
    else:
        hometown = hometown_regex.group(0)
    
    # Extract country with no tailing whitespace
    country_regex = re.search(r'(\w+)', raw_country)
    if re.search(r'(\w+)', raw_country) is None:
        country = np.nan
    else:
        country = country_regex.group(0)
    
    # Extract height in cm
    height_regex = re.search(r'(\d{3})', raw_height)
    if re.search(r'(\d{3})', raw_height) is None:
        height = np.nan
    else:
        height = height_regex.group(0)

    # Extract weight in kg
    weight_regex = re.search(r'(\d{2})\skg', raw_weight)
    if re.search(r'(\d{2})\skg', raw_weight) is None:
        weight = np.nan
    else:
        weight_kg = weight_regex.group(0)
        weight_kg_regex = re.search(r'(\d{2})', weight_kg)
        weight = weight_kg_regex.group(0)

    # Meta data dictionary
    meta_data_dict = {
        'ep_id': ep_id,
        'full_name': full_name,
        'date_of_birth': date_of_birth,
        'hometown': hometown,
        'country': country,
        'youth_team': youth_team,
        'position': position,
        'height': height,
        'weight': weight,
        'shoots': shoots,
        'scout_text': scout_text
    }

    meta_collection.insert_one(meta_data_dict)

    # Re-initialise the meta_data_dict to be empty for the next interation
    meta_data_dict = {} 

    # Reset meta_items_list for next iteration
    meta_items_list = []

    # Career statistics table
    stat_table = soup.find('table', class_='table table-striped table-condensed table-sortable player-stats highlight-stats')
    table_rows = stat_table.find_all('tr', {'class': 'team-continent-NA'})

    # Collect career statistics by variable
    for tr in table_rows:
        # Season
        if tr.find('td', {'class': 'season sorted'}).text.strip():
            tr_season = tr.find('td', {'class': 'season sorted'}).text.strip()
            season = tr_season
        elif len(tr.find('td', {'class': 'season sorted'}).text.strip()) == 0:
            season = tr_season       
        # Team
        team = tr.find('td', {'class': 'team'}).text.strip()
        # League
        league = tr.find('td', {'class': 'league'}).text.strip()
        # Games played
        if tr.find('td', {'class': 'regular gp'}).text.strip() == '-':
            games_played = 0
        else:
            games_played = tr.find('td', {'class': 'regular gp'}).text.strip() # original line
        # Goals
        if tr.find('td', {'class': 'regular g'}).text.strip() == '-':
            goals = 0
        else:
            goals = tr.find('td', {'class': 'regular g'}).text.strip() # original line
        # Assists
        if tr.find('td', {'class', 'regular pim'}).text.strip() == '-':
            assists = 0
        else:
            assists = tr.find('td', {'class': 'regular a'}).text.strip() # original line
        # Penalty minutes
        if tr.find('td', {'class': 'regular pim'}).text.strip() == '-':
            penalty_min = 0
        else:
            penalty_min = tr.find('td', {'class': 'regular pim'}).text.strip() # original line
        # Plus/minus
        if len(tr.find('td', {'class': 'regular pm'})) > 0:
            plus_minus = tr.find('td', {'class': 'regular pm'}).text.strip()
        elif len(tr.find('td', {'class': 'regular pm'})) == 0:
            plus_minus = 0
        
        # Player stats dictionary
        player_stats_dict = {
            'ep_id': ep_id,
            'season': season,
            'team': team,
            'league': league,
            'games_played': games_played,
            'goals': goals,
            'assists': assists,
            'penalty_min': penalty_min,
            'plus_minus': plus_minus
        }

        player_collection.insert_one(player_stats_dict)

        # Re-initialise the player_stats_dict to be empty for the next interation
        player_stats_dict = {}
    
    # Print current number of players added
    players_added += 1
    print('Players added: ', players_added)

