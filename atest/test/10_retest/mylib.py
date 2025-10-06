from pathlib import Path

from robot.libraries.BuiltIn import BuiltIn

from Browser import Browser


def create_context_with_string_type_recordvideodir_and_get_type_of_recordVideo_dir(
    video_path,
):
    browser: Browser = BuiltIn().get_library_instance("Browser")
    record_video = {"dir": video_path}
    browser.new_context(recordVideo=record_video)
    url = BuiltIn().get_variable_value("${LOGIN_URL}")
    browser.new_page(url)
    return str(type(record_video["dir"]))


def create_context_with_path_type_recordvideodir_and_get_type_of_recordVideo_dir(
    video_path,
):
    browser: Browser = BuiltIn().get_library_instance("Browser")
    record_video = {"dir": Path(video_path)}
    browser.new_context(recordVideo=record_video)
    url = BuiltIn().get_variable_value("${LOGIN_URL}")
    browser.new_page(url)
    return str(type(record_video["dir"]))


def create_persistent_context_with_string_type_recordvideodir_and_get_type_of_recordVideo_dir(
    video_path,
):
    browser: Browser = BuiltIn().get_library_instance("Browser")
    record_video = {"dir": video_path}
    url = BuiltIn().get_variable_value("${LOGIN_URL}")
    browser.new_persistent_context(recordVideo=record_video, url=url)
    return str(type(record_video["dir"]))


def create_persistent_context_with_path_type_recordvideodir_and_get_type_of_recordVideo_dir(
    video_path,
):
    browser: Browser = BuiltIn().get_library_instance("Browser")
    record_video = {"dir": Path(video_path)}
    url = BuiltIn().get_variable_value("${LOGIN_URL}")
    browser.new_persistent_context(recordVideo=record_video, url=url)
    return str(type(record_video["dir"]))
