# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
from mmaspider.items import MmaspiderItem, MmaFighterItem, WikiBelEventItem, WikiSFEventItem, WikiEventItem, WikiFighterItem

import pandas as pd
import os





class MmaSpider(scrapy.Spider):
	name = "mmaspider"
	allowed_domains = ["sherdog.com"]
	start_urls = [
		"http://www.sherdog.com/events/recent/%d-page" % x for x in range(1,280)
	]

	def parse(self, response):
		for href in response.xpath('//td/a[@itemprop]/@href'):
			url = response.urljoin(href.extract())
			yield scrapy.Request(url, callback=self.parse_title)
			
	def parse_title(self, response):
		date = response.xpath('/html/body/div[2]/div[2]/div[1]/div/header/div/div[2]/div[2]/span[1]/text()').extract()
		location = response.xpath('/html/body/div[2]/div[2]/div[1]/div/header/div/div[2]/div[2]/span[2]/span/text()').extract()
		match = response.xpath('/html/body/div[2]/div[2]/div[1]/div/header/div/div[1]/h1/span/text()[1]').extract()
		title = response.xpath('/html/body/div[2]/div[2]/div[1]/div/header/div/div[1]/h1/span/text()[2]').extract()
		competition = response.xpath('/html/body/div[2]/div[2]/div[1]/div/header/div/div[1]/h2/div/a/strong/span/text()').extract()

		for i, fight in enumerate(response.xpath(".//*[@itemprop = 'subEvent']")):
			item = MmaspiderItem()
			item['date'] = date
			item['competition'] = competition
			item['title'] = title
			item['location'] = location
			item['match'] = match
			item['fighterOne'] = fight.xpath('.//a/span/text()').extract()[0]
			item['fighterOneUrl'] = fight.xpath('.//a/@href').extract()[0]
			item['fighterOneResult'] = fight.css(".final_result").xpath('text()').extract()[0]
			item['fighterTwo'] = fight.xpath('.//a/span/text()').extract()[1]
			item['fighterTwoResult'] = fight.css(".final_result").xpath('text()').extract()[1]
			if i == 0:
				item['fighterTwoUrl'] = fight.xpath('.//a/@href').extract()[2]
				item['method'] = fight.xpath('.//tr/td/text()').extract()[1]
				item['referee'] = fight.xpath('.//tr/td/text()').extract()[2]
				item['fightRound'] = fight.xpath('.//tr/td/text()').extract()[3]
				item['time'] = fight.xpath('.//tr/td/text()').extract()[4]
				item['fightNum'] = fight.xpath('.//tr/td/text()').extract()[0]
			else:
				item['fighterTwoUrl'] = fight.xpath('.//a/@href').extract()[0]
				item['method'] = fight.xpath('.//td[5]/text()').extract()[0]
				item['referee'] = fight.xpath('.//td[5]/span/text()').extract()[0]
				item['fightRound'] = fight.xpath('.//td[6]/text()').extract()[0]
				item['time'] = fight.xpath('.//td[7]/text()').extract()[0]
				item['fightNum'] = fight.xpath('.//td/text()').extract()[2].strip()
			yield item






"""class fighterSpider(scrapy.Spider):
	df = pd.read_csv(r"../items.csv")
	df1 = df['fighterOneUrl']
	df2 = df1.append(df['fighterTwoUrl'])

	name = "fighterspider"
	allowed_domains = ["sherdog.com"]
	start_urls = [
		"http://www.sherdog.com"
	]

	def parse(self, response):
		for href in df2.unique():
			url = response.urljoin(href)
			yield scrapy.Request(url, callback=self.parse_fighter)

	def parse_fighter(self, response):
		fighter = MmaFighterItem()
		fighter['name'] = response.css('.fn').xpath('text()').extract()

		fighter['dob'] = response.xpath(".//*[@itemprop = 'birthDate']/text()").extract()
		fighter['born'] = response.xpath(".//*[@itemprop = 'addressLocality']/text()").extract()
		fighter['nationality'] = response.xpath(".//*[@itemprop = 'nationality']/text()").extract()
		
		fighter['height'] = response.css('.height').xpath('text()').extract()[2]
		fighter['weight'] = response.css('.weight').xpath('text()').extract()[2]
		fighter['association'] = response.css('.wclass .title a').xpath('text()').extract()
		yield fighter"""


class WikiUFCSpider(scrapy.Spider):
	name = "WikiUfcEventItem"
	allowed_domains = ["wikipedia.org"]
	start_urls = ["https://en.wikipedia.org/wiki/UFC_18"]

	def parse(self, response):
		pass

class wikiBellatorEvent(scrapy.Spider):
	name = "WikiBel"
	allowed_domains = ["wikipedia.org"]
	'''start_urls = ["https://en.wikipedia.org/wiki/Bellator_Fighting_Championships:_Season_Seven"]'''
	start_urls = ["https://en.wikipedia.org/wiki/Bellator_MMA:_2014_Summer_Series"]

	def parse(self, response):

		for x, fight in enumerate(response.css('.toccolours')):
			belevent = WikiBelEventItem()

			belevent['event'] = response.css('.infobox:not(.vevent)').xpath('.//tr[1]/th/text()').extract()[x]
			belevent['date'] = response.css('.infobox:not(.vevent)').xpath('.//tr[3]/td/text()').extract()[x]
			belevent['city'] = response.css('.infobox:not(.vevent)').xpath('.//tr[5]/td/a/text()').extract()[x]
			
			for i in fight.css('tr').xpath('.//td/..'):
				belevent['weightclass'] = i.xpath('.//td[1]/text()').extract()

				if i.xpath('.//td[2]/a/text()').extract():
					belevent['fighterOne'] = i.xpath('.//td[2]/a/text()').extract()
					belevent['fighterOneUrl'] = i.xpath('.//td[2]/a/@href').extract()
				else:
					belevent['fighterOne'] = i.xpath('.//td[2]/text()').extract()

				if i.xpath('.//td[4]/a/text()').extract():
					belevent['fighterTwo'] = i.xpath('.//td[4]/a/text()').extract()
					belevent['fighterTwoUrl'] = i.xpath('.//td[4]/a/@href').extract()
				else:
					belevent['fighterTwo'] = i.xpath('.//td[4]/text()').extract()

				belevent['result'] = i.xpath('.//td[3]/text()').extract()
				belevent['notes'] = i.xpath('.//td[8]/small/text()').extract()
				belevent['method'] = i.xpath('.//td[5]/text()').extract()
				belevent['fightRound'] = i.xpath('.//td[6]/text()').extract()
				belevent['roundTime'] = i.xpath('.//td[7]/text()').extract()
				yield belevent

		next_page = response.xpath('//*[@id="mw-content-text"]/table[1]/tr/td/a/@href').extract()[-1]
		if next_page:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback=self.parse)


class WikiUFCScrape(scrapy.Spider):
	name = "wikiEvent"
	allowed_domains = ["wikipedia.org"]
	start_urls = [
		"https://en.wikipedia.org/wiki/UFC_159"
	]
		

		
	def parse(self, response):
		promo, venue, city  = response.css('.infobox tr td a::text').extract()[0:3]
		date = response.css('.infobox').xpath('tr/td/text()').extract()[2]
		for deets in response.css('.toccolours tr').xpath('.//td/..'):
			eve = WikiEventItem()
			eve['promotion'] = promo
			eve['date'] = date
			eve['venue'] = venue
			eve['city'] = city
			if deets.xpath('.//td[2]/a/text()').extract():
				eve['fighterOne'] = deets.xpath('.//td[2]/a/text()').extract()
				eve['fighterTwo'] = deets.xpath('.//td[4]/a/text()').extract()
			else:
				eve['fighterOne'] = deets.xpath('.//td[2]/text()').extract()
				eve['fighterTwo'] = deets.xpath('.//td[4]/text()').extract()
			
			
			eve['fighterOneUrl'] = deets.xpath('.//td[2]/a/@href').extract()
			eve['fighterTwoUrl'] = deets.xpath('.//td[4]/a/@href').extract()
			eve['fightClass'] = deets.xpath('.//td[1]/text()').extract()
			eve['fighterOneResult'] = deets.xpath('.//td[3]/text()').extract()
			eve['method'] = deets.xpath('.//td[5]/text()').extract()
			eve['fightRound'] = deets.xpath('.//td[6]/text()').extract()
			eve['time'] = deets.xpath('.//td[7]/text()').extract()
			yield eve

		next_page = response.css('.infobox').xpath('//tr/td/table/tr/td[3]/a/@href').extract_first()
		if next_page:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback=self.parse)
		

class wikiSFEvent(scrapy.Spider):
	name = "WikiSF"
	allowed_domains = ["wikipedia.org"]
	'''start_urls = ["https://en.wikipedia.org/wiki/Bellator_Fighting_Championships:_Season_Seven"]'''
	start_urls = ["https://en.wikipedia.org/wiki/Strikeforce:_Diaz_vs._Cyborg"]

	def parse(self, response):

		for x, fight in enumerate(response.css('.toccolours')):
			belevent = WikiSFEventItem()

			belevent['event'] = response.css('.infobox:not(.vevent)').xpath('.//tr/th/text()').extract_first()
			belevent['date'] = response.css('.infobox:not(.vevent)').xpath('.//tr/td/text()').extract()[2]
			belevent['city'] = response.css('.infobox:not(.vevent)').xpath('.//tr/td/a/text()').extract()[2]
			
			for i in fight.css('tr').xpath('.//td/..'):
				belevent['weightclass'] = i.xpath('.//td[1]/text()').extract()

				if i.xpath('.//td[2]/a/text()').extract():
					belevent['fighterOne'] = i.xpath('.//td[2]/a/text()').extract()
					belevent['fighterOneUrl'] = i.xpath('.//td[2]/a/@href').extract()
				else:
					belevent['fighterOne'] = i.xpath('.//td[2]/text()').extract()
					belevent['fighterOneUrl'] = ''

				if i.xpath('.//td[4]/a/text()').extract():
					belevent['fighterTwo'] = i.xpath('.//td[4]/a/text()').extract()
					belevent['fighterTwoUrl'] = i.xpath('.//td[4]/a/@href').extract()
				else:
					belevent['fighterTwo'] = i.xpath('.//td[4]/text()').extract()
					belevent['fighterTwoUrl'] = ''

				belevent['result'] = i.xpath('.//td[3]/text()').extract()
				belevent['notes'] = i.xpath('.//td[8]/small/text()').extract()
				belevent['method'] = i.xpath('.//td[5]/text()').extract()
				belevent['fightRound'] = i.xpath('.//td[6]/text()').extract()
				belevent['roundTime'] = i.xpath('.//td[7]/text()').extract()
				yield belevent

		next_page = response.xpath('//*[@id="mw-content-text"]/table/tr/td/table/tr/td[3]/a/@href').extract()[0]
		if next_page:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback=self.parse)


class wikiFighterScrape(scrapy.Spider):
	name = "WikiFight"
	allowed_domains = ["wikipedia.org"]
	'''start_urls = ["https://en.wikipedia.org/wiki/Bellator_Fighting_Championships:_Season_Seven"]'''
	start_urls = ["https://en.wikipedia.org/wiki/Conor_McGregor"]

	'''df1, df2, df3 = pd.read_csv('belEvents.csv'), pd.read_csv('sfEvents.csv'), pd.read_csv('wikievents.csv')
				df = pd.DataFrame()
				df = df.append([df1, df2, df3])
				fightername = df['fighterOneUrl']
				fightername = fightername.append(df['fighterTwoUrl'])
				fightername = fightername.dropna()
				fightername = fightername.unique()
			
				def parse(self, response):
					for i in fightername:
						url = response.urljoin(i)
						yield scrapy.Request(url, callback=self.parse_fighter)'''
#mw-content-text > table.wikitable.sortable.jquery-tablesorter > tbody
	def parse(self, response):
		
		name = response.css('h1').xpath('text()').extract()

		for history in response.css('.sortable > tbody tr'):
			fighter = WikiFighterItem()
			fighter['name'] = name
			fighter['notes'] = history.xpath('td[10]/small//text()').extract()
			fighter['record'] = history.xpath('td[2]/text()').extract()
			fighter['result'] = history.xpath('td[1]/text()').extract()
			fighter['location'] = history.xpath('td[9]//text()').extract()
			yield fighter


			

		