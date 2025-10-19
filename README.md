# Prompt Forge

A Django-based application for managing AI prompts with WebSocket support.

## Features

- User authentication with JWT tokens
- Prompt creation and management
- Real-time WebSocket communication
- PostgreSQL database with vector embeddings support
- RESTful API with Django REST Framework

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Unix)
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with required environment variables
6. Run migrations: `python manage.py migrate`
7. Start the server: `python manage.py runserver`

## Environment Variables

Create a `.env` file in the project root with the following variables:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=your_db_password
```

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

- `POST /api/token/` - User sigin tokens
- `POST /api/token/refresh/` - User token refresh
- `GET /prompts/similar/` - Get similar prompts
- `POST /prompts/` - Create new prompt
- WebSocket: `/ws/prompts/` - Real-time prompt updates

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
