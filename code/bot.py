from dotenv import load_dotenv

load_dotenv()
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    NoSuchElementException,
    UnexpectedAlertPresentException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time, os, pathlib
from bs4 import BeautifulSoup
from sys import platform

CODE_DIR = pathlib.Path().absolute()
LOCALHOST_DIR = os.path.join(CODE_DIR, "driver", "localhost")


def open_page(driver, wait, eid_username, eid_password):

    attempts = 0
    while attempts < 10:
        try:
            driver.get("https://guides.lib.utexas.edu/db/144")
            time.sleep(6)
            try:
                driver.find_element(By.XPATH, '//label[@for="email"]')
                #'Session expired, restarting...'
                time.sleep(3)
                attempts += 1
                continue
            except NoSuchElementException:
                pass
            h1 = driver.find_element(By.XPATH, "//h1")
            if h1.text.strip() == "Sign in with your UT EID":
                #'Session expired, restarting...'
                login(driver, wait, eid_username, eid_password)
                time.sleep(3)
                attempts += 1
                continue
            break
        except TimeoutException:
            pass
            time.sleep(3)
            attempts += 1


def enter_search(driver, wait, date_dict, search, ut_eid, eid_password):

    attempts = 0
    while attempts < 10:
        try:
            wait.until(
                EC.element_to_be_clickable((By.XPATH, '//select[@name="dr"]'))
            ).click()
            wait.until(
                EC.element_to_be_clickable((By.XPATH, '//option[@value="Custom"]'))
            ).click()
            driver.find_element(By.XPATH, '//select[@name="isrd"]').click()
            wait.until(
                EC.element_to_be_clickable((By.XPATH, '//option[@value="High"]'))
            ).click()
            search_box = driver.find_element(By.XPATH, '//textarea[@name="ftx"]')
            search_box.clear()
            search_box.send_keys(search)
            for id_, value in date_dict.items():
                driver.find_element(By.ID, id_).clear()
                driver.find_element(By.ID, id_).send_keys(value)
            try:
                driver.find_element(By.XPATH, '//div[@class="pillNoMenu"]').click()
            except NoSuchElementException:
                pass
            search_box.send_keys(Keys.ENTER)
            wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//span[@data-channel="Dowjones"]')
                )
            )
            time.sleep(5)
            break
        except (
            StaleElementReferenceException,
            ElementClickInterceptedException,
            UnexpectedAlertPresentException,
        ) as action_error:

            pass
            time.sleep(3)
            attempts += 1

        except TimeoutException as timeout_error:

            pass
            time.sleep(3)
            open_page(driver, wait, ut_eid, eid_password)
            attempts += 1


def next_page(driver, wait):

    attempts = 0
    while attempts < 10:
        try:
            wait.until(
                EC.visibility_of_element_located((By.XPATH, '//a[@class="nextItem"]'))
            ).click()
            wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//img[@src="../img/listmanager/progress.gif"]')
                )
            )
            wait.until(
                EC.invisibility_of_element_located(
                    (By.XPATH, '//img[@src="../img/listmanager/progress.gif"]')
                )
            )
            break
        except (
            StaleElementReferenceException,
            ElementClickInterceptedException,
            UnexpectedAlertPresentException,
        ):
            # "Click next failed"

            time.sleep(3)
            attempts += 1


def login(driver, wait, eid_username, eid_password):

    wait.until(EC.element_to_be_clickable((By.ID, "username")))
    driver.find_element(By.ID, "username").send_keys(eid_username)
    driver.find_element(By.XPATH, '//input[@id="password"]').send_keys(eid_password)
    driver.find_element(By.XPATH, "//input[@value='Sign in']").click()
    try:
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@id='trust-browser-button']")
            )
        ).click()
    except TimeoutException:

        pass
        # "Duo cookies still valid; proceeding to search page..."


def make_paths(driver_folder):

    if platform == "win32":
        driver_path = os.path.join(driver_folder, "chromedriver.exe")

    elif platform == "darwin":
        driver_path = os.path.join(driver_folder, "chromedriver")

    profile_path = os.path.join(driver_folder, "localhost")

    return driver_path, profile_path


def set_driver():

    DRIVER_DIR = os.path.join(CODE_DIR, "driver")
    LOCALHOST_DIR = os.path.join(DRIVER_DIR, "localhost")
    os.makedirs(DRIVER_DIR, exist_ok=True)
    os.makedirs(LOCALHOST_DIR, exist_ok=True)
    options = Options()
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument(f"--user-data-dir={LOCALHOST_DIR}")
    driver = webdriver.Chrome(
        executable_path=ChromeDriverManager(path=DRIVER_DIR).install(),
        chrome_options=options,
    )
    wait = WebDriverWait(driver, 10)
    driver.set_page_load_timeout(20)
    return driver, wait
