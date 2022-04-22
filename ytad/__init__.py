from . import authentication, download_my_uploads, new_description, update_description
__all__ = ["authentication", "download_my_uploads",
           "new_description", "update_description"]
from . import _version
__version__ = _version.get_versions()['version']
