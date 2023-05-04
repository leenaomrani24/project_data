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
    def parse(self, response):
        offres = response.xpath('/html/body/main/section/div/section/ul[1]/li') #/html/body/main/section/div/section/ul[1]/li#

        for elt in offres:
            # récupération des informations clé toutes pages
            yield {
                "id_offre": elt.xpath('div').attrib['id'],
                "entreprise": elt.xpath('div/div[2]/div[1]/span[1]/span/text()').get(),
                "type_contrat": elt.xpath('div/div[2]/div[1]/div/div[1]/span/text()').get(),
                "titre_job":  elt.xpath('div/div[2]/div[1]/span[2]/h3/a/text()').getall(),
                "localisation": elt.xpath('div/div[2]/div[1]/div/div[2]/span/span/text()').get(),
                "date_de_publication": elt.xpath('div/div[2]/div[2]/div[1]/span/span/text()').getall(),
                "modalites_de_tetetravail": elt.xpath('div/div[2]/div[1]/div/div[3]/span/span/text()').getall(),
                "url": elt.xpath('div/div[2]/div[1]/span[2]/h3/a').attrib['href'],
                "duree_du_contrat": elt.xpath('div/div[2]/div[1]/div/div[4]/span/span/text()').getall(),
                "tag recruteur_reactif": elt.xpath('div/div[2]/div[1]/span[1]/span[2]/span/text()').getall(),
            }


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