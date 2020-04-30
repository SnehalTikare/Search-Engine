import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
#from scrapy.contrib.linkextractors import LxmlLinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from ..items import WebsearchItem
from bs4 import BeautifulSoup
from bs4.element import Comment
import pickle

class WebsearchSpider(CrawlSpider):
    name = "uic"
    count = 0
    crawled_links=set()
    links_dict={}
    to_outlinks={}
    allowed_domains=['uic.edu']
    start_urls = [
       'https://cs.uic.edu/'
    ]
    rules = [Rule(LxmlLinkExtractor(deny=('#','\?','tel:','mailto:','login\.uic\.edu','google\.com','login\.asp'),allow_domains=('uic.edu'),deny_domains=('login.uic.edu','.com','.net',"doc","?",'google.com'),
                                deny_extensions=('pdf','zip','img'),unique=True,canonicalize=True), callback='get_contents', follow=True)]
    
    # def parse(self,response):
    #     for link in response.css("a::attr('href')"):x
    #         url = response.urljoin(link.extract())
    #         self.count+=1 
    #         yield scrapy.Request(url,callback=self.get_contents)

    def get_contents(self,response):
        if '?' in response.request.url or 'login.uic.edu' in response.request.url or '.com' in response.request.url:
            yield
        else:
            outlinks=set()
            items = WebsearchItem()
            origin_url = response.request.url
            #Get all outlinks from a page
            obj = scrapy.Selector(response)
            for link in obj.xpath('*//a/@href').extract():
                if link.startswith('tel:') or link.startswith('mailto:') or link.startswith('#') or '.com' in link or '?' in link:
                    continue
                if 'http' not in link:
                    if link[0]!="/":
                        outlinks.add(origin_url + "/" + link)
                    else:
                        outlinks.add(origin_url + link)
                else:
                    outlinks.add(link) 
            self.to_outlinks[origin_url] = outlinks   
            title = response.css("title::text").extract_first().strip()
            contents = response.css(".components")
            self.crawled_links.add(origin_url)
            items['origin_link'] = origin_url
            items['title'] = title
            contents_stripped= contents.css("p::text").getall()
            #items['contents'] = u" ".join(t.strip() for t in contents_stripped)
            soup = BeautifulSoup(response.text,"lxml")
            comments = soup.findAll(text=lambda text:isinstance(text, Comment))
            for comment in comments:
                    comment.extract()
            for div in soup.find_all("div", {'class': 'browser-stripe'}):
                div.decompose()
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
            # extract only the text and strip extra line breaks
            page_text = soup.get_text(" ", strip=True)
            texts = soup.findAll(text=True)
            visible_texts = filter(self.tag_visible, texts) 
            #items['contents']=u" ".join(t.strip() for t in visible_texts)
            items['contents']=page_text

            #items['contents_vt'] = u" ".join(t.strip() for t in visible_texts)
            with open("files/file_%s.txt"%self.count,"w+") as f:
                #f.write(str(items)+"\n")
                f.writelines(page_text)
            self.links_dict["file_%s.txt"%self.count]= items['origin_link'] 
            self.count+=1
            yield items

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