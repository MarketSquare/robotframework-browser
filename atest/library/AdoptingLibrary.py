from pathlib import Path

from robot.api.deco import keyword

from Browser import Browser
from Browser.utils.data_types import RecordVideo, ViewportDimensions


class AdoptingLibrary(Browser):
    @keyword
    def open_adopted_context_with_recording(
        self,
        user_data_dir: str,
        url: str,
        headless: bool,
        tracing: Path | None,
        record_video: RecordVideo,
        viewport: ViewportDimensions | None = None,
    ) -> str:
        """Opens a persistent context in the JavaScript extension with the options of
        ``adopted_context_options``, registers it with ``register_adopted_context``
        and returns the path of its video."""
        options = self.adopted_context_options(
            tracing=tracing, recordVideo=record_video, viewport=viewport
        )
        adopted = self.call_js_keyword(
            "openAdoptedPersistentContextWithRecording",
            userDataDir=user_data_dir,
            url=url,
            headless=headless,
            viewport=viewport,
            **options,
        )
        return self.register_adopted_context(
            adopted["contextId"], options, adopted["videoPath"]
        )

    @keyword
    def video_size_of_the_active_context(self) -> ViewportDimensions | None:
        """Returns the video size that Browser embeds in the log for the active
        context, or ``None`` if it has none."""
        return self.context_cache.get(self.get_context_ids("ACTIVE", "ACTIVE")[0])
