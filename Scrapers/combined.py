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
award_collection = db.awards_data

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
players_added = 0
href_ids = []

# Loop through each combination league, year and pagination #
for league in leagues:
    for season in seasons:
        for page in pages:

            # Assemble url, get response, parse beautiful soup object
            year_url = 'http://www.eliteprospects.com/league/' + league + '/stats/' + season + '?sort=tp&page=' + page
            
            # Initialize href_ids list for each page of player profile links
            current_href_ids = []

            # Get response object from url and parse html with BeautifulSoup
            links_response = get(year_url, headers = headers)
            links_soup = BeautifulSoup(links_response.text, 'html.parser')
            sleep(30)
            
            # Isolate the table and rows, if the table doesn't exist then get the response for the next iterable pagination list
            try:
                table = links_soup.find('table', class_='table table-striped table-sortable player-stats highlight-stats season')
                player_table_rows = table.find_all('td', attrs={'class': 'player', 'style': 'white-space: nowrap;'})

                # Loop down trough each player, get their profile page then parse and insert into MongoDB
                for td in player_table_rows:
                    href = td.find('a')['href']

                    if href not in href_ids:
                        href_ids.append(href)
                        current_href_ids.append(href)
                
                for href in current_href_ids:

                    # Pull html soup from profile
                    response = get(href, headers = headers) # Add headers=headers to add user-agent header for each request
                    
                    print('')
                    print('# --------------------------------------------------------- #')
                    print('')
                    print('Current page: ', year_url)
                    print('response type: ', type(response))
                    print(response)
                    
                    soup = BeautifulSoup(response.text, 'html.parser')
                    sleep(30)

                    # Create empty list for meta table variables
                    meta_items_list = []

                    # Pull Eliteprospects ID from urls
                    ep_id_regex = re.search(r'(\d+)', href)
                    ep_id = ep_id_regex.group(0)
                    
                    # Meta data section
                    meta_section = soup.find('section', class_='plyr_details')

                    # Player name
                    full_name = meta_section.find('h1', class_='plytitle').text.strip()

                    print('ep_id: ', ep_id, 'full_name: ', full_name, 'href: ', href)
                                        
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
                    table_rows = soup.find('table', {'class': 'table table-striped table-condensed table-sortable player-stats highlight-stats'}).find('tbody').find_all('tr')

                    # Set an empty string for the current row year (season i.e - '2005-06')
                    current_year = ''

                    # Iterate through each row of the table and set aside an iterable containing each variable
                    for row in table_rows:
                        cells = row.find_all('td')
                        
                        # Build a list of each row variable for selection by indexing
                        by_year = []
                        for td in cells:
                            by_year.append(td.text.strip())

                        # Manage empty year variables by using the empty current_year string
                        if by_year[0] != '':
                            current_year = by_year[0]
                            by_year[8] = 'club'
                        elif by_year[0] == '':
                            by_year[0] = current_year
                            by_year[8] = 'international'

                        season_dict = {
                            'ep_id': ep_id,
                            'season': by_year[0],
                            'team': by_year[1],
                            'league': by_year[2],
                            'regular_gp': by_year[3],
                            'regular_g': by_year[4],
                            'regular_a': by_year[5],
                            'regular_pim': by_year[6],
                            'regular_pm': by_year[7],
                            'team_type': by_year[8],
                            'playoffs_gp': by_year[10],
                            'playoffs_g': by_year[11],
                            'playoffs_a': by_year[12],
                            'playoffs_pim': by_year[14],
                            'playoffs_pm': by_year[15]
                        }

                        player_collection.insert_one(season_dict)

                        # Awards Table
                        awards_table = soup.select('div[id="awards"] div[class="season-body clearfix"] ul[class="list-unstyled list-li clearfix"] > li')

                        for li in awards_table:

                            div = li.select_one('div')
                            season = div.text.strip()    

                            awards_list = li.find_all('a')    
                            for a in awards_list:
                                
                                awards_dict = {
                                    'ep_id': ep_id,
                                    'season': season,
                                    'award': a.text.strip(),
                                    'award_count': 1
                                }

                                award_collection.insert_one(awards_dict)

                    players_added += 1
                    print('')
                    print('# ------------')
                    print('players_added: ', players_added) 
                    
            except: 
                continue 