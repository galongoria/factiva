from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException, 
    StaleElementReferenceException,
    ElementClickInterceptedException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time



def enter_search(driver, wait, dates, year, search):
    
    attempts = 0
    while attempts < 5:
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//select[@name="dr"]'))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH, '//option[@value="Custom"]'))).click()
            driver.find_element(By.ID, 'frm').clear()
            driver.find_element(By.ID, 'frm').send_keys('01')
            driver.find_element(By.ID, 'frd').clear()
            driver.find_element(By.ID, 'frd').send_keys('01')
            driver.find_element(By.ID, 'fry').clear()
            driver.find_element(By.ID, 'fry').send_keys(year)
            driver.find_element(By.ID, 'tom').clear()
            driver.find_element(By.ID, 'tom').send_keys(dates[0])
            driver.find_element(By.ID, 'tod').clear()
            driver.find_element(By.ID, 'tod').send_keys(dates[1])
            driver.find_element(By.ID, 'toy').clear()
            driver.find_element(By.ID, 'toy').send_keys(year)
            driver.find_element(By.XPATH, '//select[@name="isrd"]').click()
            wait.until(EC.element_to_be_clickable((By.XPATH, '//option[@value="High"]'))).click()
            search_box = driver.find_element(By.XPATH, '//textarea[@name="ftx"]')
            search_box.clear()
            search_box.send_keys(search)
            try:
                driver.find_element(By.XPATH, '//div[@class="pillNoMenu"]').click()
            except NoSuchElementException:
                pass
            search_box.send_keys(Keys.ENTER)
            wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@data-channel="Dowjones"]')))
            time.sleep(5)
            break
        except UnexpectedAlertPresentException:
            attempts += 1



def next_loop(driver, wait):
    
    attempts = 0
    while attempts < 5:
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@class="nextItem"]'))).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, '//img[@src="../img/listmanager/progress.gif"]')))
            wait.until(EC.invisibility_of_element_located((By.XPATH, '//img[@src="../img/listmanager/progress.gif"]')))
            break
        except (StaleElementReferenceException, ElementClickInterceptedException):
            attempts += 1




def modify_search_loop(driver, wait):
    
    attempts = 0
    while attempts < 5:
        try:
            wait.until(EC.element_to_be_clickable((By.ID, 'btnModifySearch'))).click()
            break
        except (StaleElementReferenceException, ElementClickInterceptedException):
            attemps += 1


def login(driver, wait, eid_username, eid_password):

    wait.until(EC.element_to_be_clickable((By.ID, 'username')))
    driver.find_element(By.ID, 'username').send_keys(eid_username)
    driver.find_element(By.XPATH, '//input[@id="password"]').send_keys(eid_password)    
    driver.find_element(By.XPATH, "//input[@value='Sign in']").click()
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='trust-browser-button']"))).click()
        
    except TimeoutException:
        print('Duo cookies still valid; proceeding to search page...')


def set_driver(path):

    
    option = webdriver.ChromeOptions()
    option.add_experimental_option("debuggerAddress", "localhost:9222")
    driver = webdriver.Chrome(executable_path = path ,options=option)
    wait = WebDriverWait(driver, 10)
    driver.set_page_load_timeout(20)

    return driver, wait


def get_page(driver, url):

    driver.get(url)

