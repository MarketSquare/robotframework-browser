from typing import Union

from robotlibcore import keyword  # type: ignore

from ..base import LibraryComponent
from ..utils import is_falsy, logger


class RunOnFailureKeywords(LibraryComponent):
    @keyword(tags=["Config"])
    def register_keyword_to_run_on_failure(
        self, keyword: Union[None, str]
    ) -> Union[None, str]:
        """Sets the keyword to execute, when a Browser keyword fails.

        ``keyword`` is the name of a keyword that will be executed if a
        Browser keyword fails. It is possible to use any available
        keyword, including user keywords or keywords from other libraries,
        but the keyword must not take any arguments.

        The initial keyword to use is set when `importing` the library, and
        the keyword that is used by default is `Take Screenshot`.
        Taking a screenshot when something failed is a very useful
        feature, but notice that it can slow down the execution.

        It is possible to use string ``NONE`` or any other robot falsy name,
        case-insensitively, as well as Python ``None`` to disable this
        feature altogether.

        This keyword returns the name of the previously registered
        failure keyword or Python ``None`` if this functionality was
        previously disabled. The return value can be always used to
        restore the original value later.

        Example:
        | `Register Keyword To Run On Failure`    Take Screenshot
        | ${previous kw}=    `Register Keyword To Run On Failure`    NONE
        | `Register Keyword To Run On Failure`    ${previous kw}

        """
        old_keyword = self.library.run_on_failure_keyword
        keyword = None if is_falsy(keyword) else keyword
        self.library.run_on_failure_keyword = keyword
        logger.info(f"{keyword or 'No keyword'} will be run on failure.")
        return old_keyword
