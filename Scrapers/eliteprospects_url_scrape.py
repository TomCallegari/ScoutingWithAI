
from requests import get
from bs4 import BeautifulSoup
from time import sleep
from time import time
import pickle

leagues = ['whl', 'ohl', 'qmjhl']
leagues_url = [str(i) for i in leagues]

seasons = ['2005-2006', '2006-2007', '2007-2008', '2008-2009', '2009-2010',
           '2010-2011', '2011-2012', '2012-2013', '2013-2014', '2014-2015',
           '2016-2017', '2017-2018', '2018-19']
seasons_url = [str(i) for i in seasons]

pages = [str(i) for i in range(1, 5)]

href_id = []

start_time = time()
requests = 0
rows_added = 0

headers = {
    "user-Agent": "Personal web scraping script.  I can be contacted at thomascallegari@yahoo.com"
}

for league in leagues_url:
    for season in seasons_url:
        for page in pages:
            response = get('http://www.eliteprospects.com/league/'
                           + league
                           + '/stats/'
                           + season
                           + '?sort=tp&page='
                           + page,
                           headers=headers)
            sleep(30)
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('div', {'id': 'skater-stats'})
            player_table_rows = table.find_all('td', attrs={'class': 'player', 'style': 'white-space: nowrap;'})
            for td in player_table_rows:
                href = td.find('a')['href']
                href_id.append(href)
                rows_added += 1
                print(rows_added, href)

href_ids = list(set(href_id))

with open('listfile.data', 'wb') as filehandle:
    pickle.dump(href_ids, filehandle)

    