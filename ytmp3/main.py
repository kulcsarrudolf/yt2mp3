#!/usr/bin/env python3
"""
yt-mp3-downloader - Download portions of YouTube videos as MP3.
"""

from __future__ import unicode_literals

import argparse
import sys
from os import path, makedirs
from simber import Logger

from ytmp3 import yt, utility, defaults
from ytmp3.exceptions import DownloadError, ConvertError
from ytmp3.__version__ import __version__

logger = Logger('ytmp3')


def arguments():
    """Parse the arguments."""
    parser = argparse.ArgumentParser(
        description='yt-mp3-downloader - Extract audio from YouTube videos'
    )

    parser.add_argument(
        '--url',
        help="YouTube video URL (required)",
        required=True,
        type=str
    )
    parser.add_argument(
        '-o', '--output-dir',
        help="Output directory (default: current directory)",
        default=".",
        type=str
    )
    parser.add_argument(
        '--start-time',
        help="Start time (format: HH:MM:SS, MM:SS, or seconds)",
        default=None,
        type=str
    )
    parser.add_argument(
        '--end-time',
        help="End time (format: HH:MM:SS, MM:SS, or seconds)",
        default=None,
        type=str
    )
    parser.add_argument(
        '--duration',
        help="Duration from start-time (format: HH:MM:SS, MM:SS, or seconds)",
        default=None,
        type=str
    )
    parser.add_argument(
        '--format',
        help="Output format (default: mp3)",
        default='mp3',
        choices=['mp3', 'm4a', 'opus'],
        type=str
    )
    parser.add_argument(
        '--quality',
        help="Audio quality in kbps (default: 320)",
        default=320,
        type=int
    )
    parser.add_argument(
        '--filename',
        help="Output filename (without extension)",
        default=None,
        type=str
    )
    parser.add_argument(
        '--ytdl-config',
        help="Path to youtube-dl config file",
        default=None,
        type=str
    )
    parser.add_argument(
        '-q', '--quiet',
        help="Suppress output",
        action='store_true'
    )
    parser.add_argument(
        '--version',
        action='version',
        version=__version__
    )

    args = parser.parse_args()
    return args


def validate_args(args):
    """Validate command-line arguments."""
    # Validate time arguments
    if args.end_time and args.duration:
        logger.critical("Cannot use both --end-time and --duration. Use one or the other.")
        sys.exit(1)
    
    if args.start_time and not (args.end_time or args.duration):
        logger.warning(
            "--start-time specified without --end-time or --duration. "
            "The entire video from start-time will be extracted."
        )
    
    if (args.end_time or args.duration) and not args.start_time:
        logger.critical("--end-time or --duration requires --start-time to be specified.")
        sys.exit(1)


def download_video_portion(args):
    """Download and extract a portion of a YouTube video."""
    
    # Set quality
    defaults.DEFAULT.SONG_QUALITY = args.quality
    
    # Parse time parameters
    start_time = utility.parse_time_to_seconds(args.start_time) if args.start_time else None
    end_time = None
    
    if args.end_time:
        end_time = utility.parse_time_to_seconds(args.end_time)
    elif args.duration and start_time is not None:
        duration_seconds = utility.parse_time_to_seconds(args.duration)
        if duration_seconds is not None:
            end_time = start_time + duration_seconds
    
    # Validate parsed times
    if start_time is not None and end_time is not None:
        if start_time >= end_time:
            logger.critical("Start time must be before end time!")
            sys.exit(1)
        logger.info(f"Extracting from {start_time} to {end_time} seconds")
    
    # Get video title
    logger.info(f"Fetching video info from {args.url}")
    try:
        video_title, _ = yt.get_title(args.url, args.ytdl_config)
    except Exception as e:
        logger.critical(f"Failed to get video info: {e}")
        sys.exit(1)
    
    logger.info(f"Video title: {video_title}")
    
    # Download video
    logger.info("Downloading video...")
    try:
        downloaded_path = yt.dw(
            args.url,
            None,  # proxy
            video_title,
            args.format,
            no_progress=args.quiet,
            ytdl_config=args.ytdl_config,
            dont_convert=(args.format == 'm4a')
        )
        
        if not isinstance(downloaded_path, str):
            raise DownloadError(args.url, downloaded_path)
        
        logger.info("Downloaded successfully!")
    except Exception as e:
        logger.critical(f"Download failed: {e}")
        sys.exit(1)
    
    # Convert and extract portion if needed
    logger.info("Converting to MP3...")
    try:
        if start_time is not None and end_time is not None:
            # Extract specific portion
            converted_path = utility.extract_part_convert(
                downloaded_path,
                args.format,
                start_time,
                end_time
            )
        else:
            # Convert entire file
            if args.format == 'mp3':
                converted_path = utility.convert_to_mp3(downloaded_path)
            elif args.format == 'opus':
                converted_path = utility.convert_to_opus(downloaded_path)
            else:  # m4a
                converted_path = downloaded_path
        
        if not isinstance(converted_path, str):
            raise ConvertError(converted_path)
        
        logger.info("Conversion complete!")
    except Exception as e:
        logger.critical(f"Conversion failed: {e}")
        sys.exit(1)
    
    # Move to output directory
    output_dir = path.expanduser(args.output_dir)
    if not path.exists(output_dir):
        makedirs(output_dir)
    
    # Determine final filename
    if args.filename:
        final_filename = f"{args.filename}.{args.format}"
    else:
        # Use video title
        safe_title = "".join(c for c in video_title if c.isalnum() or c in (' ', '-', '_')).strip()
        final_filename = f"{safe_title}.{args.format}"
    
    final_path = path.join(output_dir, final_filename)
    
    # Move file
    import shutil
    shutil.move(converted_path, final_path)
    
    logger.info(f"Saved to: {final_path}")
    return final_path


def main():
    """Main entry point."""
    try:
        args = arguments()
        validate_args(args)
        
        if not args.quiet:
            logger.update_level("INFO")
        else:
            logger.update_level("WARNING")
        
        result = download_video_portion(args)
        logger.info("Done!")
        return 0
    
    except KeyboardInterrupt:
        logger.info("\nCancelled by user")
        return 1
    except Exception as e:
        logger.critical(f"Error: {e}")
        return 1


def entry():
    """Entry point for console script."""
    sys.exit(main())


if __name__ == '__main__':
    entry()
