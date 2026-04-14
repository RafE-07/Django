from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator 
from datetime import date   


# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True )
    description = models.TextField(blank=True)  
    created_at =models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Author(models.Model):
    first_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    birth_year = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(date.today().year)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name
    
    class Meta:
        ordering = ['first_name']        


class Book(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    author = models.ManyToManyField(Author, related_name='books', through='Book_Authors')
    genre = models.ManyToManyField(Genre, related_name='books', through='Book_Genres')
    published_year = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(date.today().year)])
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01)])
    pages = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    isbn = models.CharField(max_length=13, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-published_year', 'title']


class Book_Authors(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        db_table = 'books_book_authors'
        unique_together = [('book', 'author')]


class Book_Genres(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        db_table = 'books_book_genres'
        unique_together = [('book', 'genre')]
