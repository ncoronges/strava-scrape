import requests
import json
import os
from lxml import html
import re

class StravaSpider():

    def parse_data(self, index, entry):
        #print ("saving file: data/"+entry["id"]+".json")
        #with open('data/'+entry["id"]+".json", 'w') as outfile:
        #    json.dump(entry, outfile)
        #soup = BeautifulSoup(entry, "html.parser")
        #title = soup.title.string
        tree = html.fromstring(entry)
        title = tree.xpath('//title/text()')[0]
        print ("title: "+title)
        m = re.search( '^(.*?) \| Cyclist on Strava', title)
        if (m and m.group(1)):
            name = m.group(1)
            print ("name: "+ name + " index: "+str(index))
            t = tree.xpath("//span[@class='count']/text()")[0]
            print ("count: "+ t)



    def scrape_entries(self):
        more_results = True
        errors_cons = 0
        index = 0
        processed = 0
        while(index<600000):
            url = 'https://www.strava.com/athletes/'+str(index)
            try:
                r = requests.get(url)
                assert r.status_code==200, "error getting detail for: "+url
                self.parse_data(index, r.content)
                errors_cons = 0
                processed += 1
            except AssertionError:
                errors_cons += 1
                print("error getting data for: "+url+". consecutive errors: "+str(errors_cons))
            #if(errors_cons>10):
            #    more_results = False
            index+=1
            if(index%100 == 0):
                print("scraped "+str(processed)+" entries. index: "+str(index))
        print("done! processed "+str(processed)+" in total.")


spider = StravaSpider()
spider.scrape_entries()
