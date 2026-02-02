from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('student/login/', views.student_login, name='student_login'),
    path('student/signup/', views.student_signup, name='student_signup'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('test/<int:paper_id>/', views.take_test, name='take_test'),
    path('test/<int:paper_id>/submit/', views.submit_test, name='submit_test'),
    path('results/', views.view_results, name='view_results'),
    path('logout/', views.logout_view, name='logout'),
    
    path('admin_portal/login/', views.admin_login, name='admin_login'),
    path('admin_portal/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_portal/paper/create/', views.create_paper, name='create_paper'),
    path('admin_portal/paper/<int:paper_id>/', views.view_paper_admin, name='view_paper_admin'),
    path('admin_portal/paper/<int:paper_id>/add_question/', views.add_question, name='add_question'),
    path('admin_portal/results/', views.admin_view_results, name='admin_view_results'),
]
