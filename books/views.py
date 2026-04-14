from itertools import count

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods       
from.models import Book, Author, Genre

# Create your views here.

def serialize_genres(genres):
    """Serialize a queryset of Genre objects to a list of dictionaries."""
    return [
        {
            "id": genre.id,
            "name": genre.name,
            "description": genre.description,
            "created_at": genre.created_at.isoformat() if genre.created_at else None,
        }
        for genre in genres
    ]

def serialize_authors(authors):
    """Serialize a queryset of Author objects to a list of dictionaries."""
    return [
        {
            "id": author.id,
            "first_name": author.first_name,
            "email": author.email,
            "bio": author.bio,
            "birth_year": author.birth_year,
            "created_at": author.created_at.isoformat() if author.created_at else None,
        }
        for author in authors
    ]

def serialize_books(books):
    """Serialize a queryset of Book objects to a list of dictionaries.
    Handles both ManyToMany relationships: author and genre."""
    return [
        {
            "id": book.id,
            "title": book.title,
            "description": book.description,
            "published_year": book.published_year,
            "price": str(book.price),
            "pages": book.pages,
            "isbn": book.isbn,
            "authors": [
                {
                    "id": author.id,
                    "first_name": author.first_name,
                    "email": author.email,
                }
                for author in book.author.all()
            ],
            "genres": [
                {
                    "id": genre.id,
                    "name": genre.name,
                    "description": genre.description,
                }
                for genre in book.genre.all()
            ],
            "created_at": book.created_at.isoformat() if book.created_at else None,
        }
        for book in books
    ]

@require_http_methods(["GET"])
def all_genres(request):
    genres = Genre.objects.all()
    
    return JsonResponse({
        "count": genres.count(),
        "genres": serialize_genres(genres)
    })

@require_http_methods(["GET"])
def all_authors(request):
    authors = Author.objects.all()
    
    return JsonResponse({
        "count": authors.count(),
        "authors": serialize_authors(authors)
    })

@require_http_methods(["GET"])
def all_books(request):
    books = Book.objects.all()
    
    return JsonResponse({
        "count": books.count(),
        "books": serialize_books(books)
    })

@require_http_methods(["GET"])
def books_by_author(request, author_id):
    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        return JsonResponse({
            "error": f"Author with id {author_id} not found"
        }, status=404)
    except Exception as e:
        return JsonResponse({
            "error": f"An error occurred: {str(e)}"
        }, status=500)
    
    try:
        books = author.books.all()
        return JsonResponse({
            "author": {
                "id": author.id,
                "first_name": author.first_name,
                "email": author.email,
            },
            "count": books.count(),
            "books": serialize_books(books)
        })
    except Exception as e:
        return JsonResponse({
            "error": f"Error retrieving books: {str(e)}"
        }, status=500)

@require_http_methods(["GET"])
def books_by_author_name(request, author_name):
    try:
        authors = Author.objects.filter(first_name__icontains=author_name)
        if not authors.exists():
            return JsonResponse({
                "error": f"No authors found with name containing '{author_name}'"
            }, status=404)
    except Exception as e:
        return JsonResponse({
            "error": f"An error occurred: {str(e)}"
        }, status=500)
    
    try:
        books = Book.objects.filter(author__in=authors).distinct()
        return JsonResponse({
            "search_name": author_name,
            "authors_found": serialize_authors(authors),
            "total_authors": authors.count(),
            "total_books": books.count(),
            "books": serialize_books(books)
        })
    except Exception as e:
        return JsonResponse({
            "error": f"Error retrieving books: {str(e)}"
        }, status=500)

@require_http_methods(["GET"])
def authors_by_book_id(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return JsonResponse({
            "error": f"Book with id {book_id} not found"
        }, status=404)
    except Exception as e:
        return JsonResponse({
            "error": f"An error occurred: {str(e)}"
        }, status=500)
    
    try:
        authors = book.author.all()
        return JsonResponse({
            "book": {
                "id": book.id,
                "title": book.title,
                "isbn": book.isbn,
                "published_year": book.published_year,
            },
            "count": authors.count(),
            "authors": serialize_authors(authors)
        })
    except Exception as e:
        return JsonResponse({
            "error": f"Error retrieving authors: {str(e)}"
        }, status=500)

@require_http_methods(["GET"])
def authors_by_book_name(request, book_name):
    try:
        books = Book.objects.filter(title__icontains=book_name)
        if not books.exists():
            return JsonResponse({
                "error": f"No books found with title containing '{book_name}'"
            }, status=404)
    except Exception as e:
        return JsonResponse({
            "error": f"An error occurred: {str(e)}"
        }, status=500)
    
    try:
        authors = Author.objects.filter(books__in=books).distinct()
        return JsonResponse({
            "search_title": book_name,
            "books_found": serialize_books(books),
            "total_books": books.count(),
            "total_authors": authors.count(),
            "authors": serialize_authors(authors)
        })
    except Exception as e:
        return JsonResponse({
            "error": f"Error retrieving authors: {str(e)}"
        }, status=500)

@require_http_methods(["GET"])
def books_by_genre_name(request, genre_name):
    try:
        genres = Genre.objects.filter(name__icontains=genre_name)
        if not genres.exists():
            return JsonResponse({
                "error": f"No genres found with name containing '{genre_name}'"
            }, status=404)
    except Exception as e:
        return JsonResponse({
            "error": f"An error occurred: {str(e)}"
        }, status=500)
    
    try:
        books = Book.objects.filter(genre__in=genres).distinct()
        return JsonResponse({
            "search_genre": genre_name,
            "genres_found": serialize_genres(genres),
            "total_genres": genres.count(),
            "total_books": books.count(),
            "books": serialize_books(books)
        })
    except Exception as e:
        return JsonResponse({
            "error": f"Error retrieving books: {str(e)}"
        }, status=500)

@require_http_methods(["GET"])
def books_by_multiple_genres(request):
    try:
        # Get comma-separated genre names from query parameter
        genre_names_param = request.GET.get('genres', '')
        if not genre_names_param:
            return JsonResponse({
                "error": "Please provide genre names in query parameter: ?genres=genre1,genre2,genre3"
            }, status=400)
        
        genre_names = [g.strip() for g in genre_names_param.split(',')]
        genres = Genre.objects.filter(name__in=genre_names)
        
        if not genres.exists():
            return JsonResponse({
                "error": f"No genres found matching: {genre_names}"
            }, status=404)
    except Exception as e:
        return JsonResponse({
            "error": f"An error occurred: {str(e)}"
        }, status=500)
    
    try:
        # Books that belong to any of the specified genres
        books = Book.objects.filter(genre__in=genres).distinct()
        return JsonResponse({
            "search_genres": genre_names,
            "genres_found": serialize_genres(genres),
            "total_genres": genres.count(),
            "total_books": books.count(),
            "books": serialize_books(books)
        })
    except Exception as e:
        return JsonResponse({
            "error": f"Error retrieving books: {str(e)}"
        }, status=500)

@require_http_methods(["GET"])
def books_by_price_range(request):
    try:
        # Get min and max price from query parameters
        min_price = request.GET.get('min_price', None)
        max_price = request.GET.get('max_price', None)
        
        if min_price is None and max_price is None:
            return JsonResponse({
                "error": "Please provide price range: ?min_price=10&max_price=50 or ?min_price=10 or ?max_price=50"
            }, status=400)
        
        # Convert to float and validate
        filters = {}
        if min_price is not None:
            min_price = float(min_price)
            filters['price__gte'] = min_price
        
        if max_price is not None:
            max_price = float(max_price)
            filters['price__lte'] = max_price
        
        books = Book.objects.filter(**filters)
        
        if not books.exists():
            return JsonResponse({
                "message": "No books found in the specified price range",
                "filters": filters,
                "count": 0,
                "books": []
            })
    except ValueError:
        return JsonResponse({
            "error": "min_price and max_price must be valid numbers"
        }, status=400)
    except Exception as e:
        return JsonResponse({
            "error": f"An error occurred: {str(e)}"
        }, status=500)
    
    try:
        return JsonResponse({
            "price_range": {
                "min_price": float(min_price) if min_price else None,
                "max_price": float(max_price) if max_price else None,
            },
            "total_books": books.count(),
            "books": serialize_books(books)
        })
    except Exception as e:
        return JsonResponse({
            "error": f"Error retrieving books: {str(e)}"
        }, status=500)
