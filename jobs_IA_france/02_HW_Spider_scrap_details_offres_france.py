import os
import scrapy
import logging
from scrapy.crawler import CrawlerProcess
import json

# Récupération des descriptifs des postes (missions, formation et compétences requises)  +  tag (secteur, niveau diplômes ...)

# A partir d'une liste d'urls d'offres d'emplois data stockée dans un fichier json
file = open("/Users/leenaomrani/Desktop/final-project/jobs_IA_france/jobs_AI_france.json")
result = json.load(file)
list_url = ["https://www.hellowork.com" + elt["url"] for elt in result] # formatage des urls complètes


class HelloWorkSpiderDetail(scrapy.Spider) :
    
    name = "HelloWorkJobsDetails"
        
    #start_urls= ['https://www.hellowork.com/fr-fr/emplois/30312082.html', 'https://www.hellowork.com/fr-fr/emplois/25840111.html', 'https://www.hellowork.com/fr-fr/emplois/34171033.html']

    start_urls = list_url
    
    def parse(self, response):

        yield {
            "url_offre" : response.url, 
                                                  
            #"descriptif_zone1" : response.xpath('/html/body/main/section[1]/section[1]/p/text()').getall(),
            #"descriptif_zone2" : response.xpath('/html/body/main/section[1]/section[2]/p/text()').getall(), 
            #"descriptif_zone3" : response.xpath('/html/body/main/section[1]/section[3]/p/text()').getall(), 
            #"descriptif_zone4" : response.xpath('/html/body/main/section[1]/section[4]/p/text()').getall(),                                
            #"descriptif_zone5": response.xpath('/html/body/main/section[1]/section[5]/p/text()').getall(),
            #"descriptif_zone6": response.xpath('/html/body/main/section[1]/section[6]/p/text()').getall(),
            "tags_secteur" : response.xpath('/html/body/main/section[1]/section[7]/ul[2]/li/text()').getall(),
            "tags_education":response.xpath('/html/body/main/section[1]/section[3]/ul[2]/li[2]/text()').getall()
            }

            
filename = "all_IA_France_tags.json"

if filename in os.listdir("/Users/leenaomrani/Desktop/final-project/jobs_IA_france/") : 
    os.remove("/Users/leenaomrani/Desktop/final-project/jobs_IA_france/" + filename) 

process = CrawlerProcess(settings = {
    'USER_AGENT':    'Chrome/110.0.5481.178',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {'/Users/leenaomrani/Desktop/final-project/jobs_IA_france/'+ filename : {"format": "json"},
    }
})

process.crawl(HelloWorkSpiderDetail)
process.start()
