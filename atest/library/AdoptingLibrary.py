from pathlib import Path

from robot.api.deco import keyword

from Browser import Browser
from Browser.utils.data_types import RecordVideo


class AdoptingLibrary(Browser):
    @keyword
    def open_adopted_context_with_recording(
        self,
        user_data_dir: str,
        url: str,
        headless: bool,
        tracing: Path,
        record_video: RecordVideo,
    ) -> str:
        """Opens a persistent context in the JavaScript extension with the options of
        ``adopted_context_options``, registers it with ``register_adopted_context``
        and returns the path of its video."""
        options = self.adopted_context_options(
            tracing=tracing, recordVideo=record_video
        )
        adopted = self.call_js_keyword(
            "openAdoptedPersistentContextWithRecording",
            userDataDir=user_data_dir,
            url=url,
            headless=headless,
            **options,
        )
        return self.register_adopted_context(
            adopted["contextId"], options, adopted["videoPath"]
        )
