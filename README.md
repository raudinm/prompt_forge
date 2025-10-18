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

2. **PostgreSQL in CI**:

   - Uses GitHub Actions service containers
   - Tests real PostgreSQL features like ArrayField
   - Requires database service setup

3. **Mocking Strategy**:
   - Mock PostgreSQL-specific features for SQLite compatibility
   - Skip tests requiring full PostgreSQL when using SQLite

#### CI Configuration

The CI workflow (`.github/workflows/ci.yml`) includes:

- PostgreSQL service container for full feature testing
- SQLite fallback for environments without PostgreSQL
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
