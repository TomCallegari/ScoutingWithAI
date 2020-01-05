import pickle
from itertools import islice, chain, repeat
import re

import scrapy
from Prospects.items import MetaItem, RegularSeasonItem
from scrapy import Request
from scrapy.loader import ItemLoader

with open('listfile.data', 'rb') as filehandle:
    urls_list = pickle.load(filehandle)

# def chunk_pad(it, size, padval=None):
#     it = chain(iter(it), repeat(padval))
#     return iter(lambda: tuple(islice(it, size)), (padval,) * size)

# player_url_list = list(chunk_pad(urls_list, 120))
# cohort = player_url_list[0]
# urls = [str(i) for i in cohort]

# player_ids = []
# for player in urls:
#     ep_id_regex = re.search(r'(\d+)', player)
#     player_ids.append(ep_id_regex.group(0))

# popup = 'https://www.eliteprospects.com/player_print_view.php?player='

# popup_urls = []
# for i in range(len(player_ids)):
#     popup_urls.append(popup + player_ids[i])

class PlayerSpider(scrapy.Spider):
    name = 'Prospects'
    
    def start_requests(self):
        for i in urls_list:
            yield scrapy.Request(i, self.parse)

    def parse(self, response):

        metaItem = MetaItem()
        RegItem = RegularSeasonItem()

        full_name = response.xpath("//h1[@class='plytitle']/text()").re('\w+\s\w+')

        meta_table = response.xpath("//div[@class='table-view']")
        for item in meta_table.xpath("//div[@class='table-view']"):
            
            yield 
        
        