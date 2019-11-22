# Import required packages/modules
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
from time import time
from time import sleep
import pandas as pd
import re
import pickle
from itertools import islice, chain, repeat

# Setup iteratble list for player profile href links
with open('listfile.data', 'rb') as filehandle:
    urls = pickle.load(filehandle)

def chunk_pad(it, size, padval=None):
    it = chain(iter(it), repeat(padval))
    return iter(lambda: tuple(islice(it, size)), (padval,) * size)

player_url_list = list(chunk_pad(urls, 15))


print(len(player_url_list[0]))