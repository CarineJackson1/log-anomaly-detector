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

## Getting Started

### Backend Setup

1. **Create and Activate Virtual Environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Mac/Linux

2. Upgrade pip (Recommended)

   bash
   Copy
   Edit
   python -m pip install --upgrade pip

3. Install Dependencies

   bash
   Copy
   Edit
   pip install -r requirements.txt

4. Setup Environment Variables

   bash
   Copy
   Edit
   cp .env.example .env

5. Initialize Database and Run Migrations

   bash
   Copy
   Edit
   alembic upgrade head

6. Run the Backend

   bash
   Copy
   Edit
   python app.py

7. Verify Healthcheck

   - General Healthcheck: [http://localhost:5000/healthcheck/](http://localhost:5000/healthcheck/)
   - Database Tables: [http://localhost:5000/db-check](http://localhost:5000/db-check/)  
     (should display `["alembic_version", "users"]` after migration)
   - Auth Routes Status: [http://localhost:5000/auth/status](http://localhost:5000/auth/status)  
     (should return `{"success": true, "data": {"auth_status": "ready"}, "message": "Authentication routes are live and responding."}`)

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

## Project Documentation
- [PRD in Notion](https://www.notion.so/codingtemple/AstroSkill-PRD-Participants-237d15b03f0a800eae76e41e8c09ffac?source=copy_link)
- [Team workspace](https://app.slack.com/client/T1HU6FJFK/C096YMLG8A2)
- [GITFLOW.md](https://github.com/AstroSkill/astroskill-lms-connector/blob/main/GITFLOW.md)

## Team Communication
- **Daily Standups:** Tuesdays, 1pm CT / 2pm EST  
- **Sprint Reviews:** Mondays, Wednesdays, Fridays at 6pm EST  
- **Team Chat:** [Slack](https://app.slack.com/client/T1HU6FJFK/C096YMLG8A2) / [Discord](https://discord.com/channels/1396991822990938244/1396991824006090935)
