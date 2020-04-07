from notion.client import NotionClient
from urllib.parse import urlparse

from constants import TABLES, TOKEN
from interactors.chrome import ChromeInteractor


class NotionInteractor:
    def __init__(self, language, url_handler):
        self.urls = []
        self.language = language
        self.url_handler = url_handler
        self.client = NotionClient(token_v2=TOKEN)

        table = TABLES[self.language]
        self.database = self.client.get_collection_view(table)

    def load_table(self):
        current_rows = self.database.default_query().execute()

        for row in current_rows:
            url = row.link

            parsed_uri = urlparse(url)
            result = ChromeInteractor.clear_url('{uri.netloc}/'.format(uri=parsed_uri))

            print("Currently adding {} from Notion".format(result))

            self.urls.append(result)
            self.url_handler.add_from_table(result)

    def find_row(self, url):
        current_rows = self.database.default_query().execute()
        index = self.urls.index(url)
        return current_rows[index]

    def add_row(self, url, alexa_rank):
        print("Searching for {} in {}".format(url, self.urls))

        if url not in self.urls:
            row = self.database.collection.add_row()

            if "http" not in url:
                row.link = "https://" + url

            else:
                row.link = url

            row.alexa = alexa_rank
            row.name = url
            row.wrote = "Нет"

        else:
            row = self.find_row(url)
            row.alexa = alexa_rank
