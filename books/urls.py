from django.urls import path
from . import views



app_name = 'books'

urlpatterns = [
    path('api/genres/', views.all_genres, name='all_genres'),
    path('api/authors/', views.all_authors, name='all_authors'),
    path('api/books/', views.all_books, name='all_books'),
    path('api/authors/<int:author_id>/', views.books_by_author, name='books_by_author'),
    path('api/authors/name/<str:author_name>/', views.books_by_author_name, name='books_by_author_name'),
    path('api/books/<int:book_id>/authors/', views.authors_by_book_id, name='authors_by_book_id'),
    path('api/books/name/<str:book_name>/authors/', views.authors_by_book_name, name='authors_by_book_name'),
    path('api/genres/name/<str:genre_name>/books/', views.books_by_genre_name, name='books_by_genre_name'),
    path('api/genres/multiple/', views.books_by_multiple_genres, name='books_by_multiple_genres'),
    path('api/books/price/', views.books_by_price_range, name='books_by_price_range'),
]
