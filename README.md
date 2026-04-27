# Test Site: Django + HTMX

Requires:

- Python with Django installed: https://docs.djangoproject.com/en/6.0/intro/install
- A running copy of the database: https://github.com/FrameworkBenchFullStack-RepPack/database-seed

## Initial setup:

Create a virtual environment:
```sh
python3 -m venv django-venv
```

The command starts with either `python3` or `python` depending on how python was installed.

Activate the virtual environment: 

```sh
source django-venv/bin/activate
```

Open the project folder:
```sh
cd django
```

Install dependencies:

```sh
pip install -r requirements.txt
```

## Build and run:

Do this when you need to run the server for benchmarking purposes.

Activate the virtual environment: 

```sh
source django-venv/bin/activate
```

Open the project folder:
```sh
cd django
```

Run server:

```sh
DATABASE_URL=postgresql://benchmark:benchmark@localhost:5432/benchmark PORT=8000 daphne test_site.asgi:application
```

When server is ready, it logs:

```sh
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

## Run test-server for development:

Do this if you need a quick preview of the website, or are actively working on it.

Activate the virtual environment: 

```sh
source django-venv/bin/activate
```

Open the project folder:
```sh
cd django
```

Add a `.env` file in this folder that points to the database:

```
DATABASE_URL=postgresql://benchmark:benchmark@localhost:5432/benchmark
```

Run the development server:

```sh
python3 manage.py runserver
```
The command starts with either `python3` or `python` depending on how python was installed.
