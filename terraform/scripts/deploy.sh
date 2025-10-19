#!/bin/bash
set -e

# Paths
PROJECT_PATH="/var/www/html/promptforge"
TEMP_PATH="/tmp/promptforge"

# Ensure the main project directory exists
mkdir -p "$PROJECT_PATH"

# Remove old deployment files
sudo rm -rf "$PROJECT_PATH/*"

# Move new files from temporary directory
cp -r "$TEMP_PATH/"* "$PROJECT_PATH/"

# Move .env file to project directory
cp /tmp/.env "$PROJECT_PATH/.env"
sudo rm /tmp/.env

sudo rm -rf "$TEMP_PATH/*"


sudo chown -R $USER:$USER "$PROJECT_PATH"

# Move into project directory
cd "$PROJECT_PATH"

# Ensure Docker Compose is installed
if ! command -v docker &> /dev/null
then
  echo "Error: Docker is not installed. Please install Docker first."
  exit 1
fi

if ! command -v docker compose &> /dev/null
then
  echo "Error: Docker Compose is not installed. Please install Docker Compose first."
  exit 1
fi


# Pull latest images
echo "Pulling latest Docker images..."
docker compose pull &> /dev/null

# Build and start containers in detached mode
echo "Building and starting containers..."
docker compose up -d --build &> /dev/null

# Display running containers
echo "Deployment completed. Running containers:"
docker compose ps
