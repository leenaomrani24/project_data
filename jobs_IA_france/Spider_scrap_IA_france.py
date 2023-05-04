import os
import scrapy
import logging
from scrapy.crawler import CrawlerProcess


class HelloWorkSpider(scrapy.Spider):

    name = "HelloWorkJobs"
    # setup des urls à scraper  :
    NB_pages = 460
    #'https://www.hellowork.com/fr-fr/emploi/recherche.html?k=IA&l=France&l_autocomplete=http%3A%2F%2Fwww.rj.com%2Fcommun%2Flocalite%2Fpays%2FFR&ray=20&d=all&c=CDI&c=Travail_temp&c=CDD&p={}&mode=scroll/'
    start_urls = [
         'https://www.hellowork.com/fr-fr/emploi/recherche.html?k=IA&l=France&l_autocomplete=http%3A%2F%2Fwww.rj.com%2Fcommun%2Flocalite%2Fpays%2FFR&ray=20&d=all&c=CDI&c=Travail_temp&c=CDD&p={}&mode=scroll/'.format(i) for i in range(1, NB_pages)]
    def parse(self, response):
        offres = response.xpath('/html/body/main/section/div/section/ul[1]/li')

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
                "tag recruteur_reactif": elt.xpath('div/div[2]/div[1]/span[1]/span[2]/span/text()').getall()
            }


filename = "jobs_AI_france.json"

if filename in os.listdir("/Users/leenaomrani/Desktop/final-project/jobs_IA_france"):
    os.remove(
        "/Users/leenaomrani/Desktop/final-project/jobs_IA_france" + filename)

process = CrawlerProcess(settings={
    'USER_AGENT':    'Chrome/110.0.5481.178',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {'/Users/leenaomrani/Desktop/final-project/jobs_IA_france' + filename: {"format": "json"},
              }
})

process.crawl(HelloWorkSpider)
process.start()
