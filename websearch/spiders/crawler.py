import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
#from scrapy.contrib.linkextractors import LxmlLinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from ..items import WebsearchItem
from bs4 import BeautifulSoup
from bs4.element import Comment
import pickle
import json

class WebsearchSpider(CrawlSpider):
    name = "uic_crawler"
    count = 0
    crawled_links=set()
    links_dict={}
    to_outlinks={}
    allowed_domains=['uic.edu']
    start_urls = [
       'https://cs.uic.edu/'
    ]
    rules = [Rule(LxmlLinkExtractor(deny=('#',r'\?','tel:','mailto:',r'login\.uic\.edu',r'google\.com',r'login\.asp'),allow_domains=('uic.edu'),deny_domains=('login.uic.edu','.com','.net',"doc","?",'google.com'),
                                deny_extensions=('pdf','zip','img'),unique=True,canonicalize=True), callback='get_contents', follow=True)]
    
    # def parse(self,response):
    #     for link in response.css("a::attr('href')"):x
    #         url = response.urljoin(link.extract())
    #         self.count+=1 
    #         yield scrapy.Request(url,callback=self.get_contents)

    def get_contents(self,response):
        link = response.url.replace('http:','https:')
        if '?' in response.request.url or 'login.uic.edu' in response.request.url or '.com' in response.request.url or link in self.crawled_links:
            yield
        else:
            outlinks=set()
            items = {}
            origin_url = response.url.replace('http:','https:')
            self.crawled_links.add(origin_url)
            items['origin_link'] = origin_url
            title = response.css("title::text").extract_first().strip()
            items['title'] = title
            soup = BeautifulSoup(response.text,"lxml")
            for div in soup.find_all("div", {'class': 'browser-stripe'}):
                div.decompose()
            try:
                # remove header, footer and sidebar navigations
                if soup.find('div',class_= 'sidebar_content') != None:
                    soup.find('div',class_= 'sidebar_content').decompose()   
                if soup.find('div', class_='nav-links')!= None:
                    soup.find('div', class_='nav-links').decompose()
                if soup.find('footer', id='footer')!= None:    
                    soup.find('footer', id='footer').decompose()        
                # remove all script and css styling
                for script in soup(["script", "style"]):
                    script.extract()
                # extract only the te
            except Exception as e:
                print(e)

            contents = soup.findAll(text=True)
            visible_texts = filter(self.tag_visible, contents)  
            items['contents']=u" ".join(t.strip() for t in visible_texts)
            '''
            texts = []
            contents = soup.findAll('p')
            for each in contents[2:]:
                for line in each.getText().split("\n"):
                    texts.append(line.strip())
            items['contents'] =' '.join(texts)'''
            pagelinks = LinkExtractor(allow=('uic.edu'),deny=('.com'),canonicalize=True,unique=True).extract_links(response)
            for link in pagelinks:
                if (not link.url == response.url) and link.url not in outlinks:
                    outlinks.add(link.url.replace('http:','https:'))
            self.to_outlinks[origin_url] = outlinks   
            items['outlinks'] = list(outlinks)
            filename = "json_files/%s.json"%self.count
            with open(filename,"w+") as f:
                json.dump(items,f,ensure_ascii=False,indent = 4)
            f.close()
            self.links_dict[filename]= items['origin_link'] 
            self.count+=1
            yield {"response url":response.url}

    def closed(self, reason):
        print("Finished Crawling")
        with open("files_link", 'wb') as pickle_file:
            pickle.dump(self.links_dict, pickle_file)
        with open("out_links", 'wb') as pickle_file:
            pickle.dump(self.to_outlinks, pickle_file)
        with open("crawled_links.txt",'w+') as f:
            for line in self.crawled_links:
                f.write(str(line) + '\n')
        #pickle.dump(self.links_dict, pickle_file)
        print("Added dict to the pickle")

    def tag_visible(self,element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]','footer','menu','img','form','input','noscript','svg','path']:
            return False
        if isinstance(element, Comment):
            return False
        return True