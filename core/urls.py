from django.urls import path
from . import views
from django.shortcuts import redirect


urlpatterns = [
    path('', views.home, name='home'),
    path('admin-dashboard/', views.home, name='admin_dashboard'),  # Placeholder
    path('organizer-dashboard/', views.home, name='organizer_dashboard'),  # Placeholder
    path('student-dashboard/', views.home, name='student_dashboard'),  # Placeholder
    path('logout/', lambda request: redirect('login'), name='logout'),  # Dummy logout
]
