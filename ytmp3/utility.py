"""Utility functions for audio conversion and time parsing."""

from os import remove
import ffmpeg
from simber import Logger
from ytmp3 import defaults

logger = Logger("Utility")


def convert_to_mp3(path, start=None, end=None, cleanup_after_done=True):
    """Convert to mp3 using ffmpeg."""
    new_name = path + '_new.mp3'
    params = {
        "loglevel": "panic",
        "ar": 44100,
        "ac": 2,
        "ab": '{}k'.format(defaults.DEFAULT.SONG_QUALITY),
        "f": "mp3"
    }

    try:
        if start is not None and end is not None:
            params["ss"] = start
            params["to"] = end

        job = ffmpeg.input(path).output(new_name, **params)
        job.run()

        if cleanup_after_done:
            remove(path)

        return new_name
    except ffmpeg._run.Error:
        return new_name


def convert_to_opus(path, start=None, end=None, cleanup_after_done=True):
    """Convert to opus using ffmpeg."""
    new_name = path + '_new.opus'
    params = {
        "loglevel": "panic",
        "f": "opus"
    }

    try:
        if start is not None and end is not None:
            params["ss"] = start
            params["to"] = end

        job = ffmpeg.input(path).output(new_name, **params)
        job.run()

        if cleanup_after_done:
            remove(path)

        return new_name
    except ffmpeg._run.Error:
        return new_name


def extract_m4a(path, start=None, end=None, cleanup_after_done=True):
    """Extract a portion of m4a file."""
    if not start and not end:
        logger.error("Cannot trim without start and end")
        return path

    new_name = path + '_new.m4a'
    try:
        job = ffmpeg.input(path).output(
            new_name, ss=start, to=end, loglevel="panic")
        job.run()

        if cleanup_after_done:
            remove(path)

        return new_name
    except ffmpeg._run.Error as e:
        logger.warning(str(e))
        return new_name


def extract_part_convert(path, format, start, end):
    """Extract part of file and convert to specified format."""
    FORMAT_MAP = {
        "mp3": convert_to_mp3,
        "opus": convert_to_opus,
        "m4a": extract_m4a
    }

    converted_name = FORMAT_MAP.get(format)(path, start, end, False)
    return converted_name


def parse_time_to_seconds(time_str):
    """
    Parse a time string to seconds.
    
    Supports formats:
    - Seconds: "90" -> 90.0
    - MM:SS: "30:21" -> 1821.0
    - HH:MM:SS: "1:30:21" -> 5421.0
    
    Returns float or None if invalid.
    """
    if not time_str:
        return None
    
    time_str = time_str.strip()
    
    # Try parsing as plain seconds first
    try:
        return float(time_str)
    except ValueError:
        pass
    
    # Try parsing as time format (HH:MM:SS or MM:SS)
    parts = time_str.split(':')
    
    try:
        if len(parts) == 2:  # MM:SS
            minutes, seconds = map(float, parts)
            return minutes * 60 + seconds
        elif len(parts) == 3:  # HH:MM:SS
            hours, minutes, seconds = map(float, parts)
            return hours * 3600 + minutes * 60 + seconds
        else:
            logger.error("Invalid time format: {}. Use HH:MM:SS, MM:SS, or seconds.".format(time_str))
            return None
    except ValueError:
        logger.error("Invalid time format: {}. Use HH:MM:SS, MM:SS, or seconds.".format(time_str))
        return None
