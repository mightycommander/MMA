# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
from mmaspider.items import MmaspiderItem, MmaFighterItem
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



df = pd.read_csv(r'items.csv')
df1 = df['fighterOneUrl']
df2 = df1.append(df['fighterTwoUrl'])


class fighterSpider(scrapy.Spider):


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
		yield fighter
	