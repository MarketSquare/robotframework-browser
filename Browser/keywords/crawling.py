from typing import List, Optional, Set

from robot.libraries.BuiltIn import BuiltIn  # type: ignore
from robotlibcore import keyword  # type: ignore

from Browser.base import LibraryComponent

from ..utils import logger


class Crawling(LibraryComponent):
    @keyword(tags=["Crawling"])
    def crawl_site(
        self, url: Optional[str] = None, page_crawl_keyword="basic_page_crawl"
    ):
        """
        Take screenshots from all urls inside a specific site.
        """
        if url:
            self.library.new_page(url)
        self._crawl(self.library.get_url() or "", page_crawl_keyword)

    @keyword(tags=["Crawling"])
    def basic_page_crawl(self):
        self.library.take_screenshot()
        link_elements = self.library.get_elements("//a[@href]")
        links = set()
        for link_element in link_elements:
            links.add(self.library.execute_javascript("(e) => e.href", link_element))
        return list(links)

    def _crawl(self, baseurl: str, page_crawl_keyword: str):
        hrefs_to_crawl = [baseurl]
        crawled: Set[str] = set()
        while hrefs_to_crawl:
            href = hrefs_to_crawl.pop()
            if href.startswith("/"):
                href = baseurl + href[1:]
            if href.endswith(".zip"):
                logger.console("zip file detected ignoring")
                continue
            if not href.startswith(baseurl):
                continue
            if href in crawled:
                continue
            logger.info(f"Crawling url {href}")
            logger.console(
                f"{len(crawled) + 1} / {len(crawled) + 1 + len(hrefs_to_crawl)} : Crawling url {href}"
            )
            self.library.go_to(href)
            child_hrefs = BuiltIn().run_keyword(page_crawl_keyword)
            crawled.add(href)
            hrefs_to_crawl = self._build_urls_to_crawl(
                child_hrefs, hrefs_to_crawl, crawled, baseurl
            )

    def _build_urls_to_crawl(
        self,
        new_hrefs_to_crawl: List[str],
        old_hrefs_to_crawl: List[str],
        crawled: Set[str],
        baseurl: str,
    ) -> List[str]:
        new_hrefs = []
        for href in new_hrefs_to_crawl:
            if href in old_hrefs_to_crawl:
                continue
            if href in crawled:
                continue
            if not href.startswith(baseurl):
                continue
            new_hrefs.append(href)
        return new_hrefs + old_hrefs_to_crawl
