import scrapy

HOME = "https://journals.sagepub.com"

class QuotesSpider(scrapy.Spider):
    name = "psych_science"

    def start_requests(self):
        urls = [
            'https://journals.sagepub.com/toc/pssa/28/8',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        from scrapy import Selector

        for article in response.css('tr').getall():
            sel = Selector(text = article)
            access = sel.css('.accessIconContainer div').xpath('./img/@alt').get()
            if access != "No Access" and access != None:
                print(access)
                badge = sel.css('.accessIconContainer').xpath('./following-sibling::td[@valign="top"]/div[@class = "tocDeliverFormatsLinks"]')
                open_data = badge.css('img[class="openData"]')
                open_material = badge.css('img[class="openMaterial"]')
                prereg = badge.css('img[class="preregistration"]')
                if ((open_data != [] and open_material != []) or
                (open_data != [] and prereg != []) or
                (open_material != [] and prereg != [])):
                    print(f"{HOME}{badge.css('a::attr(href)').get()}")
