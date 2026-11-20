from robot.libraries.BuiltIn import BuiltIn


def set_presenter_mode(status: dict | bool = False):
    """Set presenter mode in Browser library"""
    browser = BuiltIn().get_library_instance("browser")
    print(f"Set presenter_mode to {status}")
    browser.presenter_mode = status
