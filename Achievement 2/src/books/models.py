from django.db import models
from django.shortcuts import reverse

# Create your models here.
genre_choice= (
    ('classic', 'Classic'),
    ('romantic', 'Romantic'),
    ('comic', 'Comic'),
    ('fantasy', 'Fantasy'),
    ('horror', 'Horror'),
    ('educational', 'Educational')
)
book_type_choices= (
    ('hardcover', 'Hardcover'),
    ('ebook', 'E-book'),
    ('audiob', 'Audiobook')
)
class Book(models.Model):
    name= models.CharField(max_length=120)
    genre= models.CharField(max_length=12, choices=genre_choice, default='classic')
    book_type= models.CharField(max_length=12, choices=book_type_choices, default='hardcover')
    price= models.FloatField(help_text='in US dollars $')
    author_name= models.CharField(max_length=120)
    pic= models.ImageField(upload_to='books', default='no_picture.jpg')

    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse ('books:detail', kwargs={'pk':self.pk})