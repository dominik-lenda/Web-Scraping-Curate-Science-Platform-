import scrapy



class PsychScienceSpider(scrapy.Spider):
    name = 'test'



    def start_requests(self):
          start_urls = ['https://journals.sagepub.com/doi/full/10.1177/0956797618815441']
          for url in start_urls:
              yield scrapy.Request(url=url, callback=self.parse_article)


    def parse_article(self, response):
        print(response.xpath('//span[@class="NLM_fn"]'))
