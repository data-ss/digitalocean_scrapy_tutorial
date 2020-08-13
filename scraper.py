import scrapy
# namesake package being used to perform webscraping

# run scraper in terminal using:
# scrapy runspider scraper.py

class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider" # give the spider the name "brickset_spider"
    start_urls = ['http://brickset.com/sets/year-2016']
    # provide the URL to be scraped
    # the HTML in 'start_urls' is grabbed and sent to the 'parse' method

    def parse(self, response):
        SET_SELECTOR = '.set'
        # each set is specified with the class 'set'.
        # So use '.set' for the CSS selector.
        for brickset in response.css(SET_SELECTOR):
        # pass selector into the response object
        # it grabs all the sets on the page and loops over them to extract data
            NAME_SELECTOR = 'h1 ::text'
            # name of each set is stored within h1 tag for each set
            # append ::text to selector for the name. It's a CSS pseudo-selector
            ## that fetches text inside of the "a" tag rather than tag itself
            PIECES_SELECTOR = './/dl[dt/text() = "Pieces"]/dd/a/text()'
            # there is a 'dt' tag containing the text "Pieces",
            ## and then there is a 'dd' tag following it that contains the actual
            ### number of pieces.
            #### Use "XPath" for traversing XML to grab this.
            MINIFIGS_SELECTOR = './/dl[dt/text() = "Minifigs"]/dd[2]/a/text()'
            # Same as above; there is a 'dt' tag containing the text "Minifigs",
            ## followed by a 'dd' tag after with the number.
            IMAGE_SELECTOR = 'img ::attr(src)'
            # images for sets are stored in the 'src' attribute of an 'img' tag
            ## inside an 'a' tag
            yield {
            'name': brickset.css(NAME_SELECTOR).extract_first(),
            # call extract_first() on the object because we just want the first
            ## element that matches the selector. Gives a string rather than
            ### list of elements
            'pieces': brickset.xpath(PIECES_SELECTOR).extract_first(),
            'minifigs': brickset.xpath(MINIFIGS_SELECTOR).extract_first(),
            'image': brickset.css(IMAGE_SELECTOR).extract_first(),
            }
        NEXT_PAGE_SELECTOR = '.next a ::attr(href)'
        # Add functionality to scrape through "Next" pages
        # There is a 'li' tag witht he class 'next'. Inside the tag there's an 'a'
        ## tag with a link to the next page.
        # Make scraper follow that link if it exists.

        # Define a selector for 'next page' link, extract the first match and check
        ## if it exists.
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
            # 'scrapy.Request' is a value to return, effectively saying "Hey crawl
            ## this page".
            response.urljoin(next_page),
            callback=self.parse
            # This says "once you've gotten then HTML from this page, pass it back
            ## to this method so we can parse it, extract data and find the next
            ### page".
            )
