from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.st_details, name="st_detail"),
    path('data_input/', views.data_input, name='data_input'),
]