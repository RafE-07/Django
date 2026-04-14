from django.urls import path
from . import views

app_name = "books"

urlpatterns = [
    path("api/genres/", views.all_genres),
    path("api/authors/", views.all_authors),
    path("api/books/", views.all_books),
    path('api/books/by-author/<int:author_id>/', views.books_by_author, name='books_by_author'),
    path('api/books/by-author-name/<str:author_name>/', views.books_by_author_name, name='books_by_author_name'),
    
    # Authors by books
    path('api/authors/by-book/<int:book_id>/', views.authors_by_book, name='authors_by_book'),
    path('api/authors/by-book-title/<str:book_title>/', views.authors_by_book_title, name='authors_by_book_title'),
    
    path('api/books/by-genre/<int:genre_id>/', views.books_by_genre, name='books_by_genre'),
    path('api/books/by-genre-name/<str:genre_name>/', views.books_by_genre_name, name='books_by_genre_name'),
    path('api/books/multiple-genres/', views.books_by_multiple_genres),
     # Authors by genres
    path('api/authors/by-genre/<int:genre_id>/', views.authors_by_genre, name='authors_by_genre'),
    
    # Books by year
    path('api/books/by-year/<int:year1>/<int:year2>/', views.books_by_year_range, name='books_by_year_range'),
    
    # Books by name pattern
    path('api/books/title-starts-with/<str:letter>/', views.books_by_title_starts_with, name='books_by_title_starts_with'),
    path('api/authors/name-starts-with/<str:letter>/', views.authors_by_name_starts_with, name='authors_by_name_starts_with'),
    
    # Books by price (using str converter)
    path('api/books/by-price/<str:price1>/<str:price2>/', views.books_by_price_range, name='books_by_price_range'),
    
    # Advanced filter
    path('api/books/advanced-filter/', views.books_advanced_filter, name='books_advanced_filter'),
    
]
