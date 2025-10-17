"""Functions for interacting with YouTube."""

import os
import yt_dlp
from sys import stdout
from simber import Logger
from ytmp3 import defaults
from ytmp3.exceptions import ExtractError
from downloader_cli.download import Download

logger = Logger("yt")


def progress_handler(d):
    """Handle download progress display."""
    d_obj = Download('', '', icon_done="━", icon_left="━",
                     icon_current=" ", color_done="green", color_left="black", icon_border=" ")

    if d['status'] == 'downloading':
        length = d_obj._get_terminal_length()
        time_left = d['eta']
        f_size_disp, dw_unit = d_obj._format_size(d['downloaded_bytes'])

        try:
            total_bytes = d['total_bytes']
        except KeyError:
            total_bytes = d['total_bytes_estimate']

        percent = d['downloaded_bytes'] / total_bytes * 100
        speed, s_unit, time_left, time_unit = d_obj._get_speed_n_time(
            d['downloaded_bytes'],
            0,
            cur_time=d['elapsed'] - 6
        )

        status = r"%-7s" % ("%s %s" % (round(f_size_disp), dw_unit))
        if d['speed'] is not None:
            speed, s_unit = d_obj._format_speed(d['speed'] / 1000)
            status += r"| %-3s " % ("%s %s" % (round(speed), s_unit))

        status += r"|| ETA: %-4s " % ("%s %s" % (round(time_left), time_unit))
        status = d_obj._get_bar(status, length, percent)
        status += r" %-4s" % ("{}%".format(round(percent)))

        stdout.write('\r')
        stdout.write(status)
        stdout.flush()


def get_ydl_opts(ytdl_config=None):
    """Get youtube-dl options."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': False,  # Changed to False to see errors
        'no_warnings': False,
        'extract_flat': False,
    }

    # Load config file if provided - read and parse it manually
    if ytdl_config:
        config_path = None
        if os.path.isfile(ytdl_config):
            config_path = ytdl_config
        elif os.path.isdir(ytdl_config):
            config_file = os.path.join(ytdl_config, 'config')
            if os.path.isfile(config_file):
                config_path = config_file
        
        # Parse config file and add options
        if config_path:
            try:
                with open(config_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            # Handle --cookies-from-browser option
                            if line.startswith('--cookies-from-browser'):
                                browser = line.split()[-1]
                                ydl_opts['cookiesfrombrowser'] = (browser, None, None, None)
                            # Handle --cookies option
                            elif line.startswith('--cookies'):
                                cookie_file = line.split()[-1]
                                ydl_opts['cookiefile'] = cookie_file
            except Exception as e:
                logger.warning(f"Failed to parse config file: {e}")

    return ydl_opts


def clean_filename(filename):
    """Remove unwanted characters from filename."""
    # Remove or replace characters that might cause issues
    replacements = {
        ' ': '_',
        '/': '_',
        '\\': '_',
        ':': '_',
        '*': '_',
        '?': '_',
        '"': '_',
        '<': '_',
        '>': '_',
        '|': '_',
    }
    
    for old, new in replacements.items():
        filename = filename.replace(old, new)
    
    return filename


def get_title(url, ytdl_config=None):
    """Extract video title from URL."""
    ydl_opts = get_ydl_opts(ytdl_config)
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'video')
            return title, False
    except Exception as e:
        logger.error(f"Failed to extract title: {e}")
        raise ExtractError(url)


def dw(
    url,
    proxy=None,
    song_name='ytmdl_temp.mp3',
    datatype='mp3',
    no_progress=False,
    ytdl_config=None,
    dont_convert=False,
    cookiefile=None,
    creds=None
):
    """Download the video audio."""
    
    # Add extension if needed
    if (datatype == "mp3" or datatype == "opus") and not song_name.endswith(datatype):
        song_name += '.' + datatype
    elif datatype == "m4a" and not song_name.endswith(datatype):
        song_name += '.' + datatype

    try:
        # Clean the filename
        song_name = clean_filename(song_name)

        # Create download directory
        dw_dir = defaults.DEFAULT.SONG_TEMP_DIR
        if not os.path.exists(dw_dir):
            os.makedirs(dw_dir)

        # Full path for download
        filepath = os.path.join(dw_dir, song_name)
        logger.debug(f"Download path: {filepath}")

        # Set up format
        if datatype == 'mp3' or datatype == 'opus':
            format_ = 'bestaudio/best'
        elif datatype == 'm4a':
            format_ = 'bestaudio[ext=m4a]'

        # Build yt-dlp options
        ydl_opts = get_ydl_opts(ytdl_config)
        ydl_opts.update({
            'outtmpl': filepath,
            'format': format_,
        })

        # Handle opus conversion
        if datatype == "opus" and dont_convert:
            ydl_opts["postprocessors"] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': "best",
                'preferredquality': '5',
                'nopostoverwrites': True,
            }]
            ydl_opts["outtmpl"] = filepath.replace(".opus", ".webm")

        # Add progress hook if needed
        if not no_progress:
            ydl_opts['progress_hooks'] = [progress_handler]

        # Add proxy if specified
        if proxy:
            ydl_opts['proxy'] = proxy

        # Add cookie file if specified
        if cookiefile:
            ydl_opts['cookiefile'] = cookiefile

        # Add credentials if specified
        if creds:
            ydl_opts["username"] = creds.get("username", "")
            ydl_opts["password"] = creds.get("password", "")

        # Download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return filepath

    except Exception as e:
        logger.error(f"Download failed: {e}")
        return e
