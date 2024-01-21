# Libraries
import scrapy

#Defining parameters limiting the number of pages to scrap:
pages = 2

# Creating scrapy object - Link
class Link(scrapy.Item):
    link = scrapy.Field()

# Creating our spider object
class LinkListsSpider(scrapy.Spider):
    # Defining a name of our spider 
    name = 'link_lists'
    
    allowed_domains = ['https://www.goodreads.com/']
    # Initial request is defined as a list of URLs
    start_urls = ['https://www.goodreads.com/list/show/1.Best_Books_Ever?page=' + str(i) for i in range(1, pages+1)]
    
    # Defining the function 'parse' which accepts a response parameter and extracts the data 
    def parse(self, response):
        # XPATH to the links of each book
        xpath = '//a[@class="bookTitle"]/@href'
        
        # Finding links and storing them as a scrapy object (class Link)
        selection = response.xpath(xpath)
        for s in selection:
            l = Link()
            l['link'] = 'https://www.goodreads.com' + s.get()
            yield l
    