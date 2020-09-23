from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time 
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import os 
from glob import glob 

from database_agent import URLTable
from hashlib import md5
import pickle
from tqdm import tqdm 
import config

def run_thread(num_worker, func, **argv):
    # now return 
    executor = ThreadPoolExecutor(max_workers=num_worker)
    executor.submit(func, **argv)
    executor.shutdown(wait=False) 

class Page():
    def __init__(self, hide=True):
        self.driver =self.get_driver(hide)
        self.save_dir = self.get_data_dir()
        
        self.cols = ["url", "url_guid", "url_len", 
                    "title_len", "save_pth", "status"]

    def get_driver(self, hide=True):
        # Define Browser Options
        chrome_options = Options()
        
        if hide:
            chrome_options.add_argument("--headless") # Hides the browser window
        driver = webdriver.Chrome(
            executable_path = self.get_driver_pth() , 
            options=chrome_options)
        return driver

    def get_driver_pth(self):
        res = []
        tries = 0 
        temp = '../'
        while not res and tries < 3:
            res.extend([i for i in glob('**/*.exe', recursive=True)
                        if 'chromedriver' in i ])
            temp = '../' + temp 
            tries +=1 
        return res[0]

    def get_data_dir(self):
        res = []
        tries = 0 
        temp = '../'
        while not res and tries < 3:
            res.extend([i for i in glob('**/', recursive=True)
                        if 'web_data' in i ])
            temp = '../' + temp 
            tries +=1 
        return os.path.dirname(res[0])

class PageDBAStackExchange(Page):
    def __init__(self):
        super().__init__()

    def run(self):

        for i in range(36, 1000):
            url = f'https://dba.stackexchange.com/questions?tab=newest&page={i}'
            self.driver.get(url)
            # print(f'[*] get_data {i}')
            data = self.driver.page_source
            run_thread(1, self._parsing, data=data, i=i)
            # ethetic web crawing
            time.sleep(0.5)

    def _parsing(self, data, i):
        # excerpt
        soup = BeautifulSoup(data)
        docs = soup.find_all('div', class_='excerpt')
        title_links = soup.select("a[class=question-hyperlink]")
        # ---------------------------------------
        docs = [i.text for i in docs]
        titles = [i.text for i in title_links]
        title_links = [i.get('href') for i in title_links]
        for i in [titles, title_links, docs]:
            print(len(i))


class PageStackoverflowQuestion(Page):
    'https://stackoverflow.com/questions?tab=Votes'

    def __init__(self, ):
        super().__init__()

    def run(self):
        for i in tqdm(range(0, 100000)):
            url = f'https://stackoverflow.com/questions?tab=votes&page={i}&pagesize=50'
            self.driver.get(url)
            data = self.driver.page_source
            #self._parsing(data=data, i=i, save_dir=self.save_dir)
            run_thread(1, self._parsing, data=data, i=i, save_dir=self.save_dir)
            time.sleep(0.3)

    def _parsing(self, data, i, save_dir):
        # excerpt
        # db
        
        soup = BeautifulSoup(data)
        docs = soup.find_all('div', class_='excerpt')
        title_links = soup.select("a[class=question-hyperlink]")

        docs = [i.text for i in docs]
        titles = [i.text for i in title_links]
        docs = [i+' '+j for i, j in zip(titles, docs)]

        urls = ['https://stackoverflow.com'+i.get('href') for i in title_links]

        if not len(title_links) == len(docs):
            raise ValueError('len of docs not mathch')

        # -------------------------------------
        title_len = [len(i) for i in titles]
        urls_len = [len(i) for i in urls]
        url_guids = [md5(str.encode(i)).hexdigest() for i in urls]
        
        status = [0 for _ in range(len(title_len))]

        save_pth = [os.path.join(save_dir, str(i)+'.pkl') 
                    for i in url_guids]

        # if init outside, would have DB lock
        db_agent = URLTable(config.forward_database)

        for i in range(len(urls)):
            pickle.dump( docs[i], open( save_pth[i], "wb" ))

            db_agent.insert_record(
                    url= urls[i], 
                    url_guid=url_guids[i], 
                    url_len=urls_len[i], 
                    title_len=title_len[i], 
                    save_pth=save_pth[i],
                    status = status[i],
                )


if __name__ == "__main__":
    ag = PageStackoverflowQuestion()
    ag.run()

    # driver = get_driver
    # driver.get("https://dba.stackexchange.com/questions")
    # https://dba.stackexchange.com/questions?tab=newest&page=6