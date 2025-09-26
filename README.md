# SIL Backend (Django)

## Overview

SIL Backend is a Django-based REST API that supports:

- Product and Category management
- Customer and Order management
- Google OAuth2 authentication for users
- Dockerized environment for easy setup
- CI/CD pipeline with testing and coverage

This backend is built to be secure, modular, and scalable.

---

## Features

- **Products & Categories:** CRUD operations, bulk create with nested categories
- **Orders:** Create orders with multiple items, calculate totals
- **Authentication:** Google Sign-In and JWT-based access control
- **Dockerized:** Run locally or in production with Docker Compose
- **CI/CD:** GitHub Actions for automated tests and Docker image deployment

---

## Setup / Local Development

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Git

### Clone the repository

- git clone https://github.com/josphat-otieno/sil-backend.git
- cd sil-backend

---

## Environment variables

### Create a .env file in the project root:
- DEBUG=1
- SECRET_KEY=your_secret_key
- ALLOWED_HOSTS=*
- TIME_ZONE=Africa/Nairobi
- POSTGRES_DB=django_db
- POSTGRES_USER=django_user
- POSTGRES_PASSWORD=django_password
- POSTGRES_HOST=db
- POSTGRES_PORT=5432
- AUTH_MODE=jwt
- AT_USERNAME=YOUR_AFRICASTALKING_USERNAME
- AT_API_KEY=YOUR_AFRICASTALKING_API_KEY
- AT_SENDER_ID=YOUR_AFRICASTALKING_SENDER_ID
- ADMIN_EMAIL=admin@example.com
- OIDC_ISSUER=https://accounts.google.com
- OIDC_CLIENT_ID=YOUR GOOGLE_AUTH_CLIENT_ID
- OIDC_CLIENT_SECRET=YOUR_GOOGLE_AUTH_CLIENT_SECRET
- OIDC_REDIRECT_URI=http://localhost:8001/api/auth/callback
- OIDC_SCOPES=openid,email,profile
- OIDC_AUDIENCE=http://localhost:8001/api/auth/callback

## Build and run with Docker
- docker compose up -d --build

### Create superuser
- docker compose run --rm web python manage.py createsuperuser

## Authentication via Google OAuth
###Obtain a Google Access Token
- Open the following `http://localhost:8001/api/auth/callback` in your browser and continue to Google.
- You will be redirected back to the browser after successful authentication. Copy the access token to 
- be use for authorizing other APIs

### Access Protected Endpoints
- curl -H "Authorization: Bearer <access_token>"   http://localhost:8001/api/products/

 Testing & Coverage
- docker compose run --rm web coverage run --source='.' manage.py test
- docker compose run --rm web coverage report -m
- docker compose run --rm web coverage html

```