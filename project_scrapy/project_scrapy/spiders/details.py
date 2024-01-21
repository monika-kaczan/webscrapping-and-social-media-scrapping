# Libraries
import scrapy

#Defining parameters limiting the number of pages to scrap:
limit=True

# Creating scrapy object - Book - with diffrents to be scrapped
class Book(scrapy.Item):
    title          = scrapy.Field()
    author         = scrapy.Field()
    year           = scrapy.Field()
    publisher      = scrapy.Field()
    genre          = scrapy.Field()
    votes          = scrapy.Field()
    rating         = scrapy.Field()
    pages          = scrapy.Field()

# Creating our spider object
class LinksSpider(scrapy.Spider):
    # Defining a name of our spider 
    name = 'books'
    allowed_domains = ['www.goodreads.com']
    # Initial request list is obtained fromm the *.csv file
    try:
        with open("link_lists.csv", "rt") as f:
            if limit:
                start_urls = [url.strip() for url in f.readlines()][1:101]
            else:
                start_urls = [url.strip() for url in f.readlines()][1:]         
    except:
        start_urls = []
    
    # Defining the function 'parse' which accepts a response parameter and extracts the data 
    def parse(self, response):
        
        # Creating an object from a class Book
        p = Book()
        # XPATHs for each field
        title_xpath          = '//h1[@id="bookTitle"]/text()'
        author_xpath         = '//span[@itemprop="name"]/text()'
        year_xpath           = '(//div[@id="details"]/div[@class="row"])[2]/text()'
        publisher_xpath      = '(//div[@id="details"]/div[@class="row"])[2]/text()'
        genre_xpath          = '//a[@class="actionLinkLite bookPageGenreLink"]/text()'
        votes_xpath          = '//meta[@itemprop="ratingCount"]/@content'
        rating_xpath         = '//span[@itemprop="ratingValue"]/text()'
        pages_xpath          = '//span[@itemprop="numberOfPages"]/text()'
        
        # Storing our data as an item 'p'
        p['title']           = [x.strip() for x in response.xpath(title_xpath).getall()]
        p['author']          = response.xpath(author_xpath).getall()[0]
        try:
            p['year']        = response.xpath(year_xpath).re('[0-9]{4}')
        except:
            p['year']        = ''
        try:
            p['publisher']   = response.xpath(publisher_xpath).re('by.+')[0].strip()[3:]
        except:
            p['publisher']   = ''
        p['genre']           = response.xpath(genre_xpath).getall()[0]
        p['votes']           = response.xpath(votes_xpath).getall()
        p['rating']          = [x.strip() for x in response.xpath(rating_xpath).getall()]
        p['pages']           = response.xpath(pages_xpath).re('[0-9]+')
        
        
        yield p
