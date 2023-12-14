from django.shortcuts import render
from django.views.generic import ListView, DetailView # to display lists and details
from .models import Book                              # to access the Book model

# Create your views here.
class BookListView(ListView):                         # ListView is a class-based view
    model = Book                                      # specify model
    template_name = 'books/main.html'                 # specify template

class BookDetailView(DetailView):                     # DetailView is a class-based view
    model = Book                                      # specify model
    template_name = 'books/detail.html'               # specify template
