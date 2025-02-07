from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_chat, name='chat_ai'),
    path('chatbox/', views.chatbox_view, name='chatbox_view'),
    path('sentence-correction/', views.sentence_correction_review, name='sentence_correction'),
]