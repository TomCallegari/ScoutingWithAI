from requests import get
from bs4 import BeautifulSoup
from time import sleep
from time import time
import pickle

response = get('https://www.eliteprospects.com/player/9223/john-tavares')
soup = BeautifulSoup(response.text, 'html.parser')

meta_section = soup.find('section', class_='plyr_details')
scout_text = meta_section.find('div', class_='dtl-txt').text.strip()

meta_items_list = []

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

# Draft Info
draft_table = soup.find('ul', class_='list-unstyled')
draft_info = draft_table.find('div', class_='col-xs-9 fac-lbl-dark')

print(meta_items_list)