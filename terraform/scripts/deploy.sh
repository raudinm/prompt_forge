#!/bin/bash
set -e
set -x  # Print each command for logs

# Paths
PROJECT_PATH="/var/www/html/promptforge"
TEMP_PATH="/tmp/promptforge"

# Ensure the main project directory exists
sudo mkdir -p "$PROJECT_PATH"

# Remove old deployment files
sudo rm -rf "$PROJECT_PATH/*"

# Move new files from temporary directory
sudo mv "$TEMP_PATH/"* "$PROJECT_PATH/"

# Write environment variables
if [ -n "${ENV_VARS}" ]; then
  echo "${ENV_VARS}" | sudo tee "$PROJECT_PATH/.env"
else
  echo "No environment variables provided."
fi

# Move into project directory
cd "$PROJECT_PATH"

# Ensure Docker Compose is installed
if ! command -v docker &> /dev/null
then
  echo "Docker is not installed. Please install Docker first."
  exit 1
fi

if ! command -v docker compose &> /dev/null
then
  echo "Docker Compose is not installed. Please install Docker Compose first."
  exit 1
fi


# Pull latest images
docker compose pull

# Build and start containers in detached mode
docker compose up -d --build

# Display running containers
docker compose ps
