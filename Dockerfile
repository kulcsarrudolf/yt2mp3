FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app/

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Create output directory
RUN mkdir -p /output

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Default command
ENTRYPOINT ["yt2mp3"]
CMD ["--help"]

