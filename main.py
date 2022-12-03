from calendar import c
from email import message
from itertools import count
from xml.dom.minidom import Document
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import random
import socket
import numpy as np

from selenium.common.exceptions import (
    ElementNotVisibleException,
    ElementClickInterceptedException,
    WebDriverException,
    TimeoutException,
)
import pyautogui
import pyperclip
import csv
import pandas as pd
from glob import glob
import os 
import random
import pickle
import re, itertools
# from lxml import etree
from selenium.webdriver.common.keys import Keys

def xpath_soup(element):
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name
            if siblings == [child] else
            '%s[%d]' % (child.name, 1 + siblings.index(child))
            )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--disable-notifications")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)  # version_main allows to specify your chrome version instead of following chrome global version
driver.maximize_window()
driver.get("https://www.pinterest.com/login/")
time.sleep(20)

choose = input("Enter \"y\" after logging in : ")

if choose == "y":
    driver.get("https://www.pinterest.com/idea-pin-builder/")
    
    html = driver.page_source
    soup = BeautifulSoup(html, features="html.parser")        
    
    create_story_btn = soup.find("div",attrs={"data-test-id":"storyboard-create-button"})
    
    while(True):
        html = driver.page_source
        soup = BeautifulSoup(html, features="html.parser")        
        
        create_story_btn = soup.find("div",attrs={"data-test-id":"storyboard-create-button"})
        
        if create_story_btn!=None:
            break
        time.sleep(1)
    

    
    images = glob(os.getcwd()+"\\bulk_post_pinterest"+"\\*")
    
    for i in range(len(images)):
        img = images[i]
        print("Posting image no. => "+str(i+1)+" out of "+str(len(images)))
        
        html = driver.page_source
        soup = BeautifulSoup(html, features="html.parser")        
        
        create_story_btn = soup.find("div",attrs={"data-test-id":"storyboard-create-button"})
        
        driver.find_element(By.XPATH, xpath_soup(create_story_btn)).click()
        
        time.sleep(5)
            
        driver.find_element(By.ID, "storyboard-upload-input").send_keys(img)

        while(True):
            html = driver.page_source
            soup = BeautifulSoup(html, features="html.parser")        
            
            create_story_btn = soup.find("div",attrs={"data-test-id":"storyboard-create-button"})
            
            if create_story_btn!=None:
                break
            time.sleep(1)


        time.sleep(5)
        
        while(True):
            html = driver.page_source
            soup = BeautifulSoup(html, features="html.parser")        
            
            story_edit = soup.find("div",attrs={"data-test-id":"storyboard-editor-details-media"})
            
            if story_edit!=None:
                break
            time.sleep(1)
        
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, features="html.parser")        
        
        story_next = soup.find("div",attrs={"data-test-id":"storyboard-creation-nav-done"})       
        
        driver.find_element(By.XPATH, xpath_soup(story_next)).click()
        
        time.sleep(5)
        
        html = driver.page_source
        soup = BeautifulSoup(html, features="html.parser")        
        
        story_next = soup.find("div",attrs={"data-test-id":"storyboard-creation-nav-done"})
        
        # driver.find_element(By.ID, "storyboard-selector-title").send_keys(post_title)
        driver.find_element(By.XPATH, xpath_soup(story_next)).click()      

        while(True):
            html = driver.page_source
            soup = BeautifulSoup(html, features="html.parser")        
            
            pin_stat_div = soup.find("div",attrs={"data-test-id":"pin-stats-module"})
            
            if pin_stat_div!=None:
                break
            time.sleep(1)        
        
        
        time.sleep(2)
        
        print("Done posting image no. => "+str(i+1)+" out of "+str(len(images)))
        if i == len(images)-1:
            print("================Finished================")
            
        if i != len(images)-1:
            driver.get("https://www.pinterest.com/idea-pin-builder/")
            time.sleep(10)
            
        
               
        
    