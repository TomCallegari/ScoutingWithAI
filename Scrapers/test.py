
from requests import get
from bs4 import BeautifulSoup
import re
import pickle

urls = ['https://www.eliteprospects.com/player/9609/jakub-klepis', 'https://www.eliteprospects.com/player/213489/ryan-kehrig', 'https://www.eliteprospects.com/player/9223/john-tavares']

headers = {
    "user-Agent": "Personal web-scraping script.  I can be contacted at thomascallegari@yahoo.com"
}

for url in urls:

    response = get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Pull Eliteprospects ID from urls
    ep_id_regex = re.search(r'(\d+)', url)
    ep_id = ep_id_regex.group(0)

    awards_table = soup.select('div[id="awards"] div[class="season-body clearfix"] ul[class="list-unstyled list-li clearfix"] > li')

    season_list = []
    award_list = []

    for li in awards_table:

        div = li.select_one('div')
        season = div.text.strip()    

        awards_list = li.find_all('a')    
        for a in awards_list:
            award_list.append(a.text.strip())
            season_list.append(season)

            awards_dict = {
                'ep_id': ep_id,
                'season': season,
                'award': a.text.strip(),
                'award_count': 1
            }

            print(awards_dict)


######################

# Career statistics table
table_rows = soup.find('table', {'class': 'table table-striped table-condensed table-sortable player-stats highlight-stats'}).find('tbody').find_all('tr')

current_year = ''
for row in table_rows:
    cells = row.find_all('td')

    by_year = []
    for td in cells:
        by_year.append(td.text.strip())

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

    # print('season_dict: ', season_dict)


# for row in table.find_all('tr')[1:]:
#     cells = row.find_all('td')
#     print(cells[0], ' : ', cells[1])




# for tr in table_rows:
                    
#     # Player stats dictionary
#     player_stats_dict = {
#         'ep_id': ep_id,
#         'season': tr.find('td', {'class': 'season sorted'}).text.strip(),
#         'team': tr.find('td', {'class': 'team'}).text.strip(),
#         'league': tr.find('td', {'class': 'league'}).text.strip(),
#         'games_played': tr.find('td', {'class': 'regular gp'}).text.strip(),
#         'goals': tr.find('td', {'class': 'regular g'}).text.strip(),
#         'assists': tr.find('td', {'class': 'regular a'}).text.strip(),
#         'penalty_min': tr.find('td', {'class': 'regular pim'}).text.strip(),
#         'plus_minus': tr.find('td', {'class': 'regular pm'}).text.strip()
#     }

# print('player_stats_dict: ', player_stats_dict)


# print(urls)

# leagues = ['whl', 'ohl', 'qmjhl']
# leagues_url = [str(i) for i in leagues]

# seasons = ['2001-2002', '2002-2003', '2004-2005',
#             '2005-2006', '2006-2007', '2007-2008', '2008-2009', '2009-2010',
#            '2010-2011', '2011-2012', '2012-2013', '2013-2014', '2014-2015',
#            '2016-2017', '2017-2018', '2018-19']
# seasons_url = [str(i) for i in seasons]

# pages = [str(i) for i in range(1, 5)]

# url_list = []
# for league in leagues_url:
#     for season in seasons_url:
#         for page in pages:
#             url_list.append('http://www.eliteprospects.com/league/' + league + '/stats/' + season + '?sort=tp&page='+ page)

# print(len(url_list))

# with open('listfile.data', 'rb') as filehandle:
#     urls = pickle.load(filehandle)

# print(len(urls))

# leagues = ['whl', 'ohl', 'qmjhl']
# leagues_url = [str(i) for i in leagues]

# seasons = ['2001-2002', '2002-2003', '2004-2005', '2005-2006', '2006-2007', 
#             '2007-2008', '2008-2009', '2009-2010', '2010-2011', '2011-2012', 
#             '2012-2013', '2013-2014', '2014-2015', '2016-2017', '2017-2018', 
#             '2018-19']
# seasons_url = [str(i) for i in seasons]

# pages = [str(i) for i in range(1, 10)]

# print(leagues, leagues_url)
# print(seasons, seasons_url)
# print(pages)
    
# url = 'http://www.eliteprospects.com/player/9223/john-tavares'

# meta_items_list = []

# response = get(url)
# soup = BeautifulSoup(response.text, 'html.parser')

# # ep_id
# ep_id_regex = re.search(r'(\d+)', url)
# ep_id = ep_id_regex.group(0)

# # Meta items
# meta_table = soup.find('div', class_='table-view')
# for item in meta_table.find_all('div', class_='col-xs-8 fac-lbl-dark'):
#     items = item.text.strip()
#     meta_items_list.append(items)

# for i in range(1-1, 10):
#     print(meta_items_list[i])

# stat_table = soup.find('div', {'id': 'league-stats'})
# club_table_rows = stat_table.find_all('tr', {'class': 'team-continent-NA'})
# for tr in club_table_rows:
                        
#     # Player stats dictionary
#     player_stats_dict = {
#         'ep_id': ep_id,
#         'season': tr.find('td', {'class': 'season sorted'}).text.strip(),
#         'team': tr.find('td', {'class': 'team'}).text.strip(),
#         'league': tr.find('td', {'class': 'league'}).text.strip(),
#         'games_played': tr.find('td', {'class': 'regular gp'}).text.strip(),
#         'goals': tr.find('td', {'class': 'regular g'}).text.strip(),
#         'assists': tr.find('td', {'class': 'regular a'}).text.strip(),
#         'penalty_min': tr.find('td', {'class': 'regular pim'}).text.strip(),
#         'plus_minus': tr.find('td', {'class': 'regular pm'}).text.strip()
#     }

#     for i in player_stats_dict.items():
#         print('Regular: ', i)

#     playoff_stats_dict = {
#         'ep_id': ep_id,
#         'playoffs_gp': tr.find('td', {'class': 'playoffs gp'}).text.strip(),
#         'playoffs_g': tr.find('td', {'class': 'playoffs g'}).text.strip(),
#         'playoffs_a': tr.find('td', {'class': 'playoffs a'}).text.strip(),
#         'playoffs_pim': tr.find('td', {'class': 'playoffs pim'}).text.strip(),
#         'playoffs_pm': tr.find('td', {'class': 'playoffs pm'}).text.strip()
#     }
    
#     for i in player_stats_dict.items():
#         print('Playoffs: ', i)

# int_table_rows = stat_table.find_all('tr', {'class': 'team-continent-INT'})
# for tr in int_table_rows:

#     # International stats playoffs
#     int_stats_dict = {
#         'ep_id': ep_id,
#         'team': tr.find('td', {'class': 'team'}).text.strip(),
#         'league': tr.find('td', {'class': 'league'}).text.strip(),
#         'int_gp': tr.find('td', {'class': 'regular gp'}).text.strip(),
#         'int_g': tr.find('td', {'class': 'regular g'}).text.strip(),
#         'int_a': tr.find('td', {'class': 'regular a'}).text.strip(),
#         'int_pim': tr.find('td', {'class': 'regular pim'}).text.strip(),
#         'int_pm': tr.find('td', {'class': 'regular pm'}).text.strip()
#     }

#     for i in int_stats_dict.items():
#         print('International: ', i)    