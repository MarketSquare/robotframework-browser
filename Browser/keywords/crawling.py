import urllib.parse
from typing import Optional

from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn

from Browser.base import LibraryComponent

from ..utils import logger


class Crawling(LibraryComponent):
    @keyword(tags=["Crawling"])
    def crawl_site(
        self,
        url: Optional[str] = None,
        page_crawl_keyword="take_screenshot",
        max_number_of_page_to_crawl: int = 1000,
        max_depth_to_crawl: int = 50,
    ):
        """
        Web crawler is a tool to go through all the pages on a specific URL domain.
        This happens by finding all links going to the same site and opening those.

        returns list of crawled urls.

        | =Arguments= | =Description= |
        | ``url`` | is the page to start crawling from. |
        | ``page_crawl_keyword`` | is the keyword that will be executed on every page.  By default it will take a screenshot on every page. |
        | ``max_number_of_page_to_crawl`` | is the upper limit of pages to crawl. Crawling will stop if the number of crawled pages goes over this. |
        | ``max_depth_to_crawl`` | is the upper limit of consecutive links followed from the start page. Crawling will stop if there are no more links under this depth. |

        [https://forum.robotframework.org/t//4243|Comment >>]
        """
        if url:
            self.library.new_page(url)
        return list(
            self._crawl(
                self.library.get_url() or "",
                page_crawl_keyword,
                max_number_of_page_to_crawl,
                max_depth_to_crawl,
            )
        )

    def _crawl(
        self,
        start_url: str,
        page_crawl_keyword: str,
        max_number_of_page_to_crawl: int,
        max_depth_to_crawl: int,
    ):
        hrefs_to_crawl: list[tuple[str, int]] = [(start_url, 0)]
        url_parts = urllib.parse.urlparse(start_url)
        baseurl = url_parts.scheme + "://" + url_parts.netloc
        crawled: set[str] = set()
        while hrefs_to_crawl and len(crawled) < max_number_of_page_to_crawl:
            href, depth = hrefs_to_crawl.pop()
            if not href.startswith(baseurl):
                continue
            if href in crawled:
                continue
            logger.info(f"Crawling url {href}")
            logger.console(
                f"{len(crawled) + 1} / {len(crawled) + 1 + len(hrefs_to_crawl)} : Crawling url {href}"
            )
            try:
                self.library.go_to(href)
            except Exception as e:
                logger.warn(f"Exception while crawling {href}: {e}")
                continue
            BuiltIn().run_keyword(page_crawl_keyword)
            child_hrefs = self._gather_links(depth)
            crawled.add(href)
            hrefs_to_crawl = self._build_urls_to_crawl(
                child_hrefs, hrefs_to_crawl, crawled, baseurl, max_depth_to_crawl
            )
        return crawled

    def _gather_links(self, parent_depth: int) -> list[tuple[str, int]]:
        link_elements = self.library.get_elements("//a[@href]")
        links: set[str] = set()
        depth = parent_depth + 1
        for link_element in link_elements:
            href, normal_link = self.library.evaluate_javascript(
                link_element, "(e) => [e.href, !e.download]"
            )
            if normal_link:
                links.add(href)
        return [(c, depth) for c in links]

    def _build_urls_to_crawl(
        self,
        new_hrefs_to_crawl: list[tuple[str, int]],
        old_hrefs_to_crawl: list[tuple[str, int]],
        crawled: set[str],
        baseurl: str,
        max_depth: int,
    ) -> list[tuple[str, int]]:
        new_hrefs = []
        for href, depth in new_hrefs_to_crawl:
            if depth > max_depth:
                continue
            if href in [h[0] for h in old_hrefs_to_crawl]:
                continue
            if href in crawled:
                continue
            if not href.startswith(baseurl):
                continue
            logger.debug(f"Adding link to {href}")
            new_hrefs.append((href, depth))
        return new_hrefs + old_hrefs_to_crawl
