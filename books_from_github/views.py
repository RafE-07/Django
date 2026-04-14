from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Book, Author, Genre
# Create your views here.

def serialize_genre(genre):
    """Helper to serialize a genre object"""
    return {
        'id': genre.id,
        'name': genre.name,
        'description': genre.description,
    }

def serialize_author(author):
    """Helper to serialize an author object"""
    return {
        'id': author.id,
        'name': author.name,
        'email': author.email,
        'birth_year': author.birth_year,
        'bio': author.bio,
    }
    
def serialize_book(book):
    """Helper to serialize a book object"""
    return {
        'id': book.id,
        'title': book.title,
        'price': float(book.price),
        'published_year': book.published_year,
        'pages': book.pages,
        'isbn': book.isbn,
        'authors': [{'id': a.id, 'name': a.name} for a in book.authors.all()],
        # 'authors': [serialize_author(a) for a in book.authors.all()],
        'genres': [{'id': g.id, 'name': g.name} for g in book.genres.all()],
        # 'genres': [serialize_genre(g) for g in book.genres.all()],
    }

@require_http_methods(["GET"])
def all_genres(request):
    genres = Genre.objects.all()
    return JsonResponse({
        "count":genres.count(),
        "genres":[serialize_genre(g) for g in genres]
    })
    
@require_http_methods(["GET"])
def all_authors(request):
    """Get all authors"""
    authors = Author.objects.all()
    return JsonResponse({
        'count': authors.count(),
        'authors': [serialize_author(a) for a in authors]
    })
    
@require_http_methods(["GET"])
def all_books(request):
    """Get all books"""
    books = Book.objects.all()
    return JsonResponse({
        'count': books.count(),
        'books': [serialize_book(b) for b in books]
    })
    
@require_http_methods(["GET"])
def books_by_author(request, author_id):
    try:
        author = Author.objects.get(id=author_id)
        books = author.books.all()
        return JsonResponse({
            'author': serialize_author(author),
            'books_count': books.count(),
            'books': [serialize_book(b) for b in books]
        })
    except Author.DoesNotExist:
        return JsonResponse({'error': 'Author not found'}, status=404)

@require_http_methods(["GET"])
def books_by_author_name(request, author_name):
    """Find books by author name (partial match)"""
    authors = Author.objects.filter(name__icontains=author_name) #(title__istartswith=letter)
    books = Book.objects.filter(authors__in=authors).distinct()
    return JsonResponse({
        'query': author_name,
        'authors_found': authors.count(),
        'books_count': books.count(),
        'books': [serialize_book(b) for b in books]
    })
    
@require_http_methods(["GET"])
def authors_by_book(request, book_id):
    """Find authors of a specific book"""
    try:
        book = Book.objects.get(id=book_id)
        authors = book.authors.all()
        return JsonResponse({
            'book': serialize_book(book),
            'authors_count': authors.count(),
            'authors': [serialize_author(a) for a in authors]
        })
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)

@require_http_methods(["GET"])
def authors_by_book_title(request, book_title):
    """Find authors by book title (partial match)"""
    books = Book.objects.filter(title__icontains=book_title)
    authors = Author.objects.filter(books__in=books).distinct()
    return JsonResponse({
        'query': book_title,
        'books_found': books.count(),
        'authors_count': authors.count(),
        'authors': [serialize_author(a) for a in authors]
    })
    

@require_http_methods(["GET"])
def books_by_genre(request, genre_id):
    """Find books in a specific genre"""
    try:
        genre = Genre.objects.get(id=genre_id)
        books = genre.books.all()
        return JsonResponse({
            'genre': serialize_genre(genre),
            'books_count': books.count(),
            'books': [serialize_book(b) for b in books]
        })
    except Genre.DoesNotExist:
        return JsonResponse({'error': 'Genre not found'}, status=404)


@require_http_methods(["GET"])
def books_by_genre_name(request, genre_name):
    """Find books by genre name (partial match)"""
    genres = Genre.objects.filter(name__icontains=genre_name)
    books = Book.objects.filter(genres__in=genres).distinct()
    return JsonResponse({
        'query': genre_name,
        'genres_found': genres.count(),
        'books_count': books.count(),
        'books': [serialize_book(b) for b in books]
    })
    
@require_http_methods(["GET"])
def books_by_multiple_genres(request):
    genre_ids = [2,3]
    genres = Genre.objects.filter(id__in=genre_ids)
    books = Book.objects.filter(genres__in=genres).distinct()
    return JsonResponse({
        # 'query': genre_name,
        'genres_found': genres.count(),
        'books_count': books.count(),
        'books': [serialize_book(b) for b in books]
    })
    
@require_http_methods(["GET"])
def authors_by_genre(request, genre_id):
    """Find authors who write in a specific genre"""
    try:
        genre = Genre.objects.get(id=genre_id)
        authors = Author.objects.filter(books__genres=genre).distinct()
        return JsonResponse({
            'genre': serialize_genre(genre),
            'authors_count': authors.count(),
            'authors': [serialize_author(a) for a in authors]
        })
    except Genre.DoesNotExist:
        return JsonResponse({'error': 'Genre not found'}, status=404)
    
@require_http_methods(["GET"])
def books_by_year_range(request, year1, year2):
    """Find books published between year1 and year2"""
    year1, year2 = int(year1), int(year2)
    books = Book.objects.filter(published_year__gte=year1, published_year__lte=year2)
    return JsonResponse({
        'year_range': f'{year1}-{year2}',
        'books_count': books.count(),
        'books': [serialize_book(b) for b in books]
    })
    
# ============================================================================
# FINDING BY NAME PATTERNS
# ============================================================================

@require_http_methods(["GET"])
def books_by_title_starts_with(request, letter):
    """Find books whose title starts with a letter"""
    books = Book.objects.filter(title__istartswith=letter)
    return JsonResponse({
        'starts_with': letter,
        'books_count': books.count(),
        'books': [serialize_book(b) for b in books]
    })


@require_http_methods(["GET"])
def authors_by_name_starts_with(request, letter):
    """Find authors whose name starts with a letter"""
    authors = Author.objects.filter(name__istartswith=letter)
    return JsonResponse({
        'starts_with': letter,
        'authors_count': authors.count(),
        'authors': [serialize_author(a) for a in authors]
    })

# ============================================================================
# FINDING BOOKS BY PRICE RANGE
# ============================================================================

@require_http_methods(["GET"])
def books_by_price_range(request, price1, price2):
    """Find books in a price range"""
    price1, price2 = float(price1), float(price2)
    if price1 > price2:
        price1, price2 = price2, price1
    
    books = Book.objects.filter(price__gte=price1, price__lte=price2)
    return JsonResponse({
        'price_range': f'${price1}-${price2}',
        'books_count': books.count(),
        'books': [serialize_book(b) for b in books]
    })

# ============================================================================
# COMPLEX QUERY - ADVANCED FILTERING
# ============================================================================

@require_http_methods(["GET"])
def books_advanced_filter(request):
    """
    Advanced filtering: price range, genres, and published year
    Usage: /api/books/advanced-filter/?price_min=10&price_max=50&genres=1,2,3&year_min=2000&year_max=2024
    """
    try:
        # Get query parameters
        price_min = request.GET.get('price_min')
        price_max = request.GET.get('price_max')
        genres_str = request.GET.get('genres')
        year_min = request.GET.get('year_min')
        year_max = request.GET.get('year_max')
        
        # Start with all books
        query = Book.objects.all() #QuerySet
        filters = {}
        
        # Apply price filter
        if price_min and price_max:
            price_min, price_max = float(price_min), float(price_max)
            if price_min > price_max:
                price_min, price_max = price_max, price_min
            query = query.filter(price__gte=price_min, price__lte=price_max)
            filters['price_range'] = f'${price_min}-${price_max}'
        
        # Apply genre filter
        genres = []
        if genres_str:
            genre_ids = [int(g.strip()) for g in genres_str.split(',') if g.strip()]
            genres = Genre.objects.filter(id__in=genre_ids)
            if genres.exists():
                query = query.filter(genres__in=genres).distinct()
                filters['genres'] = [serialize_genre(g) for g in genres]
        
        # Apply year filter
        if year_min and year_max:
            year_min, year_max = int(year_min), int(year_max)
            if year_min > year_max:
                year_min, year_max = year_max, year_min
            query = query.filter(
                published_year__gte=year_min,
                published_year__lte=year_max
            )
            filters['year_range'] = f'{year_min}-{year_max}'
        
        books = query.distinct()
        
        return JsonResponse({
            'filters_applied': filters,
            'books_count': books.count(),
            'books': [serialize_book(b) for b in books]
        })
    except (ValueError, TypeError) as e:
        return JsonResponse({'error': f'Invalid parameters: {str(e)}'}, status=400)
