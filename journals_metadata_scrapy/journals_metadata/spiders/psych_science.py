import scrapy
import re

# HOME = "https://journals.sagepub.com"
#
# urls_psych_science = []
# for i in range(25,31):
#   for j in zip([i]*12, range(1,13)):
#     link = f"{HOME}/toc/pssa/{j[0]}/{j[1]}"
#     urls_psych_science.append(link)

class PsychScienceSpider(scrapy.Spider):
    name = 'psych_science_wrong'

    def start_requests(self):

        # urls = urls_psych_science
        # for url in urls:
        #     yield scrapy.Request(url=url, callback=self.parse)

        url = 'https://journals.sagepub.com/loi/PSS?year=2014'
        scrapy.Request(url=url, callback=self.parse)

    #
    # def parse(self, response):
    #     for issue in





        # item = Psych_Science_Metadata()
        #
        # # scrap open_access articles with at least 2 badges
        # for article in response.css('tr'):
        #     access = article.css('.accessIconContainer div').xpath('./img/@alt').get()
        #     if access != "No Access" and access != None:
        #         badge = article.css('.accessIconContainer').xpath('./following-sibling::td[@valign="top"]/div[@class = "tocDeliverFormatsLinks"]')
        #         open_data = badge.css('img[class="openData"]')
        #         open_material = badge.css('img[class="openMaterial"]')
        #         prereg = badge.css('img[class="preregistration"]')
        #         if ((open_data != [] and open_material != []) or
        #         (open_data != [] and prereg != []) or
        #         (open_material != [] and prereg != [])):
        #             link = badge.css('a::attr(href)').get()
        #
        #     yield scrapy.Request(link, callback=self.parse_article)
        #
        #
        # def parse_article(self, response):
        #     print(response.status)






                    # link = f"{HOME}{badge.css('a::attr(href)').get()}"
                    # vol_issue_year = response.css('div[class="journalNavTitle"]::text').get()
                    # vol_issue_year_edited = vol_issue_year.strip()
                    # volume =  re.search("Volume(.\d+)", vol_issue_year_edited).group(1).strip()
                    # issue =  re.search("Issue(.\d+)", vol_issue_year_edited).group(1).strip()
                    # year =  re.search("\d{4}$", vol_issue_year_edited).group(0)




    #
    #                 yield {
    #                 'access': access,
    #                 'link' : link,
    #                 'vol_issue_year' : vol_issue_year_edited,
    #                 'volume' : volume,
    #                 'issue' : issue,
    #                 'year' : year
    #                 }
    #
    #                 if link is not None:
    #                     yield response.follow(link, callback=self.parse_article)
    #
    # def parse_article(self, response):
    #     yield {
    #     'title': response.xpath('normalize-space(.//h1)').get()
    #     }
