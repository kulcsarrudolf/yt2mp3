# yt-mp3-downloader

A simple command-line tool to extract specific portions of YouTube videos as MP3 files.

## Why I Built This

I needed to download MP3 files from YouTube videos, but I hate those websites full of ads. I saw it as a high-risk trying random pages, and they wanted to charge money for specific things like downloading a particular part from a video. So I decided to vibe code this myself.

Now I can extract exactly what I need from any YouTube video without dealing with sketchy websites or paying for basic features.

## Features

- ✅ Extract any portion of a YouTube video by time range
- ✅ Download full videos or specific segments
- ✅ Multiple time format support (HH:MM:SS, MM:SS, or seconds)
- ✅ Multiple output formats (mp3, m4a, opus)
- ✅ Configurable audio quality
- ✅ Authentication support for restricted videos

## Requirements

- Python 3.6+
- ffmpeg

### Install ffmpeg

**macOS:**

```bash
brew install ffmpeg
```

**Linux:**

```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch
sudo pacman -S ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

## Web Interface

**🌐 Try it online:** [https://kulcsarrudolf.github.io/yt2mp3/](https://kulcsarrudolf.github.io/yt2mp3/)

Beautiful, user-friendly web interface - no installation needed!

![Web Interface](https://img.shields.io/badge/Interface-Available-brightgreen)
![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-blue)

**Features:**
- 📝 Paste YouTube URL
- ⏱️ Enter start/end times or use quick duration buttons (+10s, +30s, +1m, +5m, +10m)
- 🎵 Choose format (MP3, M4A, Opus) and quality
- 📋 Get ready-to-use Docker or CLI commands
- 📋 One-click copy to clipboard

**Or run locally:** Open `index.html` in your browser

## Installation

### Using Docker (Easiest!)

Docker provides the simplest way to run yt2mp3 without worrying about Python versions or dependencies.

**Quick Start:**

```bash
# Clone the repository
git clone git@github.com:kulcsarrudolf/yt2mp3.git
cd yt2mp3

# Build the Docker image
docker build -t yt2mp3 .

# Run with the helper script
./docker-run.sh --url "YOUTUBE_URL" --start-time 1:12 --duration 3:00 --output-dir /output

# Or use docker directly
docker run --rm -v "$(pwd)/output:/output" yt2mp3 --url "URL" --start-time 1:12 --end-time 4:12 --output-dir /output

# Or use docker-compose
docker-compose run --rm yt2mp3 --url "URL" --start-time 1:12 --duration 3:00 --output-dir /output
```

**With Authentication (Chrome cookies):**

```bash
docker run --rm \
  -v "$(pwd)/output:/output" \
  -v "$(pwd)/examples:/config:ro" \
  yt2mp3 --url "URL" --start-time 1:12 --duration 3:00 --output-dir /output --ytdl-config /config/yt2mp3.conf
```

**Why Docker?**

- ✅ No Python installation needed
- ✅ All dependencies included
- ✅ Works the same on all platforms
- ✅ Isolated from your system
- ✅ Easy to update and remove

### Using uv (Recommended - Fast!)

[uv](https://github.com/astral-sh/uv) is an extremely fast Python package manager written in Rust. It's 10-100x faster than pip!

**Quick Install:**

```bash
# Install uv (if you don't have it)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone git@github.com:kulcsarrudolf/yt2mp3.git
cd yt2mp3

# Install with uv
uv pip install -e .

# Or create a virtual environment first (recommended)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

**Why uv?**

- ⚡ 10-100x faster than pip
- 🦀 Written in Rust for maximum performance
- 🎯 Drop-in replacement for pip commands
- 🔒 Better dependency resolution
- 💾 Smart caching system

### Using pip (Traditional)

```bash
git clone git@github.com:kulcsarrudolf/yt2mp3.git
cd yt2mp3
pip install -e .
```

## Usage

### Basic Command

```bash
yt2mp3 --url "YOUTUBE_URL" --start-time START --end-time END
```

Or use the short form:

```bash
yt2mp3 --url URL --start-time 30:21 --duration 25:00
```

### Options

```
Required:
  --url URL                YouTube video URL

Time Selection:
  --start-time TIME        Start time (HH:MM:SS, MM:SS, or seconds)
  --end-time TIME          End time (HH:MM:SS, MM:SS, or seconds)
  --duration TIME          Duration from start-time (alternative to --end-time)

Output:
  -o, --output-dir DIR     Output directory (default: current directory)
  --filename NAME          Output filename without extension
  --format FORMAT          Output format: mp3, m4a, opus (default: mp3)
  --quality QUALITY        Audio quality in kbps (default: 320)

Authentication:
  --ytdl-config FILE       Path to youtube-dl config file

Other:
  -q, --quiet              Suppress output
  -h, --help               Show help message
  --version                Show version
```

## Examples

### Extract a portion of a video

```bash
# Download 25 minutes starting from 30:21
yt2mp3 --url "https://youtube.com/watch?v=VIDEO_ID" --start-time 30:21 --duration 25:00

# Download from 1:13:57 to 1:52:50
yt2mp3 --url "https://youtube.com/watch?v=VIDEO_ID" --start-time 1:13:57 --end-time 1:52:50

# Using seconds (1821 seconds = 30:21)
yt2mp3 --url "https://youtube.com/watch?v=VIDEO_ID" --start-time 1821 --duration 1500
```

### Download entire video

```bash
# If no time parameters are specified, downloads the entire video
yt2mp3 --url "https://youtube.com/watch?v=VIDEO_ID"
```

### Specify output location and filename

```bash
yt2mp3 --url "https://youtube.com/watch?v=VIDEO_ID" \
      --start-time 30:21 \
      --duration 25:00 \
      --output-dir ~/Music \
      --filename "my_extract"
```

### Different output formats

```bash
# Output as OPUS (smaller file size)
yt2mp3 --url "https://youtube.com/watch?v=VIDEO_ID" \
      --start-time 30:21 \
      --duration 25:00 \
      --format opus

# Output as M4A
yt2mp3 --url "https://youtube.com/watch?v=VIDEO_ID" \
      --start-time 30:21 \
      --duration 25:00 \
      --format m4a
```

### Adjust audio quality

```bash
# Higher quality (320kbps is default)
yt2mp3 --url "https://youtube.com/watch?v=VIDEO_ID" \
      --start-time 30:21 \
      --duration 25:00 \
      --quality 320

# Lower quality for smaller file size
yt2mp3 --url "https://youtube.com/watch?v=VIDEO_ID" \
      --start-time 30:21 \
      --duration 25:00 \
      --quality 128
```

### Quiet mode

```bash
# Suppress output messages
yt2mp3 --url "https://youtube.com/watch?v=VIDEO_ID" \
      --start-time 30:21 \
      --duration 25:00 \
      --quiet
```

## Time Format Options

The tool supports flexible time formats:

| Format     | Example   | Description                 |
| ---------- | --------- | --------------------------- |
| `HH:MM:SS` | `1:30:21` | Hours, minutes, and seconds |
| `MM:SS`    | `30:21`   | Minutes and seconds         |
| Seconds    | `1821`    | Total seconds               |

**Examples:**

- `1:13:57` = 1 hour, 13 minutes, 57 seconds
- `30:21` = 30 minutes, 21 seconds
- `1821` = 1821 seconds (30 minutes, 21 seconds)

## Authentication for Restricted Videos

Some videos require authentication. Create a config file with browser cookies:

**Create config file:** `yt2mp3.conf`

```
--cookies-from-browser chrome
```

Use available browsers: `chrome`, `firefox`, `safari`, `edge`, `opera`, `brave`

**Then use it:**

```bash
yt2mp3 --url "https://youtube.com/watch?v=VIDEO_ID" \
      --start-time 30:21 \
      --duration 25:00 \
      --ytdl-config yt2mp3.conf
```

## How It Works

1. **Fetch video info** - Retrieves video metadata from YouTube
2. **Download audio** - Downloads the best quality audio stream
3. **Extract portion** - Uses ffmpeg to extract the specified time range
4. **Convert format** - Converts to the desired output format (MP3, M4A, or OPUS)
5. **Save file** - Saves to the specified output directory

## Common Use Cases

### Extract a podcast segment

```bash
yt2mp3 --url "PODCAST_URL" --start-time 15:30 --duration 45:00 -o ~/Podcasts
```

### Extract a song from a concert video

```bash
yt2mp3 --url "CONCERT_URL" --start-time 1:23:45 --end-time 1:27:30 --filename "song_name"
```

### Extract multiple segments from a lecture

```bash
# Part 1
yt2mp3 --url "LECTURE_URL" --start-time 5:00 --end-time 25:00 --filename "lecture_part1"

# Part 2
yt2mp3 --url "LECTURE_URL" --start-time 30:00 --end-time 50:00 --filename "lecture_part2"
```

## Troubleshooting

### "Sign in to confirm you're not a bot"

Use the `--ytdl-config` option with a config file that includes `--cookies-from-browser chrome`

### "ffmpeg not found"

Install ffmpeg using your package manager (see Requirements section)

### "Start time must be before end time"

Check that your `--start-time` is earlier than `--end-time`, or use `--duration` instead

### Download is slow

YouTube may throttle download speeds. This is normal and expected behavior.

## Contributing

Feel free to contribute! This is a personal project but pull requests are welcome.
