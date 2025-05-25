# 🗓️ Event Management API

A fully-featured Django REST Framework API to manage calendar events with support for:

- User authentication (JWT)
- CRUD operations on events
- Event versioning (history, rollback, diff)
- Role-based event sharing (viewer, editor, owner)
- Swagger (OpenAPI) documentation

---

## 🔧 Technologies Used

- Python 3.11+
- Django 4.x
- Django REST Framework
- JWT Authentication (`djangorestframework-simplejwt`)
- Swagger docs (`drf-yasg`)
- PostgreSQL or SQLite (customizable)
- DeepDiff for version comparisons

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/event-management-api.git
cd event-management-api
````

### 2. Create a Virtual Environment

```bash
python -m venv env
source env/bin/activate  # Linux/macOS
env\Scripts\activate     # Windows
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py migrate
```

### 5. Create Superuser (optional)

```bash
python manage.py createsuperuser
```

### 6. Run Server

```bash
python manage.py runserver
```

---

## 📘 API Documentation

Swagger/OpenAPI docs are available at:

```
http://127.0.0.1:8000/swagger/
```

You can explore all endpoints, parameters, and example responses interactively.

---

## 🔐 Authentication

Uses **JWT tokens** for authentication.

* **Login**: `/api/login/`
* **Signup**: `/api/signup/`
* **Logout**: `/api/logout/`

Include JWT token in headers for protected endpoints:

```http
Authorization: Bearer <access_token>
```

---

## 📂 API Endpoints

### 🔑 Auth

| Endpoint       | Method | Description           |
| -------------- | ------ | --------------------- |
| `/api/signup/` | POST   | Create a user account |
| `/api/login/`  | POST   | Authenticate user     |
| `/api/logout/` | POST   | Blacklist JWT token   |

---

### 📅 Events

| Endpoint                    | Method | Description                  |
| --------------------------- | ------ | ---------------------------- |
| `/api/events/`              | GET    | List user-accessible events  |
| `/api/events/`              | POST   | Create a new event           |
| `/api/events/<id>/`         | GET    | Retrieve event by ID         |
| `/api/events/<id>/`         | PUT    | Update event with versioning |
| `/api/events/<id>/`         | DELETE | Delete an event              |
| `/api/events/batch-create/` | POST   | Bulk create multiple events  |

---

### 👥 Event Sharing & Permissions

| Endpoint                                 | Method | Description                      |
| ---------------------------------------- | ------ | -------------------------------- |
| `/api/events/<id>/share/`                | POST   | Share event with user & role     |
| `/api/events/<id>/permission/`           | GET    | Get your role in an event        |
| `/api/events/<id>/permission/<user_id>/` | PUT    | Update another user's permission |
| `/api/events/<id>/permission/<user_id>/` | DELETE | Remove user from shared event    |

---

### 🕒 Versioning & History

| Endpoint                                             | Method | Description                          |
| ---------------------------------------------------- | ------ | ------------------------------------ |
| `/api/events/<id>/changelog/`                        | GET    | Get change log (all versions)        |
| `/api/events/<id>/diff/<version1_id>/<version2_id>/` | GET    | Compare two versions                 |
| `/api/events/<id>/history/<version_id>/`             | GET    | Retrieve specific historical version |
| `/api/events/<id>/rollback/<version_id>/`            | POST   | Rollback event to a specific version |




---

## ✍️ Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss your ideas.

---

