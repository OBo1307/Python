from django.shortcuts import render
from django.views.generic import ListView, DetailView # to display lists and details
from .models import Book                              # to access the Book model
from django.contrib.auth.mixins import LoginRequiredMixin #to protect class-based view

# Create your views here.
class BookListView(LoginRequiredMixin, ListView):                         # ListView is a class-based "protected" view
    model = Book                                      # specify model
    template_name = 'books/main.html'                 # specify template

class BookDetailView(LoginRequiredMixin, DetailView):                     # DetailView is a class-based "protected" view
    model = Book                                      # specify model
    template_name = 'books/detail.html'               # specify template
