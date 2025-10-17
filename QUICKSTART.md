# yt-mp3-downloader Quick Start Guide

## Installation

### Using uv (Recommended - 10-100x faster!)

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install
git clone git@github.com:kulcsarrudolf/yt2mp3.git
cd yt2mp3

# With virtual environment (recommended)
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -e .

# Or directly
uv pip install -e .
```

### Using pip

```bash
git clone git@github.com:kulcsarrudolf/yt2mp3.git
cd yt2mp3
pip install -e .
```

## Basic Usage

### Download a portion of a video

```bash
# Extract 25 minutes starting at 30:21
yt2mp3 --url "https://youtube.com/watch?v=VIDEO_ID" \
      --start-time 30:21 \
      --duration 25:00

# Extract from 1:13:57 to 1:52:50
yt2mp3 --url "https://youtube.com/watch?v=VIDEO_ID" \
      --start-time 1:13:57 \
      --end-time 1:52:50
```

### Download entire video

```bash
yt2mp3 --url "https://youtube.com/watch?v=VIDEO_ID"
```

### Specify output location

```bash
yt2mp3 --url "https://youtube.com/watch?v=VIDEO_ID" \
      --start-time 30:21 \
      --duration 25:00 \
      --output-dir ~/Music \
      --filename "my_extract"
```

## Authentication (for restricted videos)

Create a config file `yt2mp3.conf`:

```
--cookies-from-browser chrome
```

Use it:

```bash
yt2mp3 --url "https://youtube.com/watch?v=VIDEO_ID" \
      --start-time 30:21 \
      --duration 25:00 \
      --ytdl-config yt2mp3.conf
```

## Time Formats

- **HH:MM:SS**: `1:30:21` (1 hour, 30 minutes, 21 seconds)
- **MM:SS**: `30:21` (30 minutes, 21 seconds)
- **Seconds**: `1821` (1821 seconds)

## Common Options

| Option         | Description                          |
| -------------- | ------------------------------------ |
| `--url`        | YouTube video URL (required)         |
| `--start-time` | Start time for extraction            |
| `--end-time`   | End time for extraction              |
| `--duration`   | Duration from start-time             |
| `--output-dir` | Output directory                     |
| `--filename`   | Output filename (without extension)  |
| `--format`     | Output format: mp3, m4a, opus        |
| `--quality`    | Audio quality in kbps (default: 320) |
| `--quiet`      | Suppress output                      |

## Examples

**Extract podcast segment:**

```bash
yt2mp3 --url "PODCAST_URL" --start-time 15:30 --duration 45:00
```

**Extract song from concert:**

```bash
yt2mp3 --url "CONCERT_URL" --start-time 1:23:45 --end-time 1:27:30
```

**Lower quality for smaller file:**

```bash
yt2mp3 --url "VIDEO_URL" --start-time 30:21 --duration 25:00 --quality 128
```

For more details, see [README.md](README.md)
