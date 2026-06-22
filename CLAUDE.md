# CLAUDE.md

## Project Context

This is a full-stack web application called "DoMovie".

Backend:

* Django 5
* Django REST Framework
* PostgreSQL (Neon)
* JWT Authentication (SimpleJWT)

Frontend:

* HTML
* CSS
* Vanilla JavaScript (no frameworks)

---

## Goal

Build a simple movie and DVD ordering system.

* Admin manages directors, movies, and DVDs
* Users browse and place orders

Keep implementation simple and readable.

---

## Critical Rule About Output Length

* When generating FULL code (files, project structure):
  → DO NOT use caveman style
  → Output must be complete and explicit

* When answering explanations or debugging:
  → caveman style is allowed
  → Keep answers short and direct

* Never shorten code blocks

* Never omit required logic

---

## Rules

* Do not use any frontend frameworks
* Do not introduce unnecessary complexity
* Do not change project structure unless required
* Follow existing code patterns

---

## Authentication

* Use JWT (SimpleJWT)
* Store access token in localStorage
* Use header:

Authorization: Bearer <token>

* 401 → redirect to login

---

## User Roles

* admin
* user

Admin:

* Full CRUD on Director, Movie, DVD

User:

* Read-only content
* Create orders
* View own orders only

---

## Business Logic

Order creation must:

* Validate stock
* Reduce stock
* Calculate total_price
* Create Order + OrderItems
* Use transaction.atomic

---

## API

Base: /api/

* /movies/
* /directors/
* /dvds/
* /orders/
* /auth/register/
* /auth/login/
* /auth/refresh/

---

## Frontend Rules

* HTML + CSS + Vanilla JS only
* Use fetch API
* Store token in localStorage
* Store cart in localStorage

Cart:
[
{ "dvd": number, "quantity": number }
]

---

## Code Quality

* Use DRF ViewSets
* Use serializers properly
* No business logic in views
* Keep code readable

---

## Deployment

* Render compatible
* Use env vars:

  * SECRET_KEY
  * DATABASE_URL
  * DEBUG

---

## When unsure

* Ask before coding
* Do not guess
