"""Default configuration values."""

import os
from xdg.BaseDirectory import xdg_cache_home


class DEFAULT:
    """Default configuration values."""

    # The home directory
    HOME_DIR = os.path.expanduser('~')

    # The temp directory where songs will be processed
    SONG_TEMP_DIR = os.path.join(xdg_cache_home, 'yt2mp3')

    # The song quality in kbps
    SONG_QUALITY = 320

    # Default format
    DEFAULT_FORMAT = 'mp3'

    # Valid output formats
    VALID_FORMATS = ['mp3', 'm4a', 'opus']
