from django.urls import path
from .views import register, login, logout, admin_register, admin_login
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   path('register/', register, name='register'),
   path('admin-register/', admin_register, name='admin_register'),
   path('login/', login, name='login'),
   path('admin-login/', admin_login, name='admin_login'),
   path('logout/', logout, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
