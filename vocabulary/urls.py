from django import forms
from django.contrib.auth.models import User
from django.urls import path
from . import views

urlpatterns = [
    # Đường dẫn đến trang tìm kiếm từ vựng
    path('', views.search_word, name='search_word'),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
    path('read-text/', views.read_text, name='read_text'),

    # Đường dẫn khi nhấn nút học
   path('add-to-learning/', views.add_to_learning, name='add_to_learning'),

    # Đường dẫn đến trang learn_new_word
    path('learn-new-word/', views.learn_new_word, name='learn_new_word'),

    # Đường dẫn đến API random word 
    path('random-word/', views.random_word, name='random-word'),

    # Đường dẫn xử lý chức năng hoàn thành, xóa từ
    path('update-learning-status/<int:id>/', views.update_learning_status_view, name='update-learning-status'),
    path('delete-learning-word/<int:id>/', views.delete_learning_word_view, name='delete-learning-word'),
    
]