import scrapy

from scrapy.loader import ItemLoader

from ..items import KdbankdeItem
from itemloaders.processors import TakeFirst


class KdbankdeSpider(scrapy.Spider):
	name = 'kdbankde'
	start_urls = ['https://www.kd-bank.de/wir_fuer_sie/bank-blog.html']

	def parse(self, response):
		post_links = response.xpath('//*[(@id = "main-content")]//li/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		data = response.xpath('//h1/text()|//main[@id="main-content"]//h2/text()').get()
		try:
			data = data.split(')')
			title = data[1]
			date = data[0][1:]
		except:
			title = data
			date = ''
		description = response.xpath('//div[@class="module module-text-with-media ym-clearfix"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()


		item = ItemLoader(item=KdbankdeItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
