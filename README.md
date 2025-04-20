# SmallClosedWorld

A Django REST Framework API with background task processing using Celery and Redis.

---

## Features
- Secure REST API with JWT authentication
- Asynchronous background task processing with Celery
- Environment-specific configurations (Development/Production)
- PostgreSQL database support
- Redis used as both Celery broker and result backend

---

## Requirements (Without Docker)
- Python 3.8+
- Redis Server
- PostgreSQL (for production environments)

---

## Installation

### Clone the repository
```bash
git clone https://github.com/Ozii-cr/SmallClosedWorld.git
cd SmallClosedWorld
```

### Without Docker

1. **Create and activate virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Create and configure environment variables:**
```bash
cp .env.example .env
```
Edit `.env` and set appropriate environment variables (DEBUG, DATABASE_URL, etc.).

4. **Run setup script:**
```bash
python setup.py
```
This will:
- Run migrations
- Set up the database
- Prompt to create a superuser

### With Docker (Recommended)

1. **Start containers:**
```bash
docker compose up -d
```

2. **Create Django superuser:**
```bash
docker exec -it smallclosedworld-web-1 python manage.py createsuperuser
```
Use the superuser account to authenticate and obtain JWT tokens.

---

## Running the Application

### Development

Start the necessary services manually:
```bash
# Start Redis
redis-server

# Start Celery worker
celery -A core worker -l info

# Start Django server
python manage.py runserver
```

### Production
- Set `ENVIRONMENT=production` in `.env`
- Use PostgreSQL for `DATABASE_URL`
- Set `DEBUG=False` for security
- Deploy using Gunicorn/uWSGI + Nginx (or similar)

---

## API Documentation
- **Local:** [http://localhost:8000/api/v1/swagger/](http://localhost:8000/api/v1/swagger/)
- **Production:** [https://scw.vitalenex/api/v1/swagger](https://scw.vitalenex/api/v1/swagger)

**Note:**
- Use the superuser credentials to generate a token.
- If testing live, you can use:
  - Username: `scw-admin`
  - Password: `scw-admin123`

**Additional Note:**
- Background tasks triggered through Celery are designed to run for **two minutes**.

---

## Testing

### Unit Tests

Unit tests are designed to mock Celery tasks, so Redis or a full Celery setup is not required.

Run all tests:
```bash
python manage.py test api.tests
```

---

## Infrastructure Overview

### Design
- Follows a **GitOps architecture**.
- AWS resources managed automatically via GitHub Actions pipeline.

### Resources Created
- Elastic Container Registry (ECR) 
- Virtual Private Cloud (VPC)
- Security Group allowing required traffic
- EC2 instance for application deployment

**Pipeline configuration file:**
```bash
.github/workflows/gitops.yaml
```

---

## CI/CD Pipeline Design

### Stages
1. **Testing:** Run Django tests to ensure code quality.
2. **Security Scan:** Use Trivy to scan for vulnerabilities.
3. **Build and Push:** Build Docker image and push to ECR.
4. **Deploy:** Connect to EC2 instance and deploy the new version.

**Pipeline configuration file:**
```bash
.github/workflows/cicd.yaml
```

---

## Additional Notes
- Docker containers use a healthcheck that pings the Swagger endpoint to confirm readiness.
- The `.env` file is critical for both development and production.
- Make sure Redis and PostgreSQL services are properly configured if not using Docker.
- If Docker compose doesn't work, take down the containers and volume using `docker composer down -v` and start services again

---

## Quick Commands Summary
| Purpose | Command |
|:--------|:--------|
| Create Virtual Env | `python -m venv venv && source venv/bin/activate` |
| Start Docker Containers | `docker compose up -d` |
| Create Django Superuser | `docker exec -it smallclosedworld-web-1 python manage.py createsuperuser` |
| Run Tests | `python manage.py test api.tests` |
| Start Celery Worker | `celery -A core worker -l info` |

---

