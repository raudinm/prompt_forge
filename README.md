# Prompt Forge [![CI](https://github.com/raudinm/prompt_forge/actions/workflows/ci.yml/badge.svg)](https://github.com/raudinm/prompt_forge/actions/workflows/ci.yml)

A Django-based application for managing AI prompts with WebSocket support.

## Features

- User authentication with JWT tokens
- Prompt creation and management
- Real-time WebSocket communication
- PostgreSQL database with vector embeddings support
- RESTful API with Django REST Framework

## Docker Execution (Recommended)

This is the recommended method for running the application in both development and production-like environments. It provides a consistent, isolated environment with all dependencies containerized.

### Prerequisites

- Docker (version 20.10 or later)
- Docker Compose (version 2.0 or later)

### Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/raudinm/prompt_forge.git
   cd prompt_forge
   ```

2. **Create the .env file**

   Copy the example environment file and configure your settings:

   ```bash
   cp .env.example .env
   ```

   Edit the `.env` file with your desired configuration. The default values in `.env.example` are suitable for local development.

3. **Start the services**

   Use Docker Compose to build and start all services:

   ```bash
   docker-compose up --build
   ```

   The first run will take longer as Docker builds the application image and pulls the database images.

4. **Access the services**

   Once the containers are running, you can access the following services:

   - **API**: http://localhost:8000 - The Django REST API
   - **PgAdmin**: http://localhost:5050 - PostgreSQL administration interface (login with credentials from .env)
   - **Database**: localhost:7654 - PostgreSQL database (accessible externally for development tools)

### Services Overview

- **api**: Django application running with Gunicorn and Uvicorn workers for ASGI support
- **db**: PostgreSQL 17 database with persistent data storage
- **pgadmin**: Web-based PostgreSQL management tool

The services are configured to restart automatically unless manually stopped.

## Local Development Setup (Without Docker)

This section provides instructions for setting up the application for local development without using Docker. This is an alternative to the Docker method described above.

### Prerequisites

- Python 3.8 or later
- PostgreSQL (version 12 or later) installed and running locally

### Setup Instructions

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Unix)
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with required environment variables (see Environment Variables section below)
6. Run migrations: `python manage.py migrate`
7. Start the server: `python manage.py runserver`

## Environment Variables

The application requires several environment variables to be configured. Below is a comprehensive list organized by category, including default values and descriptions.

### Database Configuration

- `DATABASE_NAME`: The name of the PostgreSQL database (default: `prompt_forge`). Used to specify which database the application connects to.
- `DATABASE_USER`: The username for database authentication (default: `postgres`). Credentials for accessing the PostgreSQL database.
- `DATABASE_PASSWORD`: The password for database authentication (default: `postgres`). Secure password for the database user.
- `DATABASE_HOST`: The hostname or IP address of the database server (default: `localhost` for local, `db` for Docker). Location of the PostgreSQL server.
- `DATABASE_PORT`: The port number on which the database is running (default: `5432`). Standard PostgreSQL port.

### General Settings

- `SECRET_KEY`: A secret key for Django's cryptographic signing (default: `my_super_secret_key`). Used for security features like sessions and tokens; should be unique and secret in production.
- `DEBUG`: Enables or disables Django's debug mode (default: `True` for development, `False` for production). Controls error pages and logging verbosity.
- `ALLOWED_HOSTS`: Comma-separated list of allowed hostnames (default: `localhost,127.0.0.1`). Hosts that can serve the application to prevent HTTP Host header attacks.

### PG Admin

- `PGADMIN_PORT`: The port on which PgAdmin web interface runs (default: `5050`). Port for accessing the PostgreSQL administration tool.
- `PGADMIN_DEFAULT_EMAIL`: Default email for PgAdmin admin user (default: `admin@promptforge.io`). Login email for PgAdmin.
- `PGADMIN_DEFAULT_PASSWORD`: Default password for PgAdmin admin user (default: `admin123`). Login password for PgAdmin; change in production.

### Grafana

- `GF_SECURITY_ADMIN_USER`: Admin username for Grafana (default: `admin`). Username for Grafana dashboard access.
- `GF_SECURITY_ADMIN_PASSWORD`: Admin password for Grafana (default: `admin123`). Password for Grafana admin; secure in production.

Note: For Docker setups, adjust DATABASE_HOST to `db` and DEBUG to `False`. For local development, use `localhost` and `True` respectively.

## Testing

The project uses pytest for testing with a comprehensive test suite located in `forge/tests/`.

### Test Structure

- `test_models.py` - Model tests
- `test_serializers.py` - Serializer tests
- `test_views.py` - View tests
- `test_websocket.py` - WebSocket tests
- `test_middleware.py` - Middleware tests
- `test_throttles.py` - Throttling tests

### Local Testing

Run tests with pytest:

```bash
pytest --ds=prompt_forge.settings -v
```

### CI/CD Testing

The project includes GitHub Actions workflow for automated testing:

#### Database Testing Strategies

1. **SQLite In-Memory (Default for Tests)**:

   - Fast and isolated
   - No external dependencies
   - Limited PostgreSQL feature support

2. **Mocking Strategy**:
   - Mock PostgreSQL-specific features for SQLite compatibility
   - Skip tests requiring full PostgreSQL when using SQLite

#### CI Configuration

The CI workflow (`.github/workflows/ci.yml`) uses SQLite for all tests:

- SQLite in-memory database for fast, isolated testing
- No external database dependencies
- Environment variable-based database configuration
- Automatic test execution with pytest -v for verbose output

#### Running Tests Locally

```bash
# With SQLite (default)
pytest --ds=prompt_forge.settings -v

# With PostgreSQL (requires local PostgreSQL)
DATABASE_NAME=test_db pytest --ds=prompt_forge.settings -v

# CI simulation
CI=true pytest --ds=prompt_forge.settings -v
```

## API Endpoints

### Authentication Endpoints

#### `POST /api/signup`

- **Description**: Registers a new user account.
- **Authentication**: None required
- **Request Format**:
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```
- **Response Format**:
  - Success (HTTP 201):
    ```json
    {
      "message": "User created successfully"
    }
    ```
  - Error (HTTP 400):
    ```json
    {
      "username": ["This field is required."],
      "email": ["Enter a valid email address."],
      "password": ["This field may not be blank."]
    }
    ```
- **Special Considerations**: Username must be unique. Email is optional but recommended for password recovery.

#### `POST /api/token`

- **Description**: Obtains JWT access and refresh tokens for user authentication.
- **Authentication**: None required
- **Request Format**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response Format**:
  - Success (HTTP 200):
    ```json
    {
      "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
    ```
  - Error (HTTP 401):
    ```json
    {
      "detail": "No active account found with the given credentials"
    }
    ```
- **Special Considerations**: Use the access token in Authorization header as `Bearer <token>` for authenticated requests.

#### `POST /api/token/refresh`

- **Description**: Refreshes JWT access token using a valid refresh token.
- **Authentication**: None required
- **Request Format**:
  ```json
  {
    "refresh": "string"
  }
  ```
- **Response Format**:
  - Success (HTTP 200):
    ```json
    {
      "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
    ```
  - Error (HTTP 401):
    ```json
    {
      "detail": "Token is invalid or expired"
    }
    ```
- **Special Considerations**: Refresh tokens have longer expiration times than access tokens. Store refresh tokens securely.

### Prompt Management Endpoints

#### `POST /prompts`

- **Description**: Creates a new prompt, generates an AI response, and stores vector embeddings for similarity search.
- **Authentication**: JWT Bearer token required
- **Request Format**:
  ```json
  {
    "prompt": "string",
    "send_via_websocket": false
  }
  ```
- **Response Format**:
  - Success (HTTP 201):
    ```json
    {
      "id": 1,
      "user": 1,
      "text": "What is the capital of France?",
      "response": "The capital of France is Paris.",
      "created_at": "2023-10-19T14:18:39.913Z",
      "metadata": {
        "model_used": "GPT-2",
        "sent_via_websocket": false,
        "extra_info": null
      },
      "embedding": {
        "model_name": "all-MiniLM-L6-v2",
        "vector": [0.123, 0.456, ...]
      }
    }
    ```
  - Error (HTTP 400):
    ```json
    {
      "error": "prompt is required"
    }
    ```
- **Special Considerations**: Subject to burst and sustained rate throttling. If `send_via_websocket` is true, the response is also sent via WebSocket to the authenticated user.

#### `GET /prompts/similar`

- **Description**: Retrieves prompts similar to the provided query using FAISS vector similarity search.
- **Authentication**: JWT Bearer token required
- **Request Format**: Query parameter `q` (string)
  ```
  GET /prompts/similar/?q=What is machine learning?
  ```
- **Response Format**:
  - Success (HTTP 200):
    ```json
    [
      {
        "id": 1,
        "user": 1,
        "text": "Explain machine learning",
        "response": "Machine learning is...",
        "created_at": "2023-10-19T14:18:39.913Z",
        "metadata": {
          "model_used": "GPT-2",
          "sent_via_websocket": false,
          "extra_info": null
        },
        "embedding": {
          "model_name": "all-MiniLM-L6-v2",
          "vector": [0.123, 0.456, ...]
        }
      }
    ]
    ```
  - Error (HTTP 400):
    ```json
    {
      "error": "query parameter \"q\" is required"
    }
    ```
- **Special Considerations**: Returns up to 5 most similar prompts. FAISS index is persisted on disk for performance. Subject to rate throttling.

### WebSocket Endpoints

#### `WebSocket /ws/prompts`

- **Description**: Establishes a real-time WebSocket connection for prompt updates.
- **Authentication**: JWT token required as query parameter `token`
  ```
  ws://localhost:8000/ws/prompts/?token=<jwt_access_token>
  ```
- **Message Format** (Incoming/Outgoing):
  ```json
  {
    "message": "string",
    "prompt": "string (optional)",
    "response": "string (optional)",
    "embedding_length": "integer (optional)"
  }
  ```
- **Special Considerations**: Connection requires valid JWT access token. Used for real-time updates when creating prompts with `send_via_websocket=true`. Supports both ws (local) and wss (SSL) protocols. For API testing, import the 'Prompt Forge.postman_collection.json' file located in the project root into Postman to use the API.

## Monitoring and Logging

The application includes comprehensive monitoring and logging capabilities using Prometheus and Grafana to track application performance, database metrics, and system health.

### Prometheus Configuration

Prometheus is configured via `prometheus.yml` with the following settings:

- **Global scrape interval**: 5 seconds
- **Django application metrics**: Scraped from `/metrics` endpoint on the API service (`api:8000`)
- **PostgreSQL metrics**: Collected via postgres_exporter on port 9187

### Monitored Metrics

The monitoring setup tracks the following key metrics:

#### Django Application Metrics

- **HTTP Requests**: Total requests per second by method (GET, POST, etc.)
- **Request Latency**: Average response time for HTTP requests
- **HTTP Errors**: 4xx and 5xx error rates over 5-minute intervals

#### Database Metrics

- **Active Connections**: Current number of active PostgreSQL connections
- **Query Duration**: Average time spent on database queries
- **Database Operations**: Rows fetched vs. inserted rates

#### System Metrics

- **CPU Usage**: Process CPU utilization percentage
- **Memory Usage**: Resident memory usage in MB

### Grafana Dashboard

A custom Grafana dashboard is provided in `grafana_dashboard.json` for visualizing all monitored metrics. The dashboard includes:

- Time-series charts for HTTP requests, latency, and error rates
- Database connection and query performance metrics
- CPU and memory usage graphs
- Automatic refresh every 10 seconds

To import the dashboard:

1. Access Grafana at `http://localhost:8585` (default credentials: admin/admin123)
2. Navigate to Dashboards > Import
3. Upload or paste the contents of `grafana_dashboard.json`

### Accessing Monitoring Services

When running with Docker Compose, the monitoring services are available at:

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:8585

## WebSockets

To test WebSocket connections, create a Node.js script with the following code. This example demonstrates connections to both localhost (ws) and cloud SSL (wss) endpoints, including JWT authentication placeholders and proper error handling.

```javascript
const WebSocket = require("ws");

// JWT token placeholder - replace with actual token
const jwtToken = "your-jwt-token-here";

// Example 1: Localhost WebSocket connection (ws)
const wsLocal = new WebSocket(
  `ws://localhost:8000/ws/prompts/?token=${jwtToken}`
);

wsLocal.on("open", function open() {
  console.log("Connected to localhost WebSocket");
  // Send a test message
  wsLocal.send(JSON.stringify({ message: "Hello from test client" }));
});

wsLocal.on("message", function message(data) {
  console.log("Received from localhost:", data.toString());
});

wsLocal.on("error", function error(err) {
  console.error("Localhost WebSocket error:", err);
});

wsLocal.on("close", function close() {
  console.log("Localhost WebSocket connection closed");
});

// Example 2: Cloud SSL WebSocket connection (wss)
const wsCloud = new WebSocket(
  `wss://your-domain.com/ws/prompts/?token=${jwtToken}`
);

wsCloud.on("open", function open() {
  console.log("Connected to cloud WebSocket");
  // Send a test message
  wsCloud.send(JSON.stringify({ message: "Hello from test client" }));
});

wsCloud.on("message", function message(data) {
  console.log("Received from cloud:", data.toString());
});

wsCloud.on("error", function error(err) {
  console.error("Cloud WebSocket error:", err);
});

wsCloud.on("close", function close() {
  console.log("Cloud WebSocket connection closed");
});
```

To run the test script:

1. Save the code to a file, e.g., `websocket_test.js`
2. Run the script: `node websocket_test.js`

## Development

- Uses Django Channels for WebSocket support
- PostgreSQL for production database
- FAISS for vector similarity search
- JWT authentication with django-rest-framework-simplejwt

## Deployment

The application is designed for containerized deployment using Docker Compose and automated deployment via GitHub Actions. The deployment process supports automated provisioning and scaling on remote servers.

### Prerequisites

- A remote server with SSH access (Ubuntu/Debian recommended)
- Docker and Docker Compose installed on the server
- SSH private key for server access
- Domain name configured (optional, for production use)
- GitHub repository with deployment workflow configured

### Environment Configuration

Configure the following variables as GitHub repository secrets in your repository settings. These secrets will be used by the GitHub Actions deployment workflow:

- `SECRET_KEY`: Your production secret key
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts (e.g., your-domain.com,server-ip)
- `DATABASE_NAME`: Production database name (e.g., promptforge_prod)
- `DATABASE_USER`: Database user
- `DATABASE_PASSWORD`: Secure database password
- `DATABASE_HOST`: Database host (typically `db` for Docker Compose)
- `DATABASE_PORT`: Database port (default: 5432)
- `PGADMIN_DEFAULT_EMAIL`: PgAdmin admin email
- `PGADMIN_DEFAULT_PASSWORD`: Secure PgAdmin password
- `PGADMIN_PORT`: PgAdmin port (default: 5050)
- `DEPLOY_USER`: SSH user for deployment
- `DEPLOY_HOST`: Server IP or hostname
- `DEPLOY_SSH_KEY`: Private SSH key for server access

### Deployment via GitHub Actions

1. Ensure all required GitHub repository secrets are configured as described in the Environment Configuration section.

2. Push your code changes to the main branch or trigger the deployment workflow manually from the GitHub Actions tab.

3. The GitHub Actions workflow will automatically:

   - Build and test the application
   - Transfer the application code to the server
   - Copy the deployment script and configure environment variables
   - Execute the deployment script remotely via SSH

4. Monitor the deployment progress in the GitHub Actions logs.

### Docker Compose Setup

The deployment script automatically handles Docker Compose operations on the server:

1. **Database Service**: PostgreSQL 17 with persistent data volumes
2. **API Service**: Django application running with Gunicorn and Uvicorn workers
3. **PgAdmin Service**: Web-based PostgreSQL administration interface

The services are configured to restart automatically unless stopped manually.

### Nginx Reverse Proxy (Optional)

For production deployments with a domain name, configure Nginx as a reverse proxy:

1. Install Nginx on your server:

```bash
sudo apt update
sudo apt install nginx
```

2. Copy the Nginx configuration from `nginx/promptforge.conf` to `/etc/nginx/sites-available/promptforge`:

```bash
sudo cp nginx/promptforge.conf /etc/nginx/sites-available/promptforge
```

3. Update the `server_name` directive with your domain:

```nginx
server_name your-domain.com;
```

4. Enable the site and restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/promptforge /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Accessing the Application

- **API**: `http://your-server-ip:8000` or `https://your-domain.com` (with Nginx)
- **PgAdmin**: `http://your-server-ip:5050`
- **PostgreSQL**: Accessible internally by containers on port 5432

### Monitoring and Maintenance

- View running containers: `docker compose ps`
- Check logs: `docker compose logs -f [service-name]`
- Update deployment: Push code changes to trigger the GitHub Actions workflow
- Backup database: Use PostgreSQL backup tools or Docker volume snapshots

### Security Considerations

- Use strong, unique passwords for database and PgAdmin
- Restrict SSH access and use key-based authentication
- Configure firewall rules to limit access to necessary ports
- Keep Docker images and dependencies updated
- Use HTTPS in production (configure SSL certificates with Nginx)
