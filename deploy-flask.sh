#!/bin/bash

# Make sure Docker Swarm is initialized
if ! docker info | grep -q "Swarm: active"; then
  echo "Initializing Docker Swarm..."
  # Get IP address in a way that works on macOS
  IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n 1)
  docker swarm init --advertise-addr "$IP"
else
  echo "Docker Swarm is already initialized."
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
  echo "Error: .env file not found!"
  echo "Please create a .env file with your environment variables."
  exit 1
fi

# Build the Docker image
echo "Building Flask app image..."
docker build -t localhost/flask-websocket-app:latest .

# Deploy the stack with environment variables from .env
echo "Deploying Flask app to Swarm with environment variables..."
docker stack deploy -c flask-simple-stack.yaml flask-app

# Verify deployment
echo "Deployment complete. Checking service status..."
sleep 5
docker stack services flask-app
