import scrapy
from scrapy import Request
from scrapy import Spider

class CafranSpider(scrapy.Spider):
    name = "cafran"
    allowed_domains = ["cafran.cl"]
    start_urls = ["https://cafran.cl"]

    def parse(self, response):
        categories = response.xpath('//a[@class="menu-link"]/@href').extract()
        for category in categories:
            yield Request(category, callback= self.parse_product)

    def parse_product(self, response):
        products = response.xpath('//*[@class="entry clr"]//div[@class="e-con-inner"]')
        for product in products:
            img_url = product.xpath('.//img/@src').extract()
            name = product.xpath('.//p/../../..//h2/text()').get()
            description = product.xpath('.//p//text()').get()
            sku = product.xpath('.//h2[contains(.,"SKU:")]/text()').get()
            if sku:
                sku = sku.replace("'SKU: ","").strip()
            price = product.xpath('.//h2[contains(.,"Precio:")]/text()').get()
            if price:
                price = price.replace("Precio: ", "").replace(" + IVA", "").strip()
          
            data = {
                'img_url' : img_url,
                'name' : name,
                'description' : description,
                'sku' : sku,
                'price' : price }
            
            yield data