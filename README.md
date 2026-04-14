# Django ORM Project

## 1) All types of views and how they work

This project uses Django function-based views in `books/views.py`.

- `all_genres(request)`
  - Returns all `Genre` objects from the database.
  - Serializes them into JSON-friendly dictionaries.
  - Uses `Genre.objects.all()`.

- `all_authors(request)`
  - Returns all `Author` objects.
  - Uses `Author.objects.all()`.
  - Serializes author fields like `id`, `first_name`, `email`, `bio`, and `birth_year`.

- `all_books(request)`
  - Returns all `Book` objects.
  - Uses `Book.objects.all()`.
  - Serializes book data and both ManyToMany relations: authors and genres.

- `books_by_author(request, author_id)`
  - Queries a single author by `id` with `Author.objects.get(id=author_id)`.
  - If the author does not exist, returns a 404 JSON error.
  - Otherwise returns books for that author via `author.books.all()`.

- `books_by_author_name(request, author_name)`
  - Uses `Author.objects.filter(first_name__icontains=author_name)` to search by partial author name.
  - If no authors match, returns a 404 JSON error.
  - Returns all books linked to matching authors, using `.distinct()` to avoid duplicates.

- `authors_by_book_id(request, book_id)`
  - Queries a single book by `id` with `Book.objects.get(id=book_id)`.
  - If the book does not exist, returns a 404 JSON error.
  - Returns all authors linked to that book via `book.author.all()`.

- `authors_by_book_name(request, book_name)`
  - Uses `Book.objects.filter(title__icontains=book_name)` to search by partial title.
  - Returns authors linked to matching books.

- `books_by_genre_name(request, genre_name)`
  - Uses `Genre.objects.filter(name__icontains=genre_name)` to search by partial genre name.
  - Returns all books associated with matching genres.

- `books_by_multiple_genres(request)`
  - Reads a comma-separated `genres` query parameter.
  - Filters using `Genre.objects.filter(name__in=genre_names)`.
  - Returns books belonging to any of the selected genres.

- `books_by_price_range(request)`
  - Reads query parameters `min_price` and/or `max_price`.
  - Applies `price__gte` and/or `price__lte` filters.
  - Returns all books within that price range.

## 2) Full codebase explanation

### Root files

- `manage.py`
  - Django command-line utility for running the project, migrations, development server, and management commands.

- `db.sqlite3`
  - SQLite database file used for storing app data during development.

- `README.md`
  - This file explaining views and the codebase.

### `config/` directory

Contains project settings and URL configuration.

- `config/settings.py`
  - Django project settings.
  - Registers the `books` app in `INSTALLED_APPS`.
  - Configures the SQLite database.
  - Sets middleware and template configuration.

- `config/urls.py`
  - Defines URL routing for the project.
  - Includes app URL patterns from `books/urls.py`.

- `config/asgi.py` and `config/wsgi.py`
  - ASGI and WSGI entry points for deploying the Django app.

### `books/` app

This is the main Django application for book data.

- `models.py`
  - Defines `Genre`, `Author`, and `Book` models.
  - `Book` has ManyToMany relationships to `Author` and `Genre`.
  - Additional through tables may exist for relationship handling.

- `views.py`
  - Contains all HTTP views that return JSON responses.
  - Includes serializers for genres, authors, and books.
  - Handles search, filtering, and relationship queries.

- `urls.py`
  - Maps API endpoints to view functions.
  - Defines routes for genre, author, book, price range, and relationship-based endpoints.

- `fixtures/`
  - JSON data files for seeding the database.
  - Includes author, genre, book, and join data files.

- `migrations/`
  - Auto-generated migration files to manage database schema changes.

- `admin.py`
  - Registers models for the Django admin site.

### Additional imported repository content

- `books_from_github/`
  - A copy of the `books` directory imported from an external example repository.
  - Contains duplicate model and fixture files from the source repo.

### Notes

- Views return `JsonResponse` objects so endpoints can be consumed by APIs.
- Serialization is handled manually in `views.py` to ensure related objects can be included cleanly.
- The project is configured to run in a local development environment with SQLite.
- Query filters use Django ORM lookups like `__icontains`, `__gte`, `__lte`, and `__in`.
