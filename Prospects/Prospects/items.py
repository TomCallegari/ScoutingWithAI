# -*- coding: utf-8 -*-

import scrapy


class MetaDataItem(scrapy.Item):

    """ Data structure to store basic player 
    meta data """
    
    ep_id = scrapy.Field()
    full_name = scrapy.Field()
    date_of_birth = scrapy.Field()
    hometown = scrapy.Field()
    country = scrapy.Field()
    youth_team = scrapy.Field()
    position = scrapy.Field()
    height = scrapy.Field()
    weight = scrapy.Field()
    shoots = scrapy.Field()

class PlayerStatsItem(scrapy.Item):

    """Data structure to store player statistics"""

    ep_id = scrapy.Field()
    season = scrapy.Field()
    team = scrapy.Field()
    league = scrapy.Field()
    games_played = scrapy.Field()
    goals = scrapy.Field()
    assists = scrapy.Field()
    penalty_min = scrapy.Field()
    plus_minus = scrapy.Field()