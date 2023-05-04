import os
import scrapy
import logging
from scrapy.crawler import CrawlerProcess
import json

# Récupération des descriptifs des postes (missions, formation et compétences requises)  +  tag (secteur, niveau diplômes ...)

# A partir d'une liste d'urls d'offres d'emplois data stockée dans un fichier json
file = open('/Users/leenaomrani/Desktop/final-project/jobs_science_des_données_france/science_des_donnees_jobs.json')
result = json.load(file)
list_url = ["https://www.hellowork.com" + elt["url"] for elt in result] # formatage des urls complètes


class HelloWorkSpiderDetail(scrapy.Spider) :
    
    name = "HelloWorkJobsDetails_science"
        
    #start_urls= ['https://www.hellowork.com/fr-fr/emplois/34814705.html']

    start_urls = list_url
    
    def parse(self, response):

        yield {
            "url_offre" : response.url, 
            "descriptif_job" : response.xpath('/html/body/main/section[1]/section/p/text()').getall(),                                       
            #"descriptif_zone1" : response.xpath('/html/body/main/section[1]/section[1]/p/text()').getall(),
            #"descriptif_zone2" : response.xpath('/html/body/main/section[1]/section[2]/p/text()').getall(), 
            #"descriptif_zone3" : response.xpath('/html/body/main/section[1]/section[3]/p/text()').getall(), 
            #"descriptif_zone4" : response.xpath('/html/body/main/section[1]/section[4]/p/text()').getall(),                                
            #"descriptif_zone5": response.xpath('/html/body/main/section[1]/section[5]/p/text()').getall(),
            #"descriptif_zone6": response.xpath('/html/body/main/section[1]/section[6]/p/text()').getall(),
            "tags" : response.xpath('/html/body/main/section[1]/section[7]/ul[2]/li/text()').getall()
            }

            
filename = "jobs_science_description.json"

if filename in os.listdir("/Users/leenaomrani/Desktop/final-project/jobs_science_des_données_france/") : 
    os.remove("/Users/leenaomrani/Desktop/final-project/jobs_science_des_données_france/" + filename) 

process = CrawlerProcess(settings = {
    'USER_AGENT':    'Chrome/110.0.5481.178',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {''+ filename : {"format": "json"},
    }
})

process.crawl(HelloWorkSpiderDetail)
process.start()