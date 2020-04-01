from notion.client import NotionClient

from constants import TABLES, TOKEN


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
            print("Currently adding {} from Notion".format(url))

            self.urls.append(url)
            self.url_handler.add_from_table(url)

    def add_row(self, url, alexa_rank):
        if url not in self.urls:
            row = self.database.collection.add_row()

            if "http" not in url:
                row.link = "https://" + url

            else:
                row.link = url

            row.alexa = alexa_rank
            row.name = url
            row.wrote = "No"
