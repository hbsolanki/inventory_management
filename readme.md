# Inventory Management

## Project Goal

A small Django-based inventory management API for tracking users, products, and inventory transactions (stock in / stock out) with simple user profile support and media (profile pictures).

## Requirements

- Python 3.8+
- pip
- (Optional) virtualenv or venv

Installation dependencies are listed in `requirements.txt`.

## Quick Start

1. Create and activate a virtual environment

```bash
python3 -m venv env
source env/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Prepare the database

```bash
python manage.py migrate
python manage.py createsuperuser  # optional
```

4. Run the development server

```bash
python manage.py runserver
```

By default the project uses `db.sqlite3` in the project root.

## Media

Profile pictures are stored under the `media/profile_picture/` directory.

## API Endpoints (overview)

The project exposes REST-style endpoints for the main resources. Exact paths and available fields can be found in the apps' `urls.py`, views and serializers.

- Authentication / Token

  - `POST /api/token/` — obtain access & refresh tokens
  - `POST /api/token/refresh/` — refresh access token
  - `POST /api/token/verify/` — verify token validity

- Users

  - `GET  /user/` — list users
  - `POST /user/` — create user
  - `GET  /user/<id>/` — retrieve user
  - `PUT/PATCH /user/<id>/` — update user

- Products

  - `GET  /product/` — list products
  - `POST /product/` — create product
  - `GET  /product/<id>/` — retrieve product
  - `PUT/PATCH /product/<id>/` — update product

- Inventory Transactions
  - `GET  /inventory-transaction/` — list transactions
  - `POST /inventory-transaction/` — create transaction (stock in / out)
  - `GET  /inventory-transaction/<id>/` — retrieve transaction

Note: Inspect `inventory_management/urls.py` and each app's `urls.py` for the exact endpoint details.

## Useful Files

- `manage.py` — Django CLI entrypoint
- `db.sqlite3` — default SQLite database file (created after migration)
- `requirements.txt` — Python dependencies

## Next steps / Troubleshooting

- If you get import errors, ensure the virtual environment is activated and `requirements.txt` installed.
- To see registered routes, use `python manage.py show_urls` if you have `django-extensions` installed, or inspect `inventory_management/urls.py` and the apps' `urls.py` files.

If you'd like, I can run migrations or start the dev server for you, or generate a more detailed API reference with concrete request/response examples.
