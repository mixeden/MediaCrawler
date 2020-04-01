from selenium import webdriver
from bs4 import BeautifulSoup

from constants import ALEXA_URL, DRIVER_PATH


class ChromeInteractor:
    def __init__(self, notion_handler):
        self.notion_handler = notion_handler

    @staticmethod
    def clear_url(url):
        return url.replace("https://", "").replace("http://", "").replace("www.", "")

    @staticmethod
    def remove_formatting(thing):
        return thing.replace(",", "").replace(" ", "").replace("\n", "").replace("\t", "")

    def handle(self, url):
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(DRIVER_PATH, options=chrome_options)

        final_url = ALEXA_URL + url
        print("Getting {} with driver".format(final_url))
        driver.get(final_url)
        driver.implicitly_wait(3000)

        html = driver.execute_script('return document.documentElement.outerHTML')
        soup = BeautifulSoup(html, 'html.parser')

        big_data = soup.find_all("p", {"class": "big data"})
        alexa_rate = int(self.remove_formatting(big_data[0].contents[2]))

        truncations = soup.find_all("a", {"class": "truncation"})
        driver.quit()

        cleared_url = ChromeInteractor.clear_url(url)
        self.notion_handler.add_row(cleared_url, alexa_rate)

        return truncations
