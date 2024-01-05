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
from profiles import Profile
import multiprocessing as mp
import threading as th

class Runner():
    '''This creates many profile objects, and let them run through the profiles.csv, while searching for emails. '''
    
    def __init__(self, n):
        self.n = n
        self.processes = []
        self.bots = []
        self.progress = []
        self.file = "profiles.csv"
        self.gmail_file = "emails.csv"
        self.all_profiles = pd.read_csv(self.file)["0"]

        #creates a ton of profile bots
        for i in range(self.n):
            p = th.Thread(target = self.create_profile, args = (len(self.all_profiles),i,))
            p.start()
            self.processes.append(p)
        
        for p in self.processes:
            p.join()

        self.update_file()
        self.collect_gmail()
        print("---------------------DONE---------------------")
    
           
    def create_profile(self, tot_len, j):
        '''makes a profile object, and sets it up'''

        #splits work between bots
        i = int(j * tot_len/self.n)
        portion = self.all_profiles[int(j * tot_len/self.n) : int((j+1) * tot_len/self.n)]

        #progress used to update profiles.csv
        self.progress.append(-1)

        #stuff
        new_profile = Profile(portion, i)
        self.bots.append(new_profile)
        self.progress[j] = new_profile.end_up + i

    def update_file(self):
        '''updates profiles.csv bc we already searched''' #TODO: something wrong here about indexes
        tot_len = len(self.all_profiles)
        for i in range(self.n):
            self.all_profiles = self.all_profiles.drop(labels = [j for j in range(int((i) * tot_len/self.n) , self.progress[i])], axis=0)
            #self.all_profiles = self.all_profiles.drop(labels = [i, i+10, i+20, 2], axis=0)
        self.all_profiles.to_csv(self.file, sep=",", index=False, encoding='utf-8')

    def collect_gmail(self):
        '''saving all the gmails, and putting it into emails.csv'''

        gmails = pd.read_csv(self.gmail_file)["Email"]
        for i in range(self.n):
            y = pd.Series(self.bots[i].email_list, dtype = "object")
            gmails = pd.concat([gmails, y])
        pd.DataFrame(data = {"Email": list(set([gmail.lower() for gmail in gmails]))} ).to_csv(self.gmail_file, sep=",", index=False, encoding='utf-8')

if __name__ == "__main__":
    Runner(14)