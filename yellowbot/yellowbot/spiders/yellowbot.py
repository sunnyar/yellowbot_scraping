from scrapy.http import Request
from yellowbot.items import YellowbotItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import log, signals
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import urlparse
from scrapy.xlib.pydispatch import dispatcher
from scrapy import log, signals

class YellowbotSpider(CrawlSpider) :

    handle_httpstatus_list = [302, 400, 404, 500]
    name = 'yellowbot'
    allowed_domains = ['yellowbot.com']

    def __init__(self, category=None, city=None, state=None, *a, **kw) :

        self.locality   = city
        self.region     = state
        self.start_urls = "http://www.yellowbot.com/search?lat=&long=&q={0}&place={1}%2C+{2}".format(category, city, state)
        self.rules      = (
                            Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//div[@class="paginationContent"]/ul/li/a[contains(., "Next")]')), callback="parse_listings", follow=True),
                          )

        dispatcher.connect(self.handle_spider_closed, signals.spider_closed)
        super(YellowbotSpider, self).__init__(*a, **kw)

    def start_requests(self):

        yield Request(url=self.start_urls)


    def parse_start_url(self, response) :

        return self.parse_listings(response)


    def parse_listings(self, response) :

        links  = response.xpath('//div[contains(@class, "resultWrapper")]//h3/a/@href').extract()
        base_url = 'http://www.yellowbot.com'

        if links :
            for link in links :
                item_url = urlparse.urljoin(base_url, link)
                yield Request(item_url, callback=self.parse_details)
        else :
            no_result = \
                response.xpath('//div[@class="innerDetailsSubContent"]//div[@class="yui-b generic"]/h4/text()').extract()

            if no_result :
                item = YellowbotItem()
                item['name'] = no_result[0].strip()
                yield item


    def parse_details(self, response) :

        item = YellowbotItem()
        log.msg("Link Details", level=log.INFO)

        city = response.xpath('//span[@class="locality"]/text()').extract()
        state = response.xpath('//span[@class="region"]/text()').extract()

        if city and state :
            city  = city[0].strip()
            state = state[0].strip()
            if (city == 'Tulsa' and state == 'OK') or (city == 'Erie' and state == 'PA'):
                item['name'] = response.xpath('//h1[@class="fn"]/text()').extract()[0].strip()
                item['city'] = city
                item['state'] = state

                postal = response.xpath('//span[@class="postal-code"]/text()').extract()
                if postal :
                    item['postal'] = postal[0].strip()
                else :
                    item['postal'] = 'NA'

                street_address = response.xpath('//span[@class="street-address"]/text()').extract()
                if street_address :
                    item['address'] = street_address[0].strip()
                else :
                    item['address'] = 'NA'

                website = response.xpath('//dd[@class="url"]/a/@href').extract()
                if website :
                    item['website'] = website[0].strip()
                else :
                    item['website'] = 'NA'

                phone = response.xpath('//dd[@class="tel"]/text()').extract()
                if phone :
                    item['phone'] = phone[0].strip()
                else :
                    item['phone'] = 'NA'

                item['tags'] = ', '.join(response.xpath('//div[@class="htmltagcloud"]//a/text()').extract())

                description = response.xpath('//div[@id="business-descriptions"]/div[@class="review-block"]/p/text()').extract()
                item['description'] = ', '.join([detail for detail in description if '\n' not in detail])

                return item

        return item

    def handle_spider_closed(self, spider) :
        log.msg("Pipeline.spider_closed called", level=log.INFO)
