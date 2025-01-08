from django.urls import path
from . import views

urlpatterns = [
        path('your_view/', views.your_view, name='your_view'),
        # Thêm các URL patterns khác của bạn ở đây
]