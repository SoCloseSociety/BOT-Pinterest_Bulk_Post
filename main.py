from selenium import webdriver
import os
import time
from glob import glob

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
# from lxml import etree
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import ui
from webdriver_manager.chrome import ChromeDriverManager


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

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=options)  # version_main allows to specify your chrome version instead of following chrome global version
driver.maximize_window()
driver.get("https://www.pinterest.com/login/")
time.sleep(20)

title = input("Enter title : ")
description = input("Enter description : ")
link = input("Enter link : ")

choose = input("Enter \"y\" after logging in : ")

if choose == "y":
    driver.get("https://www.pinterest.com/pin-builder/")

    selected_element = None

    while (True):
        html = driver.page_source
        soup = BeautifulSoup(html, features="html.parser")

        selected_element = soup.find("input", attrs={"aria-label": "File upload"})

        if selected_element is not None:
            break
        time.sleep(1)

    time.sleep(5)
    images = glob(os.getcwd() + "\\bulk_post_pinterest" + "\\*")

    for i in range(len(images)):
        img = images[i]
        print("Posting image no. => " + str(i + 1) + " out of " + str(len(images)))

        html = driver.page_source
        soup = BeautifulSoup(html, features="html.parser")

        drag_drop_div = soup.find("input", attrs={"aria-label": "File upload"})

        driver.find_element(By.XPATH, xpath_soup(drag_drop_div)).send_keys(img)


        #Title
        element = driver.find_element(By.XPATH, "//textarea[contains(@id,'pin-draft-title')]")
        driver.execute_script("arguments[0].scrollIntoView()", element)
        time.sleep(1)
        driver.find_element(By.XPATH, "//textarea[contains(@id,'pin-draft-title')]").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "//textarea[contains(@id,'pin-draft-title')]").send_keys(title)

        #Description
        element = driver.find_element(By.XPATH, "//div[contains(@id,'pin-draft-description')]")
        driver.execute_script("arguments[0].scrollIntoView()", element)
        time.sleep(1)
        driver.find_element(By.XPATH, "//div[contains(@id,'pin-draft-description')]").click()
        time.sleep(4)
        inpt1 = ui.WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,  "//div[contains(@id,'pin-draft-description')]")))

        ActionChains(driver).move_to_element(inpt1).send_keys(description).perform()

        #driver.find_element(By.XPATH, "//div[contains(@id,'pin-draft-description')]").send_keys(description)

        #Link
        element = driver.find_element(By.XPATH, "//textarea[contains(@id,'pin-draft-link')]")
        driver.execute_script("arguments[0].scrollIntoView()", element)

        time.sleep(1)
        driver.find_element(By.XPATH, "//textarea[contains(@id,'pin-draft-link')]").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "//textarea[contains(@id,'pin-draft-link')]").send_keys(link)

        #Board select
        select_board_dropdown = soup.find("button", attrs={"data-test-id": "board-dropdown-select-button"})

        element = driver.find_element(By.XPATH, xpath_soup(select_board_dropdown))
        driver.execute_script("arguments[0].scrollIntoView()", element)
        time.sleep(1)

        driver.find_element(By.XPATH, xpath_soup(select_board_dropdown)).click()

        time.sleep(2)
        driver.find_element(By.ID, "pickerSearchField").send_keys("Coupons")
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, features="html.parser")
        first_item_in_list = soup.find("div", attrs={"data-test-id": "boardWithoutSection"})
        driver.find_element(By.XPATH, xpath_soup(first_item_in_list)).click()
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, features="html.parser")
        save_button = soup.find("button", attrs={"data-test-id": "board-dropdown-save-button"})
        driver.find_element(By.XPATH, xpath_soup(save_button)).click()

        time.sleep(5)
        loading_image = None
        #Post
        while (True):
            html = driver.page_source
            soup = BeautifulSoup(html, features="html.parser")

            loading_image = soup.find("svg",attrs={"role":"img","aria-label":"Saving Pin..."})

            if loading_image == None:
                break
            time.sleep(2)

        time.sleep(2)

        print("Done posting image no. => " + str(i + 1) + " out of " + str(len(images)))
        if i == len(images) - 1:
            print("================Finished================")

        if i != len(images) - 1:
            driver.get("https://www.pinterest.com/pin-builder/")
            time.sleep(2)



        # while (True):
        #     html = driver.page_source
        #     soup = BeautifulSoup(html, features="html.parser")
        #
        #     create_story_btn = soup.find("div", attrs={"data-test-id": "storyboard-create-button"})
        #
        #     if create_story_btn != None:
        #         break
        #     time.sleep(1)
        #
        # time.sleep(5)
        #
        # while (True):
        #     html = driver.page_source
        #     soup = BeautifulSoup(html, features="html.parser")
        #
        #     story_edit = soup.find("div", attrs={"data-test-id": "storyboard-editor-details-media"})
        #
        #     if story_edit != None:
        #         break
        #     time.sleep(1)
        #
        # time.sleep(5)
        # html = driver.page_source
        # soup = BeautifulSoup(html, features="html.parser")
        #
        # story_next = soup.find("div", attrs={"data-test-id": "storyboard-creation-nav-done"})
        #
        # driver.find_element(By.XPATH, xpath_soup(story_next)).click()
        #
        # time.sleep(5)
        #
        # html = driver.page_source
        # soup = BeautifulSoup(html, features="html.parser")
        #
        # story_next = soup.find("div", attrs={"data-test-id": "storyboard-creation-nav-done"})
        #
        # # driver.find_element(By.ID, "storyboard-selector-title").send_keys(post_title)
        # driver.find_element(By.XPATH, xpath_soup(story_next)).click()
        #
        # while (True):
        #     html = driver.page_source
        #     soup = BeautifulSoup(html, features="html.parser")
        #
        #     pin_stat_div = soup.find("div", attrs={"data-test-id": "pin-stats-module"})
        #
        #     if pin_stat_div != None:
        #         break
        #     time.sleep(1)
        #
        # time.sleep(2)
        #
        # print("Done posting image no. => " + str(i + 1) + " out of " + str(len(images)))
        # if i == len(images) - 1:
        #     print("================Finished================")
        #
        # if i != len(images) - 1:
        #     driver.get("https://www.pinterest.com/idea-pin-builder/")
        #     time.sleep(10)
        #
        #
