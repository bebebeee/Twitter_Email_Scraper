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


class Account():
    '''This is a sign in and sign out of twitter robot. We put 4 accounts in. Used in PART1.py'''

    def __init__(self, driver, i):
        self.which_account = i%4
        self.driver = driver
        self.set_credentials()
        self.login()

    def set_credentials(self):
        '''set credentials to be used when logging in. '''

        if self.which_account == 0:
            self.email = "[enter your email]"
            self.username = "[enter full twitter username]"
            self.passw = "[enter password]"
        elif self.which_account == 1:
            self.email = "[enter your email]"
            self.username = "[enter full twitter username]"
            self.passw = "[enter password]"
        elif self.which_account == 2:
            self.email = "[enter your email]"
            self.username = "[enter full twitter username]"
            self.passw = "[enter password]"
        else:
            self.email = "[enter your email]"
            self.username = "[enter full twitter username]"
            self.passw = "[enter password]"
        

    def login(self):
        '''logs in'''

        self.driver.get("https://twitter.com/")
        time.sleep(1)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[5]/a"))).click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input"))).send_keys(self.email)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]"))).click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input"))).send_keys(self.username)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div"))).click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input"))).send_keys(self.passw)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div"))).click()

    def switch_account(self): 
        '''typically used when account gets blocked'''

        print("Switching Accounts...")
        self.driver.get("https://twitter.com/logout")
        time.sleep(0.25)
        try:
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid = 'confirmationSheetConfirm']"))).click()
        except:
            pass
        self.which_account = (self.which_account+1)%4
        self.set_credentials() #just change it
        time.sleep(0.05)
        self.login()