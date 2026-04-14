from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

# Create your models here.
class Genre(models.Model):
    """Book genre/category"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        
class Author(models.Model):
    """Book author"""
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    birth_year = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1000), MaxValueValidator(datetime.now().year)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        

class Book(models.Model):
    """Book with authors and genres"""
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    authors = models.ManyToManyField(Author, related_name='books')
    genres = models.ManyToManyField(Genre, related_name='books') 
    published_year = models.IntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(datetime.now().year)]
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    pages = models.IntegerField(default=0, validators=[MinValueValidator(1)])
    isbn = models.CharField(max_length=13, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_year', 'title']