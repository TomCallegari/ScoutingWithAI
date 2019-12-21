import pickle
from itertools import islice, chain, repeat
import re

import scrapy
from Prospects.items import MetaItems, RegularItems, PostItems, InterItems, TourItems
from scrapy.loader import ItemLoader

with open('listfile.data', 'rb') as filehandle:
    urls_list = pickle.load(filehandle)

def chunk_pad(it, size, padval=None):
    it = chain(iter(it), repeat(padval))
    return iter(lambda: tuple(islice(it, size)), (padval,) * size)

player_url_list = list(chunk_pad(urls_list, 120))
cohort = player_url_list[0]
urls = [str(i) for i in cohort]

player_ids = []
for player in urls:
    ep_id_regex = re.search(r'(\d+)', player)
    player_ids.append(ep_id_regex.group(0))

popup = 'https://www.eliteprospects.com/player_print_view.php?player='

popup_urls = []
for i in range(len(player_ids)):
    popup_urls.append(popup + player_ids[i])

class PlayerSpider(scrapy.Spider):
    name = 'Prospects'

    start_urls = popup_urls

    def _parse_metaItem(self, response):

        lmeta = ItemLoader(item=MetaItems(), response=response)

        lmeta.add_xpath('full_name', '//*[@id="fontHeader"]')
        lmeta.add_xpath('date_of_birth', '//*[@id="ads-fullpage-site"]/p/table[2]/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/a')

        return lmeta.load_item()

