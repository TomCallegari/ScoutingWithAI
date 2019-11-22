
# Import required packages/modules
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
from time import time
from time import sleep
import pandas as pd
import re
import mysql.connector
import pickle
from mysql.connector import Error

# Initialize PlayerObject
class PlayerObject():
    """
    Write something here ...
    """

    def __init__(self, host, database, user):
        self.password = 'TCisc00l#'
        self.host = host
        self.database = database
        self.user = user

    def MySQLConnect(self, add_meta_stats, add_player_stats):
        
        try:
            cnx = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )

            if cnx.is_connected():
                print('Connected to localhost: {}'.format(self.database))

                cursor = cnx.cursor()
                
                # Setup iteratble list for player profile href links
                with open('listfile.data', 'rb') as filehandle:
                    urls = pickle.load(filehandle)
                
                players_url = [str(i) for i in urls]

                # Create empty list for meta table variables
                meta_items_list = []

                # User-agent header for www.eliteprospects.com/robots.txt web logs
                headers = {
                    "user-Agent": "Personal web-scraping script.  I can be contacted at thomascallegari@yahoo.com"
                    }
                
                # Create a variable for output printing
                players_added = 0

                # for loop for each player profile
                for player in players_url:
                    
                    # Pull html soup from profiles
                    response = get(player, headers=headers)
                    sleep(30)
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

                    # Modify date_of_birth format to fit MySQL 8.0.16 accepted date type
                    date_of_birth = datetime.strptime(raw_birth_date, '%b %d, %Y')

                    # Extract full_name with no tailing whitespace
                    full_name_regex = re.search(r'(\w+\s\w+)', raw_full_name)
                    if re.search(r'(\w+\s\w+)', raw_full_name) is None:
                        full_name = 'Unknown'
                    else:
                        full_name = full_name_regex.group(0)

                    # Extract hometown city name
                    hometown_regex = re.search(r'(\w{4,})', raw_hometown)
                    if re.search(r'(\w{4,})', raw_hometown) is None:
                        hometown = 'Unknown'
                    else:
                        hometown = hometown_regex.group(0)
    
                    # Extract country with no tailing whitespace
                    country_regex = re.search(r'(\w+)', raw_country)
                    if re.search(r'(\w+)', raw_country) is None:
                        country = 'Unknown'
                    else:
                        country = country_regex.group(0)
    
                    # Extract height in cm
                    height_regex = re.search(r'(\d{3})', raw_height)
                    if re.search(r'(\d{3})', raw_height) is None:
                        height = 'NaN'
                    else:
                        height = height_regex.group(0)

                    # Extract weight in kg
                    weight_regex = re.search(r'(\d{2})\skg', raw_weight)
                    if re.search(r'(\d{2})\skg', raw_weight) is None:
                        weight = 'NaN'
                    else:
                        weight_kg = weight_regex.group(0)
                        weight_kg_regex = re.search(r'(\d{2})', weight_kg)
                        weight = weight_kg_regex.group(0)

                    # Scouting text
                    if soup.find('div', class_='dtl-txt').text.strip() is None:
                        ep_scout_report = 'Unknown'
                    else:
                        ep_scout_report = soup.find('div', class_='dtl-txt').text.strip()

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
                        'ep_scout_report': ep_scout_report
                    }

                    # Insert meta_data into database
                    cursor.execute(add_meta_stats, meta_data_dict)

                    # Commit Data
                    cnx.commit()

                    # Reset meta_items list for next iteration
                    meta_items_list = []

                    # Career statistics table
                    stat_table = soup.find('div', {'id': 'default-player-stats-league', 'class': 'league-tab'})
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
                        games_played = tr.find('td', {'class': 'regular gp'}).text.strip()

                        # Goals
                        goals = tr.find('td', {'class': 'regular g'}).text.strip()

                        # Assists
                        assists = tr.find('td', {'class': 'regular a'}).text.strip()

                        # Penalty minutes
                        penalty_min = tr.find('td', {'class': 'regular pim'}).text.strip()

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

                        # Insert player stats row into database
                        cursor.execute(add_player_stats, player_stats_dict)

                        # Commit data
                        cnx.commit()
                    
                    # Print current number of players added
                    players_added += 1
                    print('Players added: ', players_added)
        
        except Error as e:
            print(e)
        
        cursor.close()
        cnx.close()

if __name__=='__main__':

    # Access the database through the PlayerObject
    p = PlayerObject(host='localhost', database='chl_players', user='root')

    # Create insert data statements for database
    add_meta_stats = ("INSERT INTO meta_data "
                     "(ep_id, full_name, date_of_birth, hometown, country, "
                     "youth_team, position, height, weight, shoots) "
                     "VALUES (%(ep_id)s, %(full_name)s, %(date_of_birth)s, "
                     "%(hometown)s, %(country)s, %(youth_team)s, %(position)s, "
                     "%(height)s, %(weight)s, %(shoots)s, %(ep_scout_report)s)")

    add_player_stats = ("INSERT INTO yearly_player_stats "
                       "(ep_id, season, team, league, games_played, goals, assists, "
                       "penalty_min, plus_minus) "
                       "VALUES (%(ep_id)s, %(season)s, %(team)s, %(league)s, %(games_played)s, "
                       "%(goals)s, %(assists)s, %(penalty_min)s, %(plus_minus)s)")

    p.MySQLConnect(add_meta_stats)
    p.MySQLConnect(add_player_stats)
                