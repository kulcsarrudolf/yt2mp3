#!/usr/bin/env python3
"""Setup yt-mp3-downloader - YouTube Video to MP3 Extractor."""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

exec(open("yt2mp3/__version__.py").read())

# Minimal dependencies for video extraction
req_pkgs = [
    'yt-dlp>=2024.4.9',
    'ffmpeg-python',
    'simber==0.2.6',
    'downloader-cli>=0.3.4',
    'pyxdg',
]

if __name__ == '__main__':
    setuptools.setup(
        name="yt2mp3",
        version=__version__,
        description="Simple YouTube video to MP3 extractor with time-based extraction",
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=setuptools.find_packages(),
        classifiers=(
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
            "Development Status :: 4 - Beta",
            "Environment :: Console",
            "Topic :: Multimedia :: Sound/Audio",
            "Topic :: Multimedia :: Video :: Conversion",
        ),
        python_requires=">=3.10",
        install_requires=req_pkgs,
        entry_points={
            'console_scripts': [
                "yt2mp3 = yt2mp3:entry"
            ]
        },
    )
