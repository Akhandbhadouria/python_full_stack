from django.contrib import admin
from django.urls import path
from test_1 import views
from . import views
urlpatterns = [
   path('<int:pk>/',views.st_details,name="st_detail"),
]