from bs4 import BeautifulSoup
from lxml import etree
import httpx
from typing import Iterable, Dict
import time


class SitemapIngestionPipeline:

    def __init__(
        self,
        sitemap_url: str,
        xpath: str,
        headers: dict = {},
        crawl_interval_seconds: int = 1,
    ):
        
        self._sitemap_url = sitemap_url
        self._xpath = xpath
        self._headers = headers
        self._crawl_interval_seconds = crawl_interval_seconds


    def _get_url_list(self) -> Iterable[str]:

        response = httpx.get(
            url = self._sitemap_url,
            headers = self._headers
        )

        soup = BeautifulSoup(response.text, "lxml")
        url_tags = soup.find_all("url")
        url_list = [url.loc.text for url in url_tags]

        return url_list


    def _crawl_url_list(
        self,
        url_list: Iterable[str],
        start: int,
        end: int
    ) -> Iterable[Dict]:

        dict_pages = {}
        for url in url_list[start:end]:

            response = httpx.get(
                url = url,
                headers = self._headers
            )

            soup = BeautifulSoup(response.text, "html.parser")
            tree = etree.HTML(str(soup))
            parsed_text = tree.xpath(self._xpath)
            if parsed_text:
                parsed_text = " ".join(parsed_text).strip()
                dict_pages[url] = parsed_text

            time.sleep(self._crawl_interval_seconds)

        return dict_pages


    def __call__(
        self,
        start: int = 0,
        end: int = 100
    ):
        
        url_list = self._get_url_list()
        result = self._crawl_url_list(
            url_list = url_list,
            start = start,
            end = end
        )

        return result