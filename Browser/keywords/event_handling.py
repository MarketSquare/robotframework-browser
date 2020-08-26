import json
from pathlib import Path

from robotlibcore import keyword  # type: ignore

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request
from ..utils import logger
from ..utils.data_types import DialogAction


class EventHandling(LibraryComponent):
    @keyword(tags=["PageContent", "EventHandler"])
    def handle_future_dialogs(self, action: DialogAction, prompt_input: str = ""):
        """ Handle next dialog on page with ``action``. Dialog can be any of alert,
        beforeunload, confirm or prompt.

            ``action`` < ``accept`` | ``dismiss`` | ``ignore`` > How to handle the alert. **Required**

            ``ignore`` will clear any existing alert handlers.

            ``prompt_input`` <str> The value to enter into prompt. Only valid if
            ``action`` equals accept. Defaults to empty string.
        """

        with self.playwright.grpc_channel() as stub:
            if prompt_input and action is not DialogAction.accept:
                raise ValueError("prompt_input is only valid if action is 'accept'")
            response = stub.HandleFutureDialogs(
                Request().DialogAction(action=action.name, promptInput=prompt_input)
            )
            logger.debug(response.log)

    @keyword(tags=["Setter", "PageContent", "EventHandler"])
    def handle_future_upload(self, path: str):
        """ Upload file from ``path`` into next file chooser dialog on page.

        ``path`` <str> Path to file to be uploaded.

        Example use:

        | Upload File    ${CURDIR}/test_upload_file
        | Click          \\#file_chooser

        """
        p = Path(path)
        p.resolve(strict=True)
        with self.playwright.grpc_channel() as stub:
            response = stub.HandleFutureUpload(Request().FilePath(path=str(p)))
            logger.debug(response.log)

    @keyword(tags=["Wait", "EventHandler"])
    def wait_for_download(self, saveAs: str = ""):
        """ Waits for next download event on page. Returns file path to downloaded file.

            To enable downloads context's ``acceptDownloads`` needs to be true.

            With default filepath downloaded files are deleted when Context the download happened in is closed.

            ``saveAs`` <str> Filename to save as. File will also temporarily be saved in playwright context's default download location.

            Example usage:
            | New Context      acceptDownloads=True
            | New Page         ${LOGIN_URL}
            | ${dl_promise}    Promise To  Wait For Download
            | Click            \\#file_download
            | ${file_path}=    Wait For  ${dl_promise}
        """
        with self.playwright.grpc_channel() as stub:
            if not saveAs:
                response = stub.WaitForDownload(Request().FilePath())
                logger.debug(response.log)
                return json.loads(response.json)
            else:
                p = Path(saveAs)
                p.resolve()
                response = stub.WaitForDownload(Request().FilePath(path=str(p)))
                logger.debug(response.log)
                return json.loads(response.json)
