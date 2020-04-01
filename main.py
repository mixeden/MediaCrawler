import os

from interactors.chrome import ChromeInteractor
from interactors.notion import NotionInteractor
from interactors.url import UrlInteractor

path = os.path.dirname(os.path.abspath(__file__))

print("Insert language: ")
language = input()

url_handler = UrlInteractor(language, path)
url_handler.load()

notion_handler = NotionInteractor(language, url_handler)
notion_handler.load_table()

chrome_handler = ChromeInteractor(notion_handler)

url_handler.set_chrome_interactor(chrome_handler)
url_handler.start()
