# CurateScienceBots
The project scraps metadata of research articles from academic journals such as Psychological Science, Collabra: Psychology, Journal of Cognition to feed database of [Curate Science](https://curatescience.org/app/).

[Curate Science](https://curatescience.org/app/) is a platform whose goal is to help in verification of transparency and credibility of the research.

## Extracted data

The extracted data looks like this sample:

    {
        'title': 'A New Replication Norm for Psychology',
        'year': '2015',
        'article_type': 'Original research report',
        'doi': '10.1525/collabra.23',
        'keywords': 'Independent replication, cumulative knowledge, replication norm',
        'peer_review_url': 'http://dx.doi.org/10.1525/collabra.23.opr',
        'conflict_of_interests': 'The author declares that they have no competing interests.',
        'vies': '2244',
        'downloads': '412'
    }


## Spiders

This project contains three spiders and you can list them using the `list`
command:

    $ scrapy list
    collabra
    jofcognition
    psych_science

Both spiders extract similar metadata. 

You can learn more about the spiders by going through the
[Scrapy Tutorial](http://doc.scrapy.org/en/latest/intro/tutorial.html).


## Running the spiders

You can run a spider using the `scrapy crawl` command, such as:

    $ scrapy crawl collabra
    $ scrapy crawl jofcognition
    $ scrapy crawl psych_science


If you want to save the scraped data to a file, you can pass the `-o` option:
    
    $ scrapy crawl psych_science -o psychological_science.csv
 
<img src="https://pbs.twimg.com/profile_images/1079541522863800320/p0FxpVnr_400x400.jpg" alt="CS logo" width="150"/>  
