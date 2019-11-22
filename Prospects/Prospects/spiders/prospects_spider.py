
import scrapy
import pickle
from itertools import islice, chain, repeat
import re
from Prospects.items import MetaDataItem, PlayerStatsItem

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

    def _parse_meta_data_item(self, response):

        ep_id = response.xpath('meta[@property="og:url"]')['content'].text()
        full_name = response.xpath('//span[@id="fontHeader"]/text()').get()
        date_of_birth = response.xpath('//*[@id="ads-fullpage-site"]/p/table[2]/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/a/text()').get()

        metadataitem = MetaDataItem()
        metadataitem['full_name'] = full_name,
        metadataitem['date_of_birth'] = date_of_birth,
        metadataitem['ep_id'] = ep_id

        yield metadataitem

