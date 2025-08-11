# Astroskill LMS Connector

## Project Overview
AstroSkill LMS Connector is a full-stack platform that bridges the gap between Moodle course completion and aerospace employer recruitment. It enables the tracking of learner progress and the matching of qualified candidates with hiring organizations in the aerospace sector.

## Team Members & Roles
- **Geoffrey Burt** – Backend Software Engineer  
- **Marcquez Tookes** – Backend Software Engineer  
- **Damon Dixon** – Frontend Software Engineer  
- **Josh Canterbury** – Frontend Software Engineer  
- **Key'n Brosdahl** – Frontend Software Engineer  
- **Carine Jackson** – Cybersecurity Specialist  
- **Sajana Maharjan** – Cybersecurity Specialist  

## Tech Stack
- **Frontend:** React.js or Next.js + Tailwind CSS  
- **Backend:** Python Flask / FastAPI  
- **Database:** PostgreSQL (hosted)  
- **Authentication:** Firebase Auth or Flask-JWT  
- **Moodle Integration:** REST API calls  
- **Matching Logic:** Backend Python logic  
- **Deployment:** Netlify (frontend) + Render/Railway (backend)  
- **Monitoring:** Basic error logging + health checks  

---

## 📄 New Schemas & Models

This update introduces three new backend schemas with Marshmallow validation for serialization and deserialization.

### **LearnerProfileSchema**
- **Purpose:** Stores learner skills and resume URL.
- **Key Fields:**
  - `user_id` *(required, int)*
  - `skills` *(required, list of strings, unique, case-insensitive)*
  - `resume_url` *(required, valid HTTP/HTTPS URL)*
- **Validation:** Prevents blank skills and duplicate entries (case-insensitive).
- **Model:** `LearnerProfile` — auto-created via `@post_load`.

### **EmployerSchema**
- **Purpose:** Stores employer company details and interest tags.
- **Key Fields:**
  - `user_id` *(required, int)*
  - `company_name` *(required, string, 1–500 chars)*
  - `interest_tags` *(optional, list of unique strings)*
- **Validation:** Prevents blank tags, trims whitespace, enforces uniqueness.

### **CourseProgressSchema**
- **Purpose:** Tracks learner progress through courses.
- **Key Fields:**
  - `user_id` *(required, int)*
  - `course_id` *(required, int)*
  - `completion_status` *(enum: NOT_STARTED, IN_PROGRESS, COMPLETED)*
- **Validation:** Enum must match defined `CompletionStatus` values.

---

## Getting Started

### Backend Setup

1. **Create and Activate Virtual Environment**
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Mac/Linux

2. Upgrade pip (Recommended)

   python -m pip install --upgrade pip

3. Install Dependencies

   pip install -r requirements.txt

4. Setup Environment Variables

   cp .env.example .env

5. Initialize Database and Run Migrations

   alembic upgrade head

6. Run the Backend

   python app.py

7. Verify Healthcheck

   - General Healthcheck: [http://localhost:5000/healthcheck/](http://localhost:5000/healthcheck/)
   - Database Tables: [http://localhost:5000/db-check](http://localhost:5000/db-check/)  
     (should display `[
        "alembic_version",
        "applications",
        "course_progress",
        "courses",
        "employers",
        "enrollments",
        "job_postings",
        "learner_profiles",
        "matching_data",
        "users"
      ]` after migration)
   
   - Auth Routes Status: [http://localhost:5000/auth/status](http://localhost:5000/auth/status)  
     (should return `{"success": true, 
                      "data": {"auth_status": "ready"},  
                      "message": "Authentication routes are live and responding."}`)

---

📂 Core Database Tables
Table Name	        Purpose
users	              Stores authentication credentials and role info for all platform users.
learner_profiles	  Links to users and contains skills, resumes, and learner-specific data.
courses	            Holds course metadata (title, description, source). Can be from Moodle or internal.
enrollments	        Tracks learner participation in courses, progress, and status.
course_progress	    Fine-grained progress tracking for each learner per course.
employers	          Employer organization details.
job_postings	      Job listings from aerospace employers.
applications	      Applications learners submit for job postings.
matching_data	      AI or logic-generated matches between learners and job postings.
alembic_version	    Tracks Alembic migration state.

---

📌 Database Migrations with Alembic
Alembic is used for managing changes to the database schema. It allows you to safely evolve the database without losing existing data.

How It Works
Models in backend/models define the database tables.

Alembic compares these models to the actual database to detect differences.

When a model is added, removed, or modified, you generate a migration script.

Migrations are then applied to bring the database up to date.

### Adding a New Migration

When modifying database models:

1. **Generate migration script**
   ```bash
   alembic revision --autogenerate -m "Describe changes"
   ```
2. **Apply migration**
   ```bash
   alembic upgrade head
   ```
3. **Verify migration**
   ```python
   from app import create_app
   from database import db

   app = create_app()
   with app.app_context():
       print("Tables:", db.inspect(db.engine).get_table_names())
   ```

---

## Development Workflow

To ensure consistent and smooth collaboration:

### 1. Branching Strategy
- **Main branches:**
  - `main` → Production-ready code
  - `develop` → Latest tested development code
- **Feature branches:**
  - Create a new branch for each feature or bug fix:
    ```bash
    git checkout develop
    git pull origin develop
    git checkout -b feature/<short-description>
    ```
  - Example: `feature/backend-db-init-user-model`

### 2. Committing Changes
- Commit small, logical changes frequently:
  ```bash
  git add .
  git commit -m "Implement user model and Alembic migration"
  ```

### 3. Pushing and Pull Requests
- Push your branch:
  ```bash
  git push origin feature/<short-description>
  ```
- Open a Pull Request (PR) to `develop`.
- Tag the relevant reviewer and wait for approval before merging.

### 4. Code Review
- Reviews ensure code quality and prevent merge conflicts.
- All PRs must pass:
  - Unit tests
  - Integration tests
  - Manual verification (if applicable)

### 5. Merging
- Only merge after approval.
- Squash commits if necessary to keep history clean.

### 6. Syncing Changes
- Frequently pull updates to stay aligned:
  ```bash
  git checkout develop
  git pull origin develop
  ```

---

## 🔑 Authentication Endpoints

| Method | Endpoint       | Description                        | Auth Required |
|--------|---------------|------------------------------------|---------------|
| POST   | `/auth/register` | Register a new user                 | ❌             |
| POST   | `/auth/login`    | Authenticate and receive JWT token  | ❌             |
| GET    | `/auth/me`       | Get details of the current user     | ✅             |
| GET    | `/auth/status`   | Health check for auth routes        | ❌             |

---

## 🧪 Testing the Authentication API with POSTMAN

### 1. Register User
**POST** `/auth/register`  
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "Password123",
  "role": "admin"
}

Response:
{
  "status": "success",
  "message": "User registered successfully",
  "data": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "role": "admin",
    "created_at": "...",
    "updated_at": "..."
  }
}

2. Login
POST /auth/login
{
  "email": "john@example.com",
  "password": "Password123"
}
Response:
{
  "status": "success",
  "message": "Login successful",
  "data": {
    "access_token": "JWT_TOKEN_HERE",
    "user": { ... }
  }
}

3. Current User
GET /auth/me
Header: Authorization: Bearer JWT_TOKEN_HERE

Response: 
{
  "status": "success",
  "message": "User retrieved successfully",
  "data": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "role": "admin"
  }
}

---

🧪 Running Tests & Coverage Requirements
We use pytest for backend testing with coverage tracking.
The current coverage requirement is ≥80% for all authentication-related routes.

Running All Tests

pytest
Running Only Authentication Tests

pytest -k "auth or login or register"

Running Tests with Coverage Report

pytest --cov=backend --cov-report=term-missing

This will:

Run all tests in backend/tests/

Show which lines are covered or missed

Fail if coverage drops below the team-agreed threshold (set in pytest.ini)

Current Status (as of last PR):
✅ All authentication tests pass
✅ Overall backend coverage: 90%
✅ backend/routes/auth_routes.py coverage: 80% (meets requirement)

---

🛡 Role-Based Access Control (RBAC)
Role-Based Middleware has been implemented to protect sensitive routes based on a user’s role.
Each authenticated request includes the user’s role claim inside the JWT, which is checked before allowing access.

Available Roles
learner

employer

admin

Middleware Decorator
The @roles_required(*roles) decorator is used to secure routes.
Example:

python
from utils.auth_decorators import roles_required

@app.route('/admin/dashboard')
@roles_required('admin')
def admin_dashboard():
    return success_response({"message": "Welcome, admin!"})
Users without the required role(s) will receive 403 Forbidden.

Example Protected Route
python
@app.route('/reports')
@roles_required('admin', 'employer')
def view_reports():
    return success_response({"reports": []})
In this example, both admin and employer can access the /reports endpoint.

Testing RBAC with Postman
Login with a user that has the required role (e.g., admin) and copy the access_token.

Call the protected route with the header:

Authorization: Bearer <JWT_TOKEN>
Expected:

If you have the role → 200 OK

If you don’t have the role → 403 Forbidden

Example Response (403):

json
{
  "status": "error",
  "message": "You do not have permission to access this resource."
}

---

## Project Documentation
- [PRD in Notion](https://www.notion.so/codingtemple/AstroSkill-PRD-Participants-237d15b03f0a800eae76e41e8c09ffac?source=copy_link)
- [Team workspace](https://app.slack.com/client/T1HU6FJFK/C096YMLG8A2)
- [GITFLOW.md](https://github.com/AstroSkill/astroskill-lms-connector/blob/main/GITFLOW.md)

## Team Communication
- **Daily Standups:** Tuesdays, 1pm CT / 2pm EST  
- **Sprint Reviews:** Mondays, Wednesdays, Fridays at 6pm EST  
- **Team Chat:** [Slack](https://app.slack.com/client/T1HU6FJFK/C096YMLG8A2) / [Discord](https://discord.com/channels/1396991822990938244/1396991824006090935)
# Testing Full Scan
