import scrapy
import pickle
from itertools import islice, chain, repeat

# Setup iteratble list for player profile href links
with open('listfile.data', 'rb') as filehandle:
    urls = pickle.load(filehandle)

def chunk_pad(it, size, padval=None):
    it = chain(iter(it), repeat(padval))
    return iter(lambda: tuple(islice(it, size)), (padval,) * size)

player_url_list = list(chunk_pad(urls, 120))
cohort = player_url_list[0]
urls = [str(i) for i in cohort]

class ProspectsSpider(scrapy.Spider):
    name = 'Prospects'

    start_urls = urls

    def parse(self, response):
        player_name = response.xpath('//section[@class="plyr_details"]//h1[@class="plytitle"]/text()')[1].re(r'\n\s+(\d{1}.+\d{1})\n')
        date_of_birth = response.xpath('/html/body/section[2]/div/div[1]/div[4]/div[1]/div[1]/div[2]/section/div[6]/div[1]/div[1]/ul/li[1]/div[2]/a/text()').get()
        hometown = response.xpath('/html/body/section[2]/div/div[1]/div[4]/div[1]/div[1]/div[2]/section/div[6]/div[1]/div[1]/ul/li[3]/div[2]/a/text()').get()
        country = response.xpath('/html/body/section[2]/div/div[1]/div[4]/div[1]/div[1]/div[2]/section/div[6]/div[1]/div[1]/ul/li[4]/div[2]/a/text()').get()
        drafted = response.xpath('/html/body/section[2]/div/div[1]/div[4]/div[1]/div[1]/div[2]/section/div[6]/div[2]/ul/li[3]/div[2]/a/text()').re(r'\s(\d+.+\d+)\s')
        position = response.xpath('/html/body/section[2]/div/div[1]/div[4]/div[1]/div[1]/div[2]/section/div[6]/div[1]/div[2]/ul/li[1]/div[2]/text()').re(r'\s+(\w{1,2}/*\w{1,2}/*\w{1,2})\s+') # Grab only the position text without whitespace
        height = response.xpath('/html/body/section[2]/div/div[1]/div[4]/div[1]/div/div[2]/section/div[6]/div[1]/div[2]/ul/li[2]/div[2]/text()').re(r'(\d{3})')

            
            
        yield {
            'player_name': player_name,
            'date_of_brith': date_of_birth,
            'hometown': hometown,
            'country': country,
            'drafted': drafted,
            'position': position,
            'height': height
        }
