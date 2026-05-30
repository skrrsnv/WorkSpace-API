# WorkSpace API

A backend API for team and project management built with Django REST Framework.

---

## Features

- JWT Authentication
- Custom User Model
- Project Management
- Role-based Permissions (Owner / Admin / Member)
- Membership System
- Task Management
- Activity Logs (async via Celery)
- Filtering, Searching, and Ordering
- Swagger / ReDoc API Documentation
- Dockerized Environment
- PostgreSQL Database
- Asynchronous Tasks with Celery + Redis
- Automated API Tests (pytest + DRF APIClient)

---

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Docker & Docker Compose
- Poetry
- Simple JWT
- drf-spectacular
- django-filter
- pytest

---

## Async Tasks & Activity Logs

The project uses Celery and Redis for asynchronous background processing.

### Implemented async features:

- Activity log creation via Celery tasks
- Background task execution
- Redis as message broker
- Scalable task queue architecture

### Logged events:

- Project creation
- Project update
- Project deletion
- Task creation
- Task update
- Membership creation
- Membership role updates

---

## Testing

The project includes **API-level integration tests** using pytest and DRF test client.

### Covered scenarios:

- Unauthorized access protection (401)
- Project creation via API
- Role-based permissions (403 checks)
- Task CRUD operations via API
- Membership restrictions
- Activity log creation validation (Celery eager mode)

### Testing stack:

- pytest
- pytest-django
- Django test database
- DRF APIClient
- Celery eager mode for async testing

---

## Roles

- Owner
- Admin
- Member

---

## Permissions

### Owner

- Full project access
- Can delete projects
- Can manage memberships
- Can update and delete tasks

### Admin

- Can manage memberships
- Can update tasks

### Member

- Can view project data
- Can create tasks

---

## Project Structure

```text
apps/
├── activity_logs/
├── projects/
├── tasks/
├── users/

config/
````

---

## Installation

### Clone Repository

```bash
git clone <your-repository-url>
cd WorkSpace
```

---

## Environment Variables

Create a `.env` file:

```env
DEBUG=True

SECRET_KEY=your_secret_key

DB_NAME=workspace_db
DB_USER=workspace_user
DB_PASSWORD=workspace_password
DB_HOST=db
DB_PORT=5432

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

---

## Run with Docker

### Build

```bash
docker compose build
```

### Start

```bash
docker compose up
```

### Migrations

```bash
docker compose exec web python manage.py migrate
```

### Superuser

```bash
docker compose exec web python manage.py createsuperuser
```

Celery worker runs as a separate Docker service.

---

## Local Development (Poetry)

```bash
poetry install
poetry shell
python manage.py runserver
```

---

## API Documentation

### Swagger

[http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/)

### ReDoc

[http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)

---

## Authentication

### Obtain Token

POST /api/v1/token/

### Refresh Token

POST /api/v1/token/refresh/

---

## Endpoints

### Projects

```
GET     /api/v1/projects/
POST    /api/v1/projects/
GET     /api/v1/projects/{id}/
PUT     /api/v1/projects/{id}/
DELETE  /api/v1/projects/{id}/
```

### Memberships

```
GET     /api/v1/projects/{project_id}/membership/
POST    /api/v1/projects/{project_id}/membership/
GET     /api/v1/projects/{project_id}/membership/{id}/
PUT     /api/v1/projects/{project_id}/membership/{id}/
DELETE  /api/v1/projects/{project_id}/membership/{id}/
```

### Tasks

```
GET     /api/v1/projects/{project_id}/tasks/
POST    /api/v1/projects/{project_id}/tasks/
GET     /api/v1/projects/{project_id}/tasks/{id}/
PUT     /api/v1/projects/{project_id}/tasks/{id}/
DELETE  /api/v1/projects/{project_id}/tasks/{id}/
```

### Activity Logs

```
GET     /api/v1/activity-logs/
GET     /api/v1/activity-logs/{id}/
```

---

## Filtering / Search / Ordering

Examples:

```
/api/v1/tasks/?status=todo
/api/v1/tasks/?search=backend
/api/v1/tasks/?ordering=created_at
```

---

## Future Improvements

* Comments system
* Notifications
* File upload system
* Redis caching layer
* WebSockets
* CI/CD pipeline
* Production deployment
* Frontend integration


