from requests import get
from bs4 import BeautifulSoup
from time import sleep
from time import time
import pickle
import re
import pickle
from itertools import islice, chain, repeat
import pymongo

# Create connection to MongoDB
conn = 'mongodb://localhost:27018'
client = pymongo.MongoClient(conn)

# Create Eliteprospects DB
db = client.eliteprospects

# Create collections
meta_collection = db.meta_data
player_collection = db.player_data
playoffs_collection = db.playoffs_data
international_collection = db.international_data

# Create empty list for meta table variables
meta_items_list = []

# User-agent header for www.eliteprospects.com/robots.txt web logs
headers = {
    "user-Agent": "Personal web-scraping script.  I can be contacted at thomascallegari@yahoo.com"
}

# Set list iterables for url components
leagues = ['whl', 'ohl', 'qmjhl']

seasons = ['2001-2002', '2002-2003', '2004-2005', '2005-2006', '2006-2007', 
            '2007-2008', '2008-2009', '2009-2010', '2010-2011', '2011-2012', 
            '2012-2013', '2013-2014', '2014-2015', '2016-2017', '2017-2018', 
            '2018-19']

pages = [str(i) for i in range(1, 10)]

# Set empty list and variable to track hrefs and number of rows added
href_ids = []
rows_added = 0

# Loop through each combination league, year and pagination #
for league in leagues:
    for season in seasons:
        for page in pages:

            # Assemble url, get response, parse beautiful soup object
            year_url = 'http://www.eliteprospects.com/league/' + league + '/stats/' + season + '?sort=tp&page=' + page
            print('Current page: ', year_url)

            # Get response object from url and parse html with BeautifulSoup
            response = get(year_url, headers = headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            sleep(30)
            
            # Isolate the table and rows, if the table doesn't exist then get the response for the next iterable pagination list
            try:
                table = soup.find('table', class_='table table-striped table-sortable player-stats highlight-stats season')
                player_table_rows = table.find_all('td', attrs={'class': 'player', 'style': 'white-space: nowrap;'})

                # Loop down trough each player, get their profile page then parse and insert into MongoDB
                for td in player_table_rows:
                    href = td.find('a')['href']
                    print('Current href: ', href)

                    if href not in href_ids:
                        href_ids.append(href)                    

                        # Pull html soup from profile
                        response = get(href, headers = headers) # Add headers=headers to add user-agent header for each request
                        soup = BeautifulSoup(response.text, 'html.parser')
                        sleep(30)

                        # Pull Eliteprospects ID from urls
                        ep_id_regex = re.search(r'(\d+)', player)
                        ep_id = ep_id_regex.group(0)
                        print(ep_id)

                        # Meta data section
                        meta_section = soup.find('section', class_='plyr_details')

                        # Player name
                        full_name = meta_section.find('h1', class_='plytitle').text.strip()

                        print(ep_id, full_name, player)
                        
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

                        # Insert meta data dict into MongoDB meta_data collection
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

                            # Build playoff stats dictionary
                            playoff_stats_dict = {
                                'ep_id': ep_id,
                                'playoffs_gp': tr.find('td', {'class': 'playoffs gp'}).text.strip(),
                                'playoffs_g': tr.find('td', {'class': 'playoffs g'}).text.strip(),
                                'playoffs_a': tr.find('td', {'class': 'playoffs a'}).text.strip(),
                                'playoffs_pim': tr.find('td', {'class': 'playoffs pim'}).text.strip(),
                                'playoffs_pm': tr.find('td', {'class': 'playoffs pm'}).text.strip()
                            }

                            # Insert playoff_stats table into database
                            playoffs_collection.insert_one(playoff_stats_dict)

                            # Re-initialise the playoffs_stats_dict to be empty for the next iteration
                            playoff_stats_dict = {}

                        # International statistics table
                        int_table_rows = stat_table.find_all('tr', {'class': 'team-continent-INT'})
                        for tr in int_table_rows:

                            # International stats playoffs
                            int_stats_dict = {
                                'ep_id': ep_id,
                                'team': tr.find('td', {'class': 'team'}).text.strip(),
                                'league': tr.find('td', {'class': 'league'}).text.strip(),
                                'int_gp': tr.find('td', {'class': 'regular gp'}).text.strip(),
                                'int_g': tr.find('td', {'class': 'regular g'}).text.strip(),
                                'int_a': tr.find('td', {'class': 'regular a'}).text.strip(),
                                'int_pim': tr.find('td', {'class': 'regular pim'}).text.strip(),
                                'int_pm': tr.find('td', {'class': 'regular pm'}).text.strip()
                            }

                            # Insert int_stats table into database
                            international_collection.insert_one(int_stats_dict)

                            # Re-initialise the int_stats_dict to be empty for the next iteration
                            int_stats_dict = {}

                    else:
                        continue

                    rows_added += 1
                    print(rows_added, href)    

            except: 
                continue 