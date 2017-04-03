# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MmaspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date = scrapy.Field()
    competition = scrapy.Field()
    title = scrapy.Field()
    location = scrapy.Field()
    match = scrapy.Field()
    fightNum = scrapy.Field()
    fighterOne = scrapy.Field()
    fighterOneUrl = scrapy.Field()
    fighterOneResult = scrapy.Field()
    fighterTwo = scrapy.Field()
    fighterTwoUrl = scrapy.Field()
    fighterTwoResult = scrapy.Field()
    method = scrapy.Field()
    fightRound = scrapy.Field()
    time = scrapy.Field()
    referee = scrapy.Field()

class MmaFighterItem(scrapy.Item):
	name = scrapy.Field()
	url = scrapy.Field()
	dob = scrapy.Field()
	height = scrapy.Field()
	weight = scrapy.Field()
	born = scrapy.Field()
	association = scrapy.Field()
	weight = scrapy.Field()
	record = scrapy.Field()
	