import copy
import threading

import requests


class SimpleCrawler(object):
    _results = {}

    @staticmethod
    def fetch_url(url):
        """
        Crawls the html content of the parameter url and returns the html
        :param url:
        :return:
        """
        return SimpleCrawler._fetch_url(url, False)

    @staticmethod
    def _fetch_url(url, is_threaded):
        """
        Crawls the html content of the parameter url and saves the html in _results
        :param url:
        :param is_threaded: If True, results will be stored for later processing by the fetch_urls method. Else not.
        :return: html of the url
        """
        req = requests.get(url)
        req.encoding = 'utf-8'
        html = req.text

        if is_threaded:
            SimpleCrawler._results[url] = html

        return html

    @staticmethod
    def fetch_urls(urls):
        """
        Crawls the html content of all given urls in parallel. Returns when all requests are processed.
        :param urls:
        :return:
        """
        threads = [threading.Thread(target=SimpleCrawler._fetch_url, args=(url, True,)) for url in urls]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        results = copy.deepcopy(SimpleCrawler._results)
        SimpleCrawler._results = {}
        return results
