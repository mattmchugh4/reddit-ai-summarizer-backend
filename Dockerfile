# Use the official Python image for ARM architecture
FROM python:3.9-slim-bullseye

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Default port (can be overridden by environment)
ENV PORT=5001

# Expose the port
EXPOSE 5001

# Create a simple entrypoint script
RUN echo '#!/bin/bash\n\
echo "Starting Flask app with the following configuration:"\n\
echo "FLASK_ENV: $FLASK_ENV"\n\
echo "LOG_LEVEL: $LOG_LEVEL"\n\
echo "PORT: $PORT"\n\
echo "Using Reddit API: $([ -n \"$REDDIT_CLIENT_ID\" ] && echo \"Yes\" || echo \"No\")"\n\
echo "Using OpenAI API: $([ -n \"$OPENAI_API_KEY\" ] && echo \"Yes\" || echo \"No\")"\n\
\n\
exec gunicorn --worker-class eventlet -w 1 --bind "0.0.0.0:$PORT" "wsgi:application"\n'\
> /entrypoint.sh && chmod +x /entrypoint.sh

# Use the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]