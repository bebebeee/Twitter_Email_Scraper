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

#TODO: make email processing better
class Profile():
    '''Searches through given links to find emails. Is used in PART2.py'''

    def __init__(self, profiles, i):
        self.driver = webdriver.Chrome()
        self.profiles = profiles
        self.email_list = []
        self.i = i
        self.end_up = -2
        self.errored = False
        self.email_endings = ["@gmail.com", "@yahoo.com","@hotmail.com","@aol.com","@icloud.com"]
        time.sleep(1)
        
        #loop through all the profile links, and get the email inside
        for i in range(len(self.profiles)):
            try:
                profile = self.profiles[i+self.i]
                self.go_to(profile)
            except:
                print("excepted")
                self.end_up = i
                self.errored = True
                break
        
        if not self.errored:
            self.end_up = len(self.profiles)
        print("--------------------BYE----------------------")


    def go_to(self, profile):
        self.driver.get(profile)
        try:
            WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '" + profile[20:] +"')]")))

            #this part for searching the email ending in the page
            for ending in self.email_endings:
                if ending in self.driver.page_source:
                    for element in self.driver.find_elements(By.XPATH, "//*[contains(text(), '"+ending+"')]"):
                        gmail_texts = [i for i in element.text.split(" ") if ending in i]
                        for gmail_text in gmail_texts:
                            #getting actually gmail part from the gmail
                            ind_ending = gmail_text.index(ending)
                            i = 1
                            while (i <= ind_ending):
                                if gmail_text[ind_ending-i].isalnum():
                                    pass
                                elif gmail_text[ind_ending-i] in "&'*+-./=?^_{~}!$%":
                                    pass
                                else:
                                    break
                                i += 1
                            if i == 1:
                                continue
                            else:
                                self.email_list.append(gmail_text[ind_ending-i+1:ind_ending+len(ending)])
                                print("Found gmail: " + gmail_text)

        except:
            #If we get blocked
            if "Something went wrong. Try reloading." in self.driver.page_source: 
                print("oh noe")
                self.new_session()
                time.sleep(1)

    def save_exit(self, i):
        print("saving before quitting")
        return(i)

    def new_session(self):
        self.driver.quit()
        time.sleep(0.5)
        self.driver = webdriver.Chrome()






#Profile()