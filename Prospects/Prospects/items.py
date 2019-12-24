# -*- coding: utf-8 -*-

import scrapy


class MetaItems(scrapy.Item):

    """Item class to store player meta data"""
    
    #ep_id = scrapy.Field()
    full_name = scrapy.Field()
    # date_of_birth = scrapy.Field()
    # hometown = scrapy.Field()
    # country = scrapy.Field()
    # youth_team = scrapy.Field()
    # position = scrapy.Field()
    # height = scrapy.Field()
    # weight = scrapy.Field()
    # shoots = scrapy.Field()
    # draft = scrapy.Field()
    # cap_hit = scrapy.Field()
    # scout_text = scrapy.Field()

class RegularItems(scrapy.Item):

    """Item class to store player statistics"""

    ep_id = scrapy.Field()
    season = scrapy.Field()
    team = scrapy.Field()
    league = scrapy.Field()
    games_played = scrapy.Field()
    goals = scrapy.Field()
    assists = scrapy.Field()
    penalty_min = scrapy.Field()
    plus_minus = scrapy.Field()

class PostItems(scrapy.Item):

    """Item class to store player career postseason statistics"""

    ep_id = scrapy.Field()
    season = scrapy.Field()
    games_played = scrapy.Field()
    goals = scrapy.Field()
    assists = scrapy.Field()
    penalty_min = scrapy.Field()
    plus_minus = scrapy.Field()

class InterItems(scrapy.Item):

    """Item class to store player international tournament statistics"""

    ep_id = scrapy.Field()
    season = scrapy.Field()
    tour_level = scrapy.Field()
    games_played = scrapy.Field()
    goals = scrapy.Field()
    assists = scrapy.Field()
    penalty_min = scrapy.Field()
    plus_minus = scrapy.Field()

class TourItems(scrapy.Item):

    """Item class to store player career alternate tournament statistics"""

    ep_id = scrapy.Field()
    season = scrapy.Field()
    team = scrapy.Field()
    level = scrapy.Field()
    games_played = scrapy.Field()
    goals = scrapy.Field()
    assists = scrapy.Field()
    penalty_min = scrapy.Field()
    plus_minus = scrapy.Field()
