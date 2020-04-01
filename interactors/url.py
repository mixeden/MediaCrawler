import json
import os
import time

from interactors.chrome import ChromeInteractor


class UrlInteractor:
    def __init__(self, language, path):
        self.banned_urls = []
        self.viewed_urls = []
        self.new_urls = []
        self.path = path
        self.language = language
        self.chrome_handler = None

    def ban(self, url):
        print("Banned new url: {}".format(url))

        if self.is_new(url):
            self.new_urls.remove(url)

        self.banned_urls.append(url)
        self.save()

    def add_new(self, url):
        print("Added new url: {}".format(url))

        self.new_urls.append(url)
        self.save()

    def add(self, url):
        cleared_url = ChromeInteractor.clear_url(url)

        if not (self.is_viewed(cleared_url) or self.is_banned(cleared_url) or self.is_new(cleared_url)):
            print("Should we view https://{}?".format(url))
            result = input()

            if result == 'y' or result == 'yes' or result == 'да' or result == 'у':
                self.add_new(cleared_url)

            else:
                self.ban(cleared_url)

    def view(self, url):
        cleared_url = ChromeInteractor.clear_url(url)
        print("Viewed new url: {}".format(cleared_url))

        if self.is_new(url):
            self.new_urls.remove(url)

        self.viewed_urls.append(cleared_url)
        self.save()

    def add_from_table(self, url):
        cleared_url = ChromeInteractor.clear_url(url)

        if not self.is_not_viewable(cleared_url) and not self.is_new(url):
            self.add_new(cleared_url)

    @staticmethod
    def is_found(url, array):
        for link in array:
            if url in link or link in url:
                return True

        return False

    def is_viewed(self, url):
        return self.is_found(url, self.viewed_urls)

    def is_banned(self, url):
        return self.is_found(url, self.banned_urls)

    def is_new(self, url):
        return self.is_found(url, self.new_urls)

    def is_not_viewable(self, url):
        return self.is_viewed(url) or self.is_banned(url)

    @staticmethod
    def save_empty(file):
        file.write("[]")
        file.close()

    def load(self):
        if not os.path.isfile(self.get_banned_urls_file()):
            with open(self.get_banned_urls_file(), 'w+') as file:
                self.save_empty(file)
                self.banned_urls = []

        else:
            with open(self.get_banned_urls_file(), 'r') as file:
                self.banned_urls = json.load(file)

        print("Loaded {}".format(self.get_banned_urls_file()))

        if not os.path.isfile(self.get_viewed_urls_file()):
            with open(self.get_viewed_urls_file(), 'w+') as file:
                self.save_empty(file)
                self.viewed_urls = []

        else:
            with open(self.get_viewed_urls_file(), 'r') as file:
                self.viewed_urls = json.load(file)

        print("Loaded {}".format(self.get_viewed_urls_file()))

        if not os.path.isfile(self.get_new_urls_file()):
            with open(self.get_new_urls_file(), 'w+') as file:
                self.save_empty(file)
                self.new_urls = []

        else:
            with open(self.get_new_urls_file(), 'r') as file:
                self.new_urls = json.load(file)

        print("Loaded {}".format(self.get_new_urls_file()))

    def get_banned_urls_file(self):
        return "{}/data/{}/banned_urls.json".format(self.path, self.language)

    def get_new_urls_file(self):
        return "{}/data/{}/new_urls.json".format(self.path, self.language)

    def get_viewed_urls_file(self):
        return "{}/data/{}/viewed_urls.json".format(self.path, self.language)

    def save(self):
        with open(self.get_banned_urls_file(), 'w') as outfile:
            json.dump(self.banned_urls, outfile)

        with open(self.get_new_urls_file(), 'w') as outfile:
            json.dump(self.new_urls, outfile)

        with open(self.get_viewed_urls_file(), 'w') as outfile:
            json.dump(self.viewed_urls, outfile)

    def handle_truncations(self, truncations):
        for truncation in truncations:
            if "/siteinfo" in truncation["href"]:
                url = truncation.contents[0]
                self.add(url)

    def set_chrome_interactor(self, handler):
        self.chrome_handler = handler

    def start(self):
        while len(self.new_urls) > 0:
            time.sleep(3.4)

            print("There are {} urls in list".format(len(self.new_urls)))
            url = self.new_urls[0]

            if self.is_not_viewable(url):
                print("We skip {}".format(url))
                self.view(url)

            else:
                truncations = self.chrome_handler.handle(url)

                self.view(url)
                self.handle_truncations(truncations)
