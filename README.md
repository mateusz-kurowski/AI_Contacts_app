# Contact Management API

A full-stack contact management application built with FastAPI (backend) and React (frontend), featuring complete CRUD operations for managing contacts with name and phone number fields.

## Features

- ✅ **Create** new contacts with name and phone number
- ✅ **Read** all contacts with pagination support
- ✅ **Update** existing contacts
- ✅ **Delete** contacts
- ✅ **Validation** - prevents duplicate phone numbers and empty fields
- ✅ **Database persistence** with PostgreSQL
- ✅ **REST API** with comprehensive error handling
- ✅ **Test suite** with Bruno API testing

## Tech Stack

### Backend

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **PostgreSQL** - Database
- **Pydantic** - Data validation
- **Alembic** - Database migrations

### Frontend

- **React** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool

### DevOps

- **Docker & Docker Compose** - Containerization
- **Bruno** - API testing
- **uv** - Python package management


## Requirements

### Development

- **Docker & Docker Compose** - For running the full application
- **uv** - Python package manager (for backend development)
- **pnpm** - JavaScript package manager (for frontend development)

### Deployment

- **Docker** - For production deployment

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd swe_assessment
```

### 2. Environment Setup

The application uses environment variables defined in `.env` files. The default configuration should work for local development.

### 3. Run with Docker (Recommended)

#### Development Mode

```bash
# Start all services (database, backend, frontend, nginx)
docker-compose -f compose.dev.yml up --build

# Or start specific services
docker-compose -f compose.dev.yml up db adminer backend migrate --build
```

#### Production Mode

```bash
# Start production services
docker-compose -f compose.prod.yml up --build
```

### 4. Access the Application

After starting the services:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Database Admin (Adminer)**: http://localhost:8080
  - Server: `db`
  - Username: `root`
  - Password: `example`
  - Database: `dbname`

## API Endpoints

### Contact Operations

- `GET /` - Health check
- `POST /contacts/` - Create a new contact
- `GET /contacts/` - Get all contacts (supports pagination with `skip` and `limit`)
- `GET /contacts/{id}` - Get contact by ID
- `PUT /contacts/{id}` - Update contact by ID
- `DELETE /contacts/{id}` - Delete contact by ID

### Example API Usage

#### Create a Contact

```bash
curl -X POST "http://localhost:8000/contacts/" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "phone": "+1234567890"}'
```

#### Get All Contacts

```bash
curl "http://localhost:8000/contacts/"
```

#### Update a Contact

```bash
curl -X PUT "http://localhost:8000/contacts/1" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Smith", "phone": "+1987654321"}'
```

## Development

### Backend Development

```bash
cd backend
# Install dependencies
uv sync

# Run development server
uv run fastapi dev src/main.py
```

### Frontend Development

```bash
cd frontend
# Install dependencies
bun install

# Run development server
bun dev
```

### Database Migrations

```bash
# Create a new migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Apply migrations
docker-compose exec backend alembic upgrade head
```

## Testing

### API Testing with Bruno

The project includes a comprehensive Bruno test suite in the `swe-requests/` directory:

1. Import the Bruno collection from `swe-requests/`
2. Set environment to "dev" (uses `http://localhost:8000`)
3. Run tests in sequence (they are numbered for correct order)

The test suite covers:

- ✅ CRUD operations
- ✅ Input validation
- ✅ Error handling
- ✅ Duplicate prevention
- ✅ Pagination

### Manual Testing

1. Start the application: `docker-compose -f compose.dev.yml up --build`
2. Open Bruno or use curl to test endpoints
3. Use the Swagger UI at http://localhost:8000/docs for interactive testing

## Project Structure

```
swe_assessment/
├── backend/                 # FastAPI backend
│   ├── src/
│   │   ├── main.py         # FastAPI application
│   │   ├── db/             # Database models and operations
│   │   └── api/            # API endpoints
│   ├── alembic/            # Database migrations
│   └── Dockerfile          # Backend container config
├── frontend/               # React frontend
│   ├── src/                # React components and logic
│   └── Dockerfile          # Frontend container config
├── swe-requests/           # Bruno API test suite
├── compose.dev.yml         # Development docker compose
├── compose.prod.yml        # Production docker compose
└── README.md               # This file
```

## Troubleshooting

### Database Connection Issues

- Ensure PostgreSQL container is running: `docker-compose ps`
- Check database logs: `docker-compose logs db`
- Verify environment variables in `.env` files
