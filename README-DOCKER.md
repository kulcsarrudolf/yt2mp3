# yt2mp3 Docker Guide

This guide covers how to use yt2mp3 with Docker.

## Quick Start

### Build the Image

```bash
docker build -t yt2mp3 .
```

### Basic Usage

**Helper Script (Easiest):**

```bash
./docker-run.sh --url "YOUTUBE_URL" --start-time 1:12 --duration 3:00 --output-dir /output
```

**Direct Docker Command:**

```bash
docker run --rm \
  -v "$(pwd)/output:/output" \
  yt2mp3 --url "YOUTUBE_URL" --start-time 1:12 --duration 3:00 --output-dir /output
```

**Docker Compose:**

```bash
docker-compose run --rm yt2mp3 \
  --url "YOUTUBE_URL" \
  --start-time 1:12 \
  --duration 3:00 \
  --output-dir /output
```

## Examples

### Download a 3-minute clip

```bash
./docker-run.sh \
  --url "https://youtube.com/watch?v=VIDEO_ID" \
  --start-time 1:12 \
  --duration 3:00 \
  --output-dir /output
```

Output: `./output/Video_Title.mp3`

### Download with specific start and end times

```bash
docker run --rm \
  -v "$(pwd)/output:/output" \
  yt2mp3 \
  --url "https://youtube.com/watch?v=VIDEO_ID" \
  --start-time 1:13:57 \
  --end-time 1:52:50 \
  --output-dir /output
```

### Download with authentication (Chrome cookies)

```bash
docker run --rm \
  -v "$(pwd)/output:/output" \
  -v "$(pwd)/examples:/config:ro" \
  yt2mp3 \
  --url "https://youtube.com/watch?v=VIDEO_ID" \
  --start-time 10:00 \
  --duration 5:00 \
  --output-dir /output \
  --ytdl-config /config/yt2mp3.conf
```

### Custom filename and quality

```bash
./docker-run.sh \
  --url "https://youtube.com/watch?v=VIDEO_ID" \
  --start-time 30:21 \
  --duration 25:00 \
  --output-dir /output \
  --filename "my_clip" \
  --quality 192
```

## Volume Mounts

The Docker container needs access to:

1. **Output directory** (`/output`): Where downloaded MP3 files are saved

   ```bash
   -v "$(pwd)/output:/output"
   ```

2. **Config directory** (`/config`): For authentication configs (optional)
   ```bash
   -v "$(pwd)/examples:/config:ro"
   ```

## Troubleshooting

### Permission Issues

If you get permission errors with output files:

```bash
# Create output directory with correct permissions
mkdir -p output
chmod 777 output

# Or use your user ID
docker run --rm \
  --user $(id -u):$(id -g) \
  -v "$(pwd)/output:/output" \
  yt2mp3 --url "URL" --start-time 1:12 --duration 3:00 --output-dir /output
```

### Authentication Required

If you get "Sign in to confirm you're not a bot":

1. Create or update `examples/yt2mp3.conf` with your browser:

   ```
   --cookies-from-browser chrome
   ```

2. Mount the config:

   ```bash
   docker run --rm \
     -v "$(pwd)/output:/output" \
     -v "$(pwd)/examples:/config:ro" \
     yt2mp3 --url "URL" --start-time 1:12 --duration 3:00 --output-dir /output --ytdl-config /config/yt2mp3.conf
   ```

   **Note:** Cookie extraction from browsers doesn't work inside Docker. You need to:

   - Run yt2mp3 outside Docker once to extract cookies
   - Or manually export cookies to a file and mount it

### Check Logs

To see verbose output:

```bash
docker run --rm \
  -v "$(pwd)/output:/output" \
  yt2mp3 --url "URL" --start-time 1:12 --duration 3:00 --output-dir /output
```

(Remove `--quiet` flag for full output)

## Building for Production

### Build with specific tag

```bash
docker build -t yt2mp3:1.0.0 .
```

### Multi-platform build

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t yt2mp3:latest .
```

### Push to registry

```bash
docker tag yt2mp3:latest your-registry/yt2mp3:latest
docker push your-registry/yt2mp3:latest
```

## Advanced Usage

### Interactive Shell

```bash
docker run --rm -it \
  -v "$(pwd)/output:/output" \
  --entrypoint /bin/bash \
  yt2mp3
```

### Check version

```bash
docker run --rm yt2mp3 --version
```

### Run specific Python command

```bash
docker run --rm yt2mp3 python3 -m yt2mp3 --help
```

## Environment Variables

Set environment variables:

```bash
docker run --rm \
  -e PYTHONUNBUFFERED=1 \
  -v "$(pwd)/output:/output" \
  yt2mp3 --url "URL" --start-time 1:12 --duration 3:00 --output-dir /output
```

## Benefits of Docker

- ✅ **No Python installation needed** - Everything is containerized
- ✅ **Consistent environment** - Works the same everywhere
- ✅ **Easy cleanup** - Remove with `docker rmi yt2mp3`
- ✅ **Isolated** - Doesn't affect your system
- ✅ **Portable** - Share the same image across machines

## Resources

- [Dockerfile](Dockerfile)
- [docker-compose.yml](docker-compose.yml)
- [docker-run.sh](docker-run.sh)
- [Main README](README.md)
