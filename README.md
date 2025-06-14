# project-oop- Retail Management System Phase 1

This project now includes a small Flask API server and a React based user interface.

## Backend

Install Python dependencies and run the server:

```bash
pip install -r requirements.txt
python server.py
```

The server loads the store data from the `Store` directory and exposes two endpoints:

- `GET /api/products` – list all products.
- `POST /api/login` – login with JSON body `{"user_id": "<id>", "password": "<pass>"}`.

## Frontend

A minimal React application is located in the `frontend` directory. Install Node dependencies and start the development server:

```bash
cd frontend
npm install
npm start
```

The React app fetches product data from `http://localhost:5000/api/products` and displays it.
