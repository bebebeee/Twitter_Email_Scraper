from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
from pro_link import Twitter
import multiprocessing as mp
import threading as th

class Gather():
    '''Has many pro_link Twitter bots to help scrape faster. Used in DONE. Specify number of bots. 
    4=quickly need a lot, but only like 10,000 (because the accounts get temparally banned faster). 
    3=medium speed, larger quanitity. 
    2=lower speed, even larger quanitity. 
    1=slowest, and largest'''
    
    def __init__(self, n):
        self.n = n
        self.file = "profiles.csv"
        self.bots = []
        self.prof_links = pd.read_csv(self.file)["0"].tolist()
        
        threads = []
        for i in range(self.n):
            t = th.Thread(target = self.make_bot, args = (i,))
            threads.append(t)
            t.start()

        t = th.Thread(target = self.number_collected, args = ())
        threads.append(t)
        t.start()

        for t in threads:
            t.join()

        pd.Series(list(set(self.prof_links))).to_csv(self.file, sep=",", index=False, encoding='utf-8')
        

    def make_bot(self, i):
        b = Twitter(i)
        self.bots.append(b)
        b.primary_search()
        b.secondary_search()
        self.prof_links = self.prof_links + b.save_exit()
        self.bots.remove(b)

    def number_collected(self):
        time.sleep(12)
        while len(self.bots) != 0:
            time.sleep(5)
            n = len(self.prof_links)
            for bot in self.bots:
                n += len(bot.profiles)
            print("Length of profiles is " + str(n))
            

if __name__ == "__main__":
    Gather(4)



        