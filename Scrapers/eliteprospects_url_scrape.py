
from requests import get
from bs4 import BeautifulSoup
from time import sleep
from time import time
import pickle

leagues = ['whl', 'ohl', 'qmjhl']

seasons = ['2001-2002', '2002-2003', '2004-2005', '2005-2006', '2006-2007', 
            '2007-2008', '2008-2009', '2009-2010', '2010-2011', '2011-2012', 
            '2012-2013', '2013-2014', '2014-2015', '2016-2017', '2017-2018', 
            '2018-19']

pages = [str(i) for i in range(1, 5)]

href_ids = []
rows_added = 0

headers = {
    "user-Agent": "Personal web scraping script.  I can be contacted at thomascallegari@yahoo.com"
}

for league in leagues:
    for season in seasons:
        for page in pages:

            # Assemble url, get response, parse beautiful soup object
            year_url = 'http://www.eliteprospects.com/league/' + league + '/stats/' + season + '?sort=tp&page=' + page

            # Get response object from url and parse html with BeautifulSoup
            response = get(year_url, headers = headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Isolate the table and rows
            try:
                table = soup.find('table', class_='table table-striped table-sortable player-stats highlight-stats season')
                player_table_rows = table.find_all('td', attrs={'class': 'player', 'style': 'white-space: nowrap;'})

                for td in player_table_rows:
                    href = td.find('a')['href']
                    href_ids.append(href)

                    rows_added += 1
                    print(rows_added, href)
            except:
                continue

href_ids = list(set(href_ids))
print('Number of player profiles: ' , len(href_ids))

with open('listfile.data', 'wb') as filehandle:
    pickle.dump(href_ids, filehandle)
