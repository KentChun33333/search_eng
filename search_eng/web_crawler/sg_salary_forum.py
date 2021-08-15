from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

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

# what is the feasible data model 

class Page():
    def __init__(self, hide=0):
        self.driver =self.get_driver(hide)
        self.save_dir = self.get_data_dir()
        
        self.cols = ["url", "url_guid", "url_len", 
                    "title_len", "save_pth", "status"]

    def get_driver(self, hide):
        # Define Browser Options
        chrome_options = Options()
        
        if hide:
            chrome_options.add_argument("--headless") # Hides the browser window
        
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

        # driver = webdriver.Chrome(
            # executable_path = self.get_driver_pth() , 
            # options=chrome_options)
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

class SGSalaryForum(Page):
    def __init__(self):
        super().__init__()

    def run(self):
        # how to auto pattern
        res_all = []
        # how to auto pattern ->  
        # https://forums.salary.sg/{sub_forum}/{post-id-naming}-{page}.html#.YRkI3Ygzamc
        for i in range(1, 51):
            url = f"https://forums.salary.sg/income-jobs/10418-factual-local"+ \
                   "-bank-salaries-dbs-united-overseas-bank-oversea-chinese-bank"+\
                   "ing-corporation-commoner-climbing-up-ranks-{i}.html#.YRkI3Ygzamc"
            self.driver.get(url)
            # print(f'[*] get_data {i}')
            data = self.driver.page_source
            # parse 
            soup = BeautifulSoup(data)
            res = soup.find_all("div", {"class": "post_message"})
            res = [i.text for i in res]
            res_all.extend(res)
            time.sleep(0.2)
        
        with open('resut.txt', 'w') as f:
            f.writelines(res_all)
            # --------------------------------------------
            # run_thread(1, self._parsing, data=data, i=i)
            # # ethetic web crawing
            # time.sleep(0.5)


if __name__ == "__main__":
    ag = SGSalaryForum()
    ag.run()

    # driver = get_driver
    # driver.get("https://dba.stackexchange.com/questions")
    # https://dba.stackexchange.com/questions?tab=newest&page=6