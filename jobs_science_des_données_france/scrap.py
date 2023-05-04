import os
import scrapy
import logging
from scrapy.crawler import CrawlerProcess


class HelloWorkSpider(scrapy.Spider):

    name = "HelloWorkJobs"
    # setup des urls à scraper  :
    NB_pages = 59

    start_urls = [
'https://www.hellowork.com/fr-fr/emploi/recherche.html?k=science+donn%C3%A9es&l=france&l_autocomplete=france&ray=20&d=all&c=CDI&c=CDD&c=Travail_temp&p={}&mode=scroll/'.format(i) for i in range(1, NB_pages)]

    def parse_job_page(self, response):
        # extract the job description
        description = response.xpath('/html/body/main/section[1]/div/div/div[1]/div/div[2]/section[1]/div/p/text()').get()
        yield {
            "id_offre": response.url.split("/")[-1].split(".")[0],
            "entreprise": response.xpath('/html/body/main/section[1]/div/div/div[1]/div/div[2]/section[1]/div/h2/a/text()').get(),
            "type_contrat": response.xpath('/html/body/main/section[1]/div/div/div[1]/div/div[2]/section[2]/ul/li[2]/text()').get(),
            "titre_job": response.xpath('/html/body/main/section[1]/div/div/div[1]/div/div[2]/section[1]/div/h1/text()').get(),
            "localisation": response.xpath('/html/body/main/section[1]/div/div/div[1]/div/div[2]/section[2]/ul/li[1]/text()').get(),
            "date_de_publication": response.xpath('/html/body/main/section[1]/div/div/div[1]/div/div[2]/section[2]/ul/li[3]/text()').get(),
            "modalites_de_tetetravail": response.xpath('/html/body/main/section[1]/div/div/div[1]/div/div[2]/section[2]/ul/li[5]/text()').get(),
            "url": response.url,
            "duree_du_contrat": response.xpath('/html/body/main/section[1]/div/div/div[1]/div/div[2]/section[2]/ul/li[4]/text()').get(),
            "tag recruteur_reactif": response.xpath('/html/body/main/section[1]/div/div/div[1]/div/div[2]/section[1]/div/div/span[2]/span/text()').get(),
            "description": description.strip() if description else ""
        }

    def parse(self, response):
        offres = response.xpath('/html/body/main/section/div/section/ul[1]/li') #/html/body/main/section/div/section/ul[1]/li#

        for elt in offres:
            # récupération des informations clé toutes pages
            offer_url = elt.xpath('div/div[2]/div[1]/span[2]/h3/a').attrib['href']
            yield scrapy.Request(offer_url, callback=self.parse_job_page)

filename = "science_des_donnees_jobs.json"

if filename in os.listdir("/Users/leenaomrani/Desktop/final-project/jobs_science_des_données_france/"):
    os.remove(
        "/Users/leenaomrani/Desktop/final-project/jobs_science_des_données_france/" + filename)

process = CrawlerProcess(settings={
    'USER_AGENT':    'Chrome/110.0.5481.178',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {'/Users/leenaomrani/Desktop/final-project/jobs_science_des_données_france/' + filename: {"format": "json"},
              }
})

process.crawl(HelloWorkSpider)
process.start()