from django.urls import path
from .views import (BookListView, BookDeleteView, BookCreateView, BookUpdateView,
                    DeleteReviewView, UpdateReviewView, BookDetailView, AddReviewView)

app_name = 'products'

urlpatterns = [
path('books/', BookListView.as_view(), name='book_list'),
    path('book_create/', BookCreateView.as_view(), name='book_create'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('book/<int:pk>/update/', BookUpdateView.as_view(), name='book_update'),
    path('book/<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),
]