import scrapy
import re

# 3. Psychological Science: all articles since badges started in 2014 that have an
# "Open Practices" statement, i.e., starting at Volume 25 Issue 5, May 2014
# (though only 1 article in that issue); 0 in next issue; 6 articles in Issue 7)
# (at least 2 badges)
#  Metadata to extract (from PDF and HTML):
# • title, year, DOI, article type (don't think this is available), abstract text,
# "Keywords", # of downloads (from an article's "metrics" subpage; example),
# "Declaration of Conflicting Interests", article HTML URL (only if open access),
# article PDF URL (sci-hub URL), "Open Practices" statement (extract all URLs and
# save in open.content.URLs field), "Funding", and "Authors Contributions",
# number of views, number of downloads

HOME = "https://journals.sagepub.com"



class PsychScienceSpider(scrapy.Spider):
    name = 'psych_science'

    def start_requests(self):
        start_urls = ['https://journals.sagepub.com/loi/PSS?year=2010-2019']
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_year)

    def parse_year(self, response):
        all_years = response.css('h4 a')
        for year in all_years:
            if int(year.css('::text').get()) >= 2014:
                url_year = f"{HOME}{year.css('::attr(href)').get()}"
                yield scrapy.Request(url_year, callback=self.parse_volumes)

    def parse_volumes(self, response):
        all_issues = response.css('h6 a')
        for issue in all_issues:
            issue_url = issue.css('::attr(href)').get()
            yield scrapy.Request(issue_url, callback = self.parse_issue)

    def parse_issue(self, response):
        """Get articles with at least two badges: open data and open material, or
        open data and preregistration, or open material and preregistration.
        """
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
                    open_article_url = f"{HOME}{badge.css('a::attr(href)').get()}"
                    yield scrapy.Request(open_article_url, callback = self.parse_article)

    def parse_article(self, response):
        def extract_data(title):
            for p_tag in response.xpath('//span[@class="NLM_fn"]'):
                if p_tag.xpath(f'./p/span[contains(text(), "{title}")]') != []:
                    full_text_list = p_tag.xpath('descendant-or-self::*/text()').getall()
                    return ''.join(full_text_list[1::])
        vol_issue_year = response.css('div[class="tocLink"] a::text').get()

        yield {
        'title': response.xpath('normalize-space(//h1/text())').get().strip(),
        'volume': re.search("Vol(.\d+)", vol_issue_year).group(1).strip(),
        'issue': re.search("Issue(.\d+)", vol_issue_year).group(1).strip(),
        'year':  re.search("\d{4}$", vol_issue_year).group(0),
        'doi': response.css('a[class="doiWidgetLink"]::text').get(),
        'abstract': response.xpath('normalize-space(//*[@class="abstractSection abstractInFull"]/p)').getall()[0],
        'keywords': ', '.join(response.css('kwd-group a::text').getall()),
        'url': response.request.url,
        'pdf_url': f"""{HOME}{response.css('a[data-item-name="download-PDF"]::attr(href)').get()}""",
        # 'conflict_of_interests': extract_data("Declaration"),
        # 'funding': extract_data("Funding"),
        # 'open_practices': extract_data("Open Practice"),
        'funding': extract_data("Funding"),
        'acknow': response.xpath('normalize-space(//div[@class="acknowledgement"]/p)').get(),
        }
