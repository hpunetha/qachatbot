''' Scraper.
'''

import re
from urllib.parse import urljoin, urlsplit, SplitResult
import requests,pickle
from bs4 import BeautifulSoup
from tqdm import tqdm

class RecursiveScraper:
    ''' Scrape URLs in a recursive manner.
    '''
    def __init__(self, url):
        ''' Constructor to initialize domain name and main URL.
        '''
        self.domain = urlsplit(url).netloc
        self.mainurl = url
        self.urls = set()

    def preprocess_url(self, referrer, url):
        ''' Clean and filter URLs before scraping.
        '''
        if not url:
            return None

        fields = urlsplit(urljoin(referrer, url))._asdict() # convert to absolute URLs and split
        fields['path'] = re.sub(r'/$', '', fields['path']) # remove trailing /
        fields['fragment'] = '' # remove targets within a page
        fields = SplitResult(**fields)
        if fields.netloc == self.domain:
            httpurl = cleanurl = fields.geturl()
            httpsurl = cleanurl = fields.geturl()
            # Scrape pages of current domain only
            if fields.scheme == 'http':
                httpurl = cleanurl = fields.geturl()
                httpsurl = httpurl.replace('http:', 'https:', 1)
            else:
                httpsurl = cleanurl = fields.geturl()
                httpurl = httpurl.replace('https:', 'http:', 1)
            if httpurl not in self.urls and httpsurl not in self.urls:
                # Return URL only if it's not already in list
                return cleanurl

        return None

    def scrape(self, url=None):
        ''' Scrape the URL and its outward links in a depth-first order.
            If URL argument is None, start from main page.
        '''
        if url is None:
            url = self.mainurl

#        print("Scraping {:s} ...".format(url))
        self.urls.add(url)
        if len(list(self.urls))%50==0:
            print('Number of links extracted = '+str(len(list(self.urls))))
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        for link in soup.findAll("a"):
            childurl = self.preprocess_url(url, link.get("href"))
            if childurl:
                self.scrape(childurl)


all_links = []
if __name__ == '__main__':
    rscraper = RecursiveScraper("http://iiitd.ac.in/")
    try:
        rscraper.scrape()
        
            
    except: 
        all_links.append(rscraper.urls)
        f = open('all_iiitd_links.pickle','wb')
        pickle.dump(rscraper.urls,f)
        f.close()
        
    all_links.append(rscraper.urls)
    f = open('all_iiitd_links.pickle','wb')
    pickle.dump(all_links,f)
    f.close()
print(all_links)