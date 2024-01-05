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
from acc import Account
#TODO: to get more accounts, can click the 'show more replies' button
#TODO: put secondary search inside a method, so that when we call it in PAR1, we can find total
class Twitter():
    '''Collects twitter user links, and puts them in profiles.csv. Uses acc.py'''

    def __init__(self, i):
        self.driver = webdriver.Chrome()
        self.links = []
        self.link_on = "https://twitter.com/" 
        self.profiles = []
        self.account = Account(self.driver, i)
        self.keep_searching = True

        time.sleep(5)
        #primary search -- to get links and profiles

        #secondary search -- go through each of the links, and get all the profiles on that page
        

    def primary_search(self):
        while True:
            try:
                stop = self.search_page(True)
                if stop:
                    break
            except:
                return None

    def secondary_search(self):
        for i in range(len(self.links)):
            self.link_on = self.links[i]
            print("Zooming in on " + str(i+1) + "/" + str(len(self.links)) + " link: " + self.link_on)
            self.driver.get(self.link_on)
            while True:
                try:
                    stop = self.search_page(False)
                    if stop:
                        break
                except:
                    return None


    def search_page(self, get_links):
        stop = self.view_tweets(get_links)
        #if get_links:
        #    print("Length of links: " + str(len(self.links)))
        #print("Length of profiles: " + str(len(self.profiles)))
        if (stop):
            return True
        return False

    def view_tweets(self,getting_more_links):
        #loop through loaded tweets
            #get profile
            #save to pandas
        #scroll down
            #check if at end page
        time.sleep(2)
        all_tweets = self.driver.find_elements(By.XPATH, "//div[@data-testid='cellInnerDiv']")
        if len(all_tweets) == 0:
            print("Need to switch accounts...")
            self.account.switch_account()

        for tweet in all_tweets:
            try:
                profile_link = self.get_profile(tweet)
                self.profiles.append(profile_link)
            except:
                pass
            if getting_more_links:
                try:
                    tweet_link = self.get_tweet(tweet)
                    self.links.append(tweet_link)
                except:
                    pass

        end_of_page = self.scroll_down()
        return end_of_page

    def get_profile(self, tweet):
        link = tweet.find_element(By.XPATH, ".//a")
        return link.get_attribute('href')

    def scroll_down(self):
        prev = self.driver.execute_script('return document.body.scrollHeight')
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(2)
        curr = self.driver.execute_script('return document.body.scrollHeight')
        if (prev == curr):
            return True
        return False

    def get_tweet(self, tweet):
        #"//div[@data-testid='cellInnerDiv']//article//a//time//.." for the links
        tweet_link = tweet.find_element(By.XPATH, ".//article//a//time//..")
        return tweet_link.get_attribute("href")

    def save_exit(self):
        print("---------------------BYE from PART1---------------------")  
        return self.profiles
        
