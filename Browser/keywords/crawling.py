from typing import List, Optional, Set

from robotlibcore import keyword  # type: ignore

from Browser.base import LibraryComponent

from ..utils import logger


class Crawling(LibraryComponent):
    @keyword(tags=["Crawling"])
    def crawl_site(self, url: Optional[str] = None):
        """
        Take screenshots from all urls inside a specific site.
        """
        if url:
            self.library.new_page(url)
        self._crawl(self.library.get_url() or "")

    def _crawl(self, baseurl: str):
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
                f"{len(crawled) + 1} / {len(crawled) + len(hrefs_to_crawl)} : Crawling url {href}"
            )
            self.library.go_to(href)
            self.library.take_screenshot()
            crawled.add(href)
            links = self.library.get_elements("//a[@href]")
            child_hrefs = [self.library.get_attribute(link, "href") for link in links]
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
            if href.startswith("/"):
                href = baseurl + href[1:]
            if href in old_hrefs_to_crawl:
                continue
            if href in crawled:
                continue
            if not href.startswith(baseurl):
                continue
            new_hrefs.append(href)
        return new_hrefs + old_hrefs_to_crawl
