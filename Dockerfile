# Use a lightweight official Python image
FROM python:3.12-slim

# Prevents Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=prompt_forge.settings

# Install system dependencies required for PostgreSQL and builds
RUN apt update && apt install -y vim build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first (for better Docker caching)
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the entire project into the container
COPY . .

# Default command: run Django with Gunicorn in production
CMD ["gunicorn", "prompt_forge.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
