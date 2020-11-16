import platform

__version__ = "2.1.0"
bin_archive_filename = f"browser_wrapper-{platform.system()}-{__version__}"
bin_archive_filename_with_ext = (
    f"browser_wrapper-{platform.system()}-{__version__}.tar.gz"
)
