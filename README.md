# 🧾 Inventory Management System (FastAPI + SQLite + JWT)

A modular FastAPI-based backend for an **Inventory Management System** consisting of:

* **Auth Service** → User registration and JWT-based login
* **Product Service** → CRUD operations for products with category and pagination
* **Inventory Service** → Track product stock levels across warehouses

Built with **FastAPI**, **SQLAlchemy**, **SQLite**, and **Docker**.

---

## 🏗️ Project Architecture

```
inventory_management/
├── docker-compose.yml
├── .env
├── data/                      # Shared SQLite DB (via Docker volume)
└── services/
    ├── auth_service/
    │   ├── app/
    │   │   ├── main.py
    │   │   ├── routers.py
    │   │   ├── database.py
    │   │   ├── models.py
    │   │   ├── schemas.py
    │   │   └── crud.py
    │   ├── Dockerfile
    │   └── requirements.txt
    ├── product_service/
    │   ├── app/
    │   │   ├── main.py
    │   │   ├── routers.py
    │   │   ├── database.py
    │   │   ├── models.py
    │   │   ├── schemas.py
    │   │   └── crud.py
    │   ├── Dockerfile
    │   └── requirements.txt
    └── inventory_service/
    │   ├── app/
    │   │   ├── main.py
    │   │   ├── routers.py
    │   │   ├── database.py
    │   │   ├── models.py
    │   │   ├── schemas.py
    │   │   └── crud.py
    │   ├── Dockerfile
    │   └── requirements.txt
    │ -- README.md
```

Each service runs independently and communicates only via JWT (no internal HTTP calls).

---

## ⚙️ Environment Variables (`.env`)

```bash
JWT_SECRET=supersecretkey123
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=sqlite:////data/db.sqlite
```

> For local runs (not Docker), use `DATABASE_URL=sqlite:///./data/db.sqlite`.

---

## 🚀 Running the Project

### 🐳 Using Docker (recommended)

Build and start all services:

```bash
docker compose up --build
```

* Auth Service → [http://localhost:8000](http://localhost:800)
* Product Service → [http://localhost:8002](http://localhost:8002)
* Inventory Service → [http://localhost:8003](http://localhost:8003)

Each service includes built-in Swagger docs at `/docs`.

---

### 🧩 Running Locally (without Docker)

1. Create a virtual environment in each service folder:

   ```bash
   cd services/auth_service
   python -m venv .venv
   .venv\Scripts\activate  # (on Windows)
   pip install -r requirements.txt
   ```

2. Ensure `data/` folder exists at project root:

   ```bash
   mkdir ../../data
   ```

3. Run the service:

   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

4. Repeat steps for `product_service` and `inventory_service`, using ports **8002** and **8003**.

---

## 🔑 API Overview

### Auth Service (`:8000`)

| Endpoint         | Method | Description             |
| ---------------- | ------ | ----------------------- |
| `/auth/register` | POST   | Register a new user     |
| `/auth/login`    | POST   | Login and get JWT token |

**Example:**

```bash
curl -X POST http://localhost:8000/auth/register \
 -H "Content-Type: application/json" \
 -d '{"username":"alice","password":"secret"}'
```

Login to get a token:

```bash
curl -X POST http://localhost:8000/auth/login \
 -H "Content-Type: application/json" \
 -d '{"username":"alice","password":"secret"}'
```

---

### Product Service (`:8002`)

| Endpoint             | Method | Description                                          |
| -------------------- | ------ | ---------------------------------------------------- |
| `/api/products`      | POST   | Create product                                       |
| `/api/products`      | GET    | List products (pagination, optional category filter) |
| `/api/products/{id}` | GET    | Get product by ID                                    |
| `/api/products/{id}` | PUT    | Update product                                       |
| `/api/products/{id}` | DELETE | Delete product                                       |

**Example:**

```bash
curl -X POST http://localhost:8002/api/products \
 -H "Authorization: Bearer <token>" \
 -H "Content-Type: application/json" \
 -d '{"name":"Widget","description":"A widget","price":9.99,"category":"gadgets"}'
```

---

### Inventory Service (`:8003`)

| Endpoint                             | Method | Description                          |
| ------------------------------------ | ------ | ------------------------------------ |
| `/api/inventory`                     | POST   | Add or update stock quantity         |
| `/api/inventory/{product_id}`        | GET    | Get stock for a product              |
| `/api/inventory/adjust/{product_id}` | POST   | Adjust stock (add/subtract quantity) |

**Example:**

```bash
curl -X POST http://localhost:8003/api/inventory \
 -H "Authorization: Bearer <token>" \
 -H "Content-Type: application/json" \
 -d '{"product_id":1,"quantity":100,"warehouse":"W1"}'
```

---

## 🧠 Testing

You can add **pytest** tests under each service (e.g. `tests/test_auth.py`) and run:

```bash
pytest
```

Example simple test:

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["service"] == "auth"
```

---

## 🪣 Common Issues

| Issue                                                    | Solution                                                  |
| -------------------------------------------------------- | --------------------------------------------------------- |
| `ModuleNotFoundError: No module named 'routers'`         | Add `__init__.py` inside the `app` folder                 |
| `attempted relative import with no known parent package` | Run with `uvicorn app.main:app` **from the service root** |
| Database not found                                       | Ensure `data/` folder exists before running               |

---

## 🧩 Next Steps

* Add role-based permissions (Admin / Staff / Viewer)
* Switch SQLite → PostgreSQL for production
* Add Redis caching for product list
* Implement Alembic migrations
* Add Prometheus metrics or middleware for monitoring
* Configure CI/CD with GitHub Actions

---

## 👨‍💻 Author

Developed by **Nilesh** for the Whitestorksoft Python Practical Assignment
Tech Stack: **FastAPI**, **SQLAlchemy**, **SQLite**, **Docker**, **JWT Auth**

---
