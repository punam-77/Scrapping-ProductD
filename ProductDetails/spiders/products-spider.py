import scrapy


class ProductsSpider(scrapy.Spider):
    name = "products"
	#response = "a"

    def start_requests(self):
        urls = [
            'https://www.joyeverley.co.uk/collections/all?page=1',
            'https://www.joyeverley.co.uk/collections/all?page=2',

		]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'joyeverley-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
	
    def parse(self, response) :
        for products in response.css('div.info'):
            yield {
                'title': products.css('span.title::text').extract_first(),
                'price': products.css('small.price::text').extract_first(),
            
            }
	
    #for products in response.css("div.info"):
	 #   title = products.css("span.title::text").extract_first()
	  #  price = products.css("span.money::text").extract_first()
	   # print(dict(title=title,price=money))
    #{'title': '"sustanable Baroque Diamond Engagement Ring"', 'price': '1,295.00 GBP'}
