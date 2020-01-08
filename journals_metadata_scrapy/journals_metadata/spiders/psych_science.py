import scrapy

HOME = "https://journals.sagepub.com"

urls_psych_science = []
for i in range(25,31):
  for j in zip([i]*12, range(1,13)):
    link = f"{HOME}/toc/pssa/{j[0]}/{j[1]}"
    urls_psych_science.append(link)

class PsychScienceSpider(scrapy.Spider):
    name = 'psych_science'

    def start_requests(self):

        urls = urls_psych_science

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # scrap open_access articles with at least 2 badges
        for article in response.css('tr'):
            access = article.css('.accessIconContainer div').xpath('./img/@alt').get()
            if access != "No Access" and access != None:
                badge = article.css('.accessIconContainer').xpath('./following-sibling::td[@valign="top"]/div[@class = "tocDeliverFormatsLinks"]')
                open_data = badge.css('img[class="openData"]')
                open_material = badge.css('img[class="openMaterial"]')
                prereg = badge.css('img[class="preregistration"]')
                if ((open_data != [] and open_material != []) or
                (open_data != [] and prereg != []) or
                (open_material != [] and prereg != [])):
                    vol_issue = response.css('div[class="journalNavTitle"]::text').get()
                    link = f"{HOME}{badge.css('a::attr(href)').get()}"
                    yield {
                    'access': access,
                    'link' : link,
                    'vol_issue' : vol_issue.strip()
                    }
