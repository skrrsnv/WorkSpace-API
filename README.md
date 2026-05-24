# WorkSpace API

A backend API for team and project management built with Django REST Framework.

---

## Features

* JWT Authentication
* Custom User Model
* Project Management
* Role-based Permissions
* Membership System
* Task Management
* Activity Logs
* Filtering, Searching, and Ordering
* Swagger / ReDoc API Documentation
* Dockerized Environment
* PostgreSQL Database
* Asynchronous Tasks with Celery + Redis

---

## Tech Stack

* Python
* Django
* Django REST Framework
* PostgreSQL
* Redis
* Celery
* Docker & Docker Compose
* Poetry
* Simple JWT
* drf-spectacular
* django-filter

---

## Async Tasks & Activity Logs

The project uses Celery and Redis for asynchronous background processing.

### Implemented async features

* Activity log creation
* Background task execution
* Redis as message broker
* Scalable task queue architecture

### Example logged events

* Project creation
* Project update
* Project deletion
* Task creation
* Task update
* Membership creation
* Membership role updates

---

## Roles

The system supports three project roles:

* Owner
* Admin
* Member

---

## Permissions

### Owner

* Full project access
* Can delete projects
* Can manage memberships
* Can update and delete tasks

### Admin

* Can manage memberships
* Can update tasks

### Member

* Can view project data
* Can create tasks

---

## Project Structure

```text
apps/
├── activity_logs/
├── projects/
├── tasks/
├── users/

config/
```

---

## Installation

### Clone Repository

```bash
git clone <your-repository-url>
cd WorkSpace
```

---

## Environment Variables

Create a `.env` file in the root directory:

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

### Build Containers

```bash
docker compose build
```

### Start Project

```bash
docker compose up
```

### Apply Migrations

```bash
docker compose exec web python manage.py migrate
```

### Create Superuser

```bash
docker compose exec web python manage.py createsuperuser
```

Celery worker runs automatically as a separate Docker service.

---

## Local Development with Poetry

### Install Dependencies

```bash
poetry install
```

### Activate Shell

```bash
poetry shell
```

### Run Server

```bash
python manage.py runserver
```

---

## API Documentation

### Swagger UI

```text
http://127.0.0.1:8000/api/schema/swagger-ui/
```

### ReDoc

```text
http://127.0.0.1:8000/api/redoc/
```

---

## Authentication

JWT authentication is used.

### Obtain Token

```text
POST /api/v1/token/
```

### Refresh Token

```text
POST /api/v1/token/refresh/
```

---

## Main Endpoints

### Projects

```text
GET     /api/v1/projects/
POST    /api/v1/projects/
GET     /api/v1/projects/{id}/
PUT     /api/v1/projects/{id}/
DELETE  /api/v1/projects/{id}/
```

### Memberships

```text
GET     /api/v1/projects/{project_id}/membership/
POST    /api/v1/projects/{project_id}/membership/
GET     /api/v1/projects/{project_id}/membership/{id}/
PUT     /api/v1/projects/{project_id}/membership/{id}/
DELETE  /api/v1/projects/{project_id}/membership/{id}/
```

### Tasks

```text
GET     /api/v1/projects/{project_id}/tasks/
POST    /api/v1/projects/{project_id}/tasks/
GET     /api/v1/projects/{project_id}/tasks/{id}/
PUT     /api/v1/projects/{project_id}/tasks/{id}/
DELETE  /api/v1/projects/{project_id}/tasks/{id}/
```

### Activity Logs

```text
GET     /api/v1/activity-logs/
GET     /api/v1/activity-logs/{id}/
```

---

## Filtering, Searching, Ordering

Implemented with `django-filter`.

### Examples

```text
/api/v1/tasks/?status=todo
/api/v1/tasks/?search=backend
/api/v1/tasks/?ordering=created_at
```

---

## Future Improvements

* Automated Tests
* Comments System
* Notifications
* File Uploads
* Redis Caching Layer
* WebSockets
* Frontend Integration
* CI/CD Pipeline
* Production Deployment
