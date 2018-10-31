# Scrapping-ProductD
Scrapping of Product names and price from website
Steps:
CRATING A PROJECT:
	To scrap the data from web pages, first you need to create the Scrapy project where you will be storing the code. To create a new directory, run the following command −
	scrapy startproject ProductDetails
	The above code will create a directory with name first_scrapy and it will contain the following structure −
	ProductDetails
    scrapy.cfg            # deploy configuration file

    tutorial/             # project's Python module, you'll import your code from here
        __init__.py

        items.py          # project items definition file

        middlewares.py    # project middlewares file

        pipelines.py      # project pipelines file

        settings.py       # project settings file

        spiders/          # a directory where you'll later put your spiders
            __init__.py
OUR FIRST SPIDER:
	This is the code for our first Spider. Save it in a file named quotes_spider.py under the tutorial/spiders directory in your project:

	import scrapy
	class ProductsSpider(scrapy.Spider):
		name = "products"

		def start_requests(self):
			urls = [
			https://www.joyeverley.co.uk/collections/all?page=1
			https://www.joyeverley.co.uk/collections/all?page=2
			]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

		def parse(self, response):
			page = response.url.split("/")[-2]
			filename = 'joyoverley-%s.html' % page
			with open(filename, 'wb') as f:
			f.write(response.body)
			self.log('Saved file %s' % filename)
	To put our spider to work, go to the project’s top level directory and run:

		scrapy crawl products
	Now, check the files in the current directory. You should notice that new file have been created: joyoverley-collection.html with the content for the respective URLs, as our parse method instructs.

EXTRACTING DATA:
	The best way to learn how to extract data with Scrapy is trying selectors using the shell Scrapy shell. Run:
	$scrapy shell 'https://www.joyeverley.co.uk'
	You will see something like:
	[ ... Scrapy log here ... ]
	2016-09-19 12:09:27 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://quotes.toscrape.com/page/1/> (referer: None)
	[s] Available Scrapy objects:
	[s]   scrapy     scrapy module (contains scrapy.Request, scrapy.Selector, etc)
	[s]   crawler    <scrapy.crawler.Crawler object at 0x7fa91d888c90>
	[s]   item       {}
	[s]   request    <GET https://www.joyeverley.co.uk/collections/all?page=1>
	[s]   response   <200 https://www.joyeverley.co.uk/collections/all?page=2>
	[s]   settings   <scrapy.settings.Settings object at 0x7fa91d888c10>
	[s]   spider     <DefaultSpider 'default' at 0x7fa91c8af990>
	[s] Useful shortcuts:
	[s]   shelp()           Shell help (print this help)
	[s]   fetch(req_or_url) Fetch request (or URL) and update local objects
	[s]   view(response)    View response in a browser
	>>>
	Using the shell, you can try selecting elements using CSS with the response object:
	>>> response.css('title')
	[<Selector xpath='descendant-or-self::title' data='<title>Quotes to Scrape</title>'>]
	The result of running response.css('title') is a list-like object called SelectorList, which represents a list of Selector objects that wrap around XML/HTML elements and allow you to run further queries to fine-grain the selection or extract the data.
	To extract the text from the title above, you can do:
	>>> response.css('title::text').extract()
	['Quotes to Scrape']
	There are two things to note here: one is that we’ve added ::text to the CSS query, to mean we want to select only the text elements directly inside <title> element. If we don’t specify ::text, we’d get the full title element, including its tags:
	>>> response.css('title').extract()
	['<title>Joy Everley Fine Jewellers, London</title>']
	The other thing is that the result of calling .extract() is a list, because we’re dealing with an instance of SelectorList. When you know you just want the first result, as in this case, you can do:
	>>> response.css('title::text').extract_first()
	'Joy Everley Fine Jewellers, London'
	As an alternative, you could’ve written:
	>>> response.css('title::text')[0].extract()
	'Joy Everley Fine Jewellers, London'
	However, using .extract_first() avoids an IndexError and returns None when it doesn’t find any element matching the selection.
	
EXTRACTING PRODUCT NAME AND DETAILS:
	Now that you know a bit about selection and extraction, let’s complete our spider by writing the code to extract the quotes from the web page.
	
	Let’s open up scrapy shell and play a bit to find out how to extract the data we want:
	$ scrapy shell 'https://www.joyeverley.co.uk'
	
	We get a list of selectors for the quote HTML elements with:
	>>> response.css("div.info")
	Each of the selectors returned by the query above allows us to run further queries over their sub-elements. Let’s assign the first selector to a variable, so that we can run our CSS selectors directly on a particular quote:
	>>> quote = response.css("div.info")[0]
	Now, let’s extract name and price from that product using the quote object we just created:
	>>> title = product.css("span.title::text").extract_first()
	>>> title
	''Joy Everley Fine Jewellers, London''
	>>> price = quote.css("span.money::text").extract_first()
	>>> price
	1,295.00 GBP
	Having figured out how to extract each bit, we can now iterate over all the quotes elements and put them together into a Python dictionary:
	>>> for quote in response.css("div.quote"):
	...     text = quote.css("span.text::text").extract_first()
	...     author = quote.css("small.author::text").extract_first()
	...     tags = quote.css("div.tags a.tag::text").extract(	)
	...     print(dict(text=text, author=author, tags=tags))
		{'title': '"sustanable Baroque Diamond Engagement Ring"', 'price': '1,295.00 GBP'}
	...	
	
	
EXTRACTING DATA IN OUR SPIDER:
	Let’s get back to our spider. Until now, it doesn’t extract any data in particular, just saves the whole HTML page to a local file. Let’s integrate the extraction logic above into our spider.
	A Scrapy spider typically generates many dictionaries containing the data extracted from the page. To do that, we use the yield Python keyword in the callback, as you can see below:
	import scrapy
	class ProductSpider(scrapy.Spider):
		name = "products"
		start_urls = [
			'https://www.joyeverley.co.uk/collections/all?page=1',
			'https://www.joyeverley.co.uk/collections/all?page=2',
				]

		def parse(self, response):
			for products in response.css('div.quote'):
				yield {
					'title': quote.css('span.title::text').extract_first(),
					'price': quote.css('small.money::text').extract_first(),
					}
					
	 Run this spider, it will output the extracted data with the log.
	 
STORING THE SCRAPED DATA:
	The simplest way to store the scraped data is by using Feed exports, with the following command:
	$scrapy crawl products -o products.json
	That will generate an quotes.json file containing all scraped items, serialized in JSON.
