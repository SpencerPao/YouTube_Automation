from . import app_config, authentication, download_my_uploads, new_description, update_description
__all__ = ["app_config", "authentication", "download_my_uploads",
           "new_description", "update_description"]
from . import _version
__version__ = _version.get_versions()['version']
